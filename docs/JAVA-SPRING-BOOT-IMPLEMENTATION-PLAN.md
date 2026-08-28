# Java Spring Boot Migration & Inter-Service Architecture Plan

> **Status:** Planning document — no code changes yet.  
> **Scope:** Migrate 10 Python (FastAPI) backend services to Java Spring Boot, make all services inter-communicable, and run the full stack in Docker.  
> **Date:** August 2026

---

## Table of Contents

1. [Current State](#1-current-state)
2. [Target Architecture](#2-target-architecture)
3. [Recommended Spring Boot Stack](#3-recommended-spring-boot-stack)
4. [Repository Layout](#4-repository-layout)
5. [Inter-Service Communication](#5-inter-service-communication)
6. [Docker Strategy](#6-docker-strategy)
7. [Migration Workflow](#7-migration-workflow)
8. [Cross-Cutting Concerns](#8-cross-cutting-concerns)
9. [Frontend Impact](#9-frontend-impact)
10. [CI/CD Changes](#10-cicd-changes)
11. [Implementation Order](#11-implementation-order)
12. [Success Criteria](#12-success-criteria)
13. [Decisions to Make Before Coding](#13-decisions-to-make-before-coding)

---

## 1. Current State

The repository contains **10 independently deployable Python (FastAPI) services**, each with its own `docker-compose.yml`, exposed on host ports **8001–8010**:

| # | Service | Port | Key dependencies |
|---|---------|------|------------------|
| 01 | URL Shortener | 8001 | Postgres, Redis |
| 02 | Auth Service | 8002 | Postgres |
| 03 | Rate Limiter | 8003 | Postgres, Redis |
| 04 | File Storage | 8004 | Local/object storage |
| 05 | Notification Service | 8005 | Postgres, RabbitMQ, Mailhog |
| 06 | Job Queue | 8006 | Postgres, Redis |
| 07 | API Gateway | 8007 | Redis |
| 08 | Log Aggregator | 8008 | Postgres, OpenSearch |
| 09 | Feature Flags | 8009 | Postgres |
| 10 | Mini Redis | 8010 | In-memory, WebSocket |

A **Vite + React frontend** in `frontend/` calls each service directly via `http://localhost:8001`–`8010`.

### Conventions (from `shared/README.md`)

- JSON logs include a request ID when available.
- Configuration is exclusively environment-driven.
- Each service exposes `/health` and owns its database schema.
- OpenAPI documentation at `/docs` per service.

### Important note

Services are **mostly independent today**. The API gateway validates JWT locally and does **not** call auth or rate-limiter services. The goal of this migration is to make **all services able to communicate with each other** while remaining dockerized.

---

## 2. Target Architecture

```
                    ┌─────────────────┐
                    │  React frontend │  (keep as-is; same ports/URLs)
                    └────────┬────────┘
                             │ HTTP
                    ┌────────▼────────┐
                    │  API Gateway    │  Spring Cloud Gateway (replaces 07)
                    │  :8007          │
                    └────────┬────────┘
         ┌───────────────────┼───────────────────┐
         │                   │                   │
   ┌─────▼─────┐      ┌──────▼──────┐     ┌─────▼─────┐
   │ Auth      │◄────►│ URL Short   │◄───►│ Rate Limit│  ... (all 10)
   │ :8002     │      │ :8001       │     │ :8003     │
   └─────┬─────┘      └──────┬──────┘     └─────┬─────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
              Docker network: bemini-net
              + Postgres, Redis, RabbitMQ, OpenSearch, Mailhog
```

**Core idea:** One root `docker-compose.yml` puts all services on a shared Docker network. Each Spring Boot app resolves sibling services by hostname (`auth-service`, `url-shortener`, etc.) and communicates over HTTP (sync) or message brokers (async).

---

## 3. Recommended Spring Boot Stack

| Python (current) | Java (target) |
|------------------|---------------|
| FastAPI | Spring Web (`spring-boot-starter-web`) |
| Pydantic models | Java records + `jakarta.validation` |
| SQLAlchemy | Spring Data JPA + Flyway or Liquibase |
| `redis` client | Spring Data Redis (Lettuce) |
| RabbitMQ workers | Spring AMQP + `@RabbitListener` |
| `httpx` outbound calls | OpenFeign or WebClient |
| `/docs` OpenAPI | springdoc-openapi |
| Env-based config | `application.yml` + environment variables |
| `shared/` utilities | Maven/Gradle `common` module |

### Recommended versions

- **Java:** 21
- **Spring Boot:** 3.3+
- **Spring Cloud:** 2023.x (if using Gateway / service discovery)

---

## 4. Repository Layout

Keep the frontend unchanged. Add a Java monorepo alongside Python (parallel migration) or replace Python folders when parity is reached.

```
BEMINIPROJECT/
├── frontend/                    # unchanged
├── java/                        # new root for all Spring services
│   ├── pom.xml                  # parent POM (or build.gradle.kts)
│   ├── common/                  # shared lib (JWT, logging, DTOs, Feign config)
│   ├── url-shortener/           # maps to 01
│   ├── auth-service/            # maps to 02
│   ├── rate-limiter/            # maps to 03
│   ├── file-storage/            # maps to 04
│   ├── notification-service/    # maps to 05 (app + worker profile)
│   ├── job-queue/               # maps to 06 (app + worker profile)
│   ├── api-gateway/             # maps to 07
│   ├── log-aggregator/          # maps to 08
│   ├── feature-flags/           # maps to 09
│   └── mini-redis/              # maps to 10
├── docker-compose.yml           # ONE compose for entire stack
├── docker-compose.infra.yml     # optional: only DBs/brokers
└── docs/
    └── JAVA-SPRING-BOOT-IMPLEMENTATION-PLAN.md  # this file
```

Each service is its own Spring Boot application with:

- `src/main/java/...`
- `src/main/resources/application.yml`
- `Dockerfile` (multi-stage: Maven build → JRE runtime)
- Same **external host port** as today (`8001`–`8010`) so the frontend keeps working

---

## 5. Inter-Service Communication

### Option A — Docker DNS + OpenFeign (recommended to start)

1. Define one shared network in root `docker-compose.yml`: `bemini-net`.
2. Assign stable hostnames per service: `auth-service`, `rate-limiter`, `url-shortener`, etc.
3. Configure service URLs in each app's `application.yml`:

```yaml
services:
  auth:
    url: http://auth-service:8000
  url-shortener:
    url: http://url-shortener:8000
  rate-limiter:
    url: http://rate-limiter:8000
  # ... all 10
```

4. Define Feign client interfaces in the `common` module.
5. Any service can inject and call another, e.g. `@Autowired AuthClient authClient`.

**Pros:** Simple, no extra infrastructure, works well in Docker Compose.  
**Cons:** URLs are static (acceptable for Compose and Kubernetes with stable service names).

### Option B — Spring Cloud (Eureka + Gateway + Feign)

1. Run a **Eureka server** as a service registry.
2. Each app registers as `AUTH-SERVICE`, `RATE-LIMITER`, etc.
3. **OpenFeign** resolves `http://AUTH-SERVICE/...` via Spring Cloud LoadBalancer.
4. **Spring Cloud Gateway** replaces the current API gateway with routes to all backends.

**Pros:** Closer to production microservices; dynamic discovery.  
**Cons:** Extra container and operational complexity.

### Sync vs async communication

| Service | Primary communication |
|---------|----------------------|
| Auth | Google OAuth (external); other services call it for JWT validation |
| URL Shortener | Postgres + Redis; may call log-aggregator, feature-flags |
| Rate Limiter | Redis; other services call it before heavy operations |
| File Storage | Object storage; HMAC signed URLs |
| Notifications | RabbitMQ + SMTP; HTTP webhook callbacks |
| Job Queue | Redis + Postgres; HTTP callbacks to arbitrary URLs |
| API Gateway | Proxies to all backends; JWT validation |
| Log Aggregator | OpenSearch; every service POSTs logs here |
| Feature Flags | Postgres; every service checks flags before behavior |
| Mini Redis | In-memory KV + WebSocket pub/sub |

### Practical mesh pattern

Do not literally call every service from every service. Instead:

- **Cross-cutting clients in `common`:** `AuthClient`, `LogClient`, `FeatureFlagsClient`, `RateLimiterClient`.
- **Gateway** routes external traffic and enforces auth + rate limits.
- **Async** where appropriate: notifications and job queue via RabbitMQ/Redis.

This provides full mesh *capability* without unnecessary coupling.

---

## 6. Docker Strategy

### Root `docker-compose.yml` structure

```yaml
services:
  # --- Infrastructure ---
  postgres-auth: ...
  postgres-url: ...
  redis-shared: ...        # or per-service Redis like today
  rabbitmq: ...
  opensearch: ...
  mailhog: ...

  # --- Java services (all on bemini-net) ---
  url-shortener:
    build: ./java/url-shortener
    ports: ["8001:8000"]
    environment:
      DATABASE_URL: jdbc:postgresql://postgres-url:5432/...
      REDIS_URL: redis://redis-shared:6379
      SERVICES_AUTH_URL: http://auth-service:8000
      SERVICES_LOG_URL: http://log-aggregator:8000
      # ... URLs for all sibling services
    networks: [bemini-net]
    depends_on: [...]

  auth-service:
    ports: ["8002:8000"]
    ...

  # ... repeat for services 03–10

  notification-worker:
    build: ./java/notification-service
    command: ["java", "-jar", "app.jar", "--spring.profiles.active=worker"]

networks:
  bemini-net:
    driver: bridge
```

### Dockerfile pattern (per service)

Multi-stage build:

1. **Build stage:** `maven:3.9-eclipse-temurin-21` → `mvn -pl <module> -am package -DskipTests`
2. **Run stage:** `eclipse-temurin:21-jre-alpine` → copy `target/*.jar` → `EXPOSE 8000` → `ENTRYPOINT java -jar app.jar`

### Docker checklist

- **Internal container port:** 8000
- **Host port mapping:** 8001–8010 (same as Python)
- **Healthchecks:** `/actuator/health` or `/health` with `depends_on: condition: service_healthy`
- **Shared network:** `bemini-net` so `http://auth-service:8000` resolves from any container
- **Per-service databases:** preserve independence (one Postgres instance per service or separate DB names)

### Run the full stack

```bash
docker compose up --build
```

---

## 7. Migration Workflow

### Phase 0 — Contract freeze

1. Export OpenAPI specs from each Python service (`/docs` → download JSON/YAML).
2. Treat those specs as the **API contract** the Java services must implement.
3. Document environment variables from each `config/.env.example` and `docker-compose.yml`.

### Phase 1 — Scaffold

1. Create parent Maven project + `common` module.
2. Generate 10 Spring Boot apps (Web, JPA, Validation, Actuator).
3. Add root `docker-compose.yml` with infrastructure only; verify Postgres, Redis, RabbitMQ, OpenSearch start.

### Phase 2 — Migrate one simple service first

Start with **09-feature-flags** or **03-rate-limiter**.

1. Implement REST API to match OpenAPI contract.
2. Add Dockerfile; plug into compose on the correct port.
3. Write JUnit + MockMvc or Testcontainers tests (parity with existing pytest suites).
4. Point frontend at the Java instance; confirm UI works.

### Phase 3 — Cross-cutting services

1. **Auth** — JWT issuance; other services validate via `common` security filter or gateway.
2. **Log aggregator** — add `LogClient` in `common`; every Java service ships logs here.
3. **API Gateway** — Spring Cloud Gateway routes to all Java backends.

### Phase 4 — Async services

1. **Notifications** — Spring AMQP + worker profile (mirrors Python `worker` container).
2. **Job queue** — Redis + scheduled jobs + worker profile.

### Phase 5 — Special cases

1. **Mini Redis** — WebSocket with Spring WebSocket/STOMP (most complex port).
2. **File storage** — multipart upload, HMAC signed URLs.

### Phase 6 — Full mesh

1. Add Feign clients in `common` for all 10 services.
2. Add a demo/internal endpoint per service, e.g. `GET /internal/ping-all`, that calls the other nine (proves inter-service wiring).
3. Decommission Python folders when parity is reached.

---

## 8. Cross-Cutting Concerns

| Concern | Approach |
|---------|----------|
| Authentication | Gateway validates JWT; service-to-service uses internal API keys or service JWT (`client_credentials` from auth-service) |
| Timeouts / retries | Resilience4j on Feign / WebClient |
| Correlation IDs | Propagate `X-Request-Id` in a `common` servlet filter (mirrors `shared/logging.py`) |
| Configuration | Environment variables in compose; optional Spring Cloud Config later |
| Observability | Spring Actuator + Micrometer; all services → log-aggregator |
| CORS | Gateway handles CORS for frontend; internal service calls skip CORS |

---

## 9. Frontend Impact

`frontend/src/config/services.ts` already uses `http://localhost:8001`–`8010`.

If Java services keep the same ports and API paths, **no frontend changes are required**.

Update the frontend only if:

- Path prefixes change (avoid this).
- Mini Redis WebSocket URL changes.
- All traffic is routed exclusively through the gateway (then point `VITE_*_URL` env vars to gateway paths).

---

## 10. CI/CD Changes

Replace `.github/workflows/test-services.yml` Python job with:

- Matrix build across 10 Java modules
- `mvn test` per module
- Optional: `docker compose up -d` + integration smoke tests
- Build and push 10 Docker images to a registry (GHCR, Docker Hub)

---

## 11. Implementation Order

| Order | Service | Rationale |
|-------|---------|-----------|
| 1 | `common` + compose infra | Foundation for all services |
| 2 | `09-feature-flags` | Simple CRUD; good template |
| 3 | `02-auth-service` | Needed by gateway and other services |
| 4 | `03-rate-limiter` | Redis logic port |
| 5 | `08-log-aggregator` | Wire all services to centralized logging |
| 6 | `07-api-gateway` | Central entry + routing |
| 7 | `01-url-shortener` | Classic CRUD + Redis |
| 8 | `04-file-storage` | File I/O and signed URLs |
| 9 | `06-job-queue` | Worker pattern with Redis |
| 10 | `05-notification-service` | RabbitMQ + worker |
| 11 | `10-mini-redis` | WebSocket last (highest complexity) |

---

## 12. Success Criteria

After implementation, this command should work:

```bash
docker compose up --build
```

And deliver:

- [ ] All 10 Java services healthy on ports 8001–8010
- [ ] Frontend works without changes
- [ ] Any service can call any other via Docker hostnames
- [ ] Gateway routes external traffic with JWT + rate limits
- [ ] Workers (notifications, jobs) process queues correctly
- [ ] One command tears down the entire stack

---

## 13. Decisions to Make Before Coding

| Decision | Recommendation |
|----------|----------------|
| Monorepo vs 10 separate repos | **Monorepo** (Maven multi-module) for this project |
| Service discovery | **Docker DNS** to start; Eureka optional later |
| Replace Python in place vs parallel tree | **Parallel `java/` tree** during migration (safer) |
| Shared vs per-service databases | **Per-service databases** (keep current independence) |
| Shared vs per-service Redis | Match current design (per-service or shared as needed) |

---

## Appendix: Port & Service Name Reference

| Service folder | Docker hostname (suggested) | Host port | Container port |
|----------------|----------------------------|-----------|----------------|
| `01-url-shortener` | `url-shortener` | 8001 | 8000 |
| `02-auth-service` | `auth-service` | 8002 | 8000 |
| `03-rate-limiter` | `rate-limiter` | 8003 | 8000 |
| `04-file-storage` | `file-storage` | 8004 | 8000 |
| `05-notification-service` | `notification-service` | 8005 | 8000 |
| `06-job-queue` | `job-queue` | 8006 | 8000 |
| `07-api-gateway` | `api-gateway` | 8007 | 8000 |
| `08-log-aggregator` | `log-aggregator` | 8008 | 8000 |
| `09-feature-flags` | `feature-flags` | 8009 | 8000 |
| `10-mini-redis` | `mini-redis` | 8010 | 8000 |

---

*This document is the canonical implementation plan for the Java Spring Boot migration. Update it as decisions are made and phases are completed.*
