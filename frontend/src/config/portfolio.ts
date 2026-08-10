export type SkillCategory = {
  category: string;
  items: string[];
};

export type Highlight = {
  id: string;
  title: string;
  body: string;
  tags: string[];
  talkingPoint?: string;
  /** Service slugs this highlight maps to for ServiceShell callouts */
  serviceSlugs?: string[];
};

export type NarrativeBlock = {
  label: string;
  title: string;
  body: string;
};

export type ArchNode = {
  id: string;
  label: string;
  kind: "service" | "infra" | "hub";
  theme?: string;
  blurb?: string;
  slug?: string;
};

export const portfolio = {
  brand: "BE Mini Lab",
  projectTitle: "BE Mini Lab — Multi-Service Backend Systems Lab",
  oneLiner:
    "Built 10 independently deployable FastAPI services covering auth, caching, rate limiting, messaging, job processing, API gatewaying, logging, and feature flags — each with Docker Compose, PostgreSQL/Redis where needed, pytest, and GitHub Actions CI.",
  heroHeadline: "Ten backend systems. One neon command deck.",
  heroSub:
    "A cyberpunk ops console over a production-style FastAPI portfolio — independent services, real data stores, and live demos you can jack into.",
  metrics: [
    { value: "10", label: "Services" },
    { value: "FastAPI", label: "Stack" },
    { value: "4+", label: "Data stores" },
    { value: "CI", label: "GitHub Actions" },
  ],
  starNarrative: [
    {
      label: "01 // Situation",
      title: "Beyond CRUD",
      body: "Interview-ready depth needed more than a single demo app — systems that mirror what production teams run: auth, rate limiting, queues, gateways, caching, and observability.",
    },
    {
      label: "02 // Task",
      title: "Ship ten labs",
      body: "Design and ship 10 independently deployable FastAPI services, each with its own data store, Docker Compose stack, tests, and clear operational concerns — security, durability, and performance.",
    },
    {
      label: "03 // Result",
      title: "Demo-ready depth",
      body: "A working multi-service portfolio with concrete talking points on auth security, rate-limit algorithms, messaging reliability, and caching — including real failure modes like token reuse, poison messages, and cache inconsistency.",
    },
  ] as NarrativeBlock[],
  skills: [
    {
      category: "Languages",
      items: ["Python 3.12", "TypeScript", "SQL"],
    },
    {
      category: "Frameworks",
      items: ["FastAPI", "React", "Vite", "OpenAPI"],
    },
    {
      category: "Data",
      items: ["PostgreSQL", "Redis", "RabbitMQ", "OpenSearch"],
    },
    {
      category: "Infra",
      items: ["Docker", "Docker Compose", "GitHub Actions"],
    },
    {
      category: "Practices",
      items: ["JWT/OAuth", "RBAC", "pytest", "httpx", "Health checks"],
    },
  ] as SkillCategory[],
  highlights: [
    {
      id: "ten-services",
      title: "Ten production-style FastAPI services",
      body: "Designed and implemented 10 independently deployable services with OpenAPI docs, health checks, and Docker Compose stacks using PostgreSQL, Redis, RabbitMQ, and OpenSearch.",
      tags: ["FastAPI", "Docker", "OpenAPI"],
      talkingPoint:
        "Independent labs, not a mesh — each owns DB/config/deploy; the gateway is self-contained with no cross-service calls.",
      serviceSlugs: [],
    },
    {
      id: "auth",
      title: "Auth with JWT, refresh rotation & OIDC",
      body: "Argon2 password hashing, JWT access tokens, rotating/revocable refresh tokens hashed at rest, RBAC, and Google OIDC login.",
      tags: ["JWT", "Argon2", "OIDC", "RBAC"],
      talkingPoint:
        "Short-lived JWT + rotating refresh; refresh tokens stored hashed; role-gated admin routes.",
      serviceSlugs: ["auth-service", "api-gateway"],
    },
    {
      id: "rate-limits",
      title: "Redis rate limiting + API gateway",
      body: "Lua token-bucket and sliding-window (ZSET) algorithms, plus an API gateway with JWT verification, prefix-based reverse proxying, and local rate limiting.",
      tags: ["Redis", "Lua", "Gateway"],
      talkingPoint:
        "Token bucket vs sliding window tradeoffs; Lua/Redis for atomicity under concurrency.",
      serviceSlugs: ["rate-limiter", "api-gateway"],
    },
    {
      id: "messaging",
      title: "Messaging & job pipelines",
      body: "RabbitMQ notification pipeline with durable queues, retry/backoff, and a dead-letter queue; Redis job queue with workers and interval-based schedulers.",
      tags: ["RabbitMQ", "DLQ", "Workers"],
      talkingPoint:
        "Why DLQ + retries matter; at-least-once delivery implications for consumers.",
      serviceSlugs: ["notifications", "job-queue"],
    },
    {
      id: "storage",
      title: "Object store & URL shortener",
      body: "Mini object store with filesystem + DB metadata, HMAC-SHA256 signed URLs, and path-traversal safeguards; URL shortener with Redis read-through caching and click analytics.",
      tags: ["HMAC", "Redis cache", "Analytics"],
      talkingPoint:
        "Signed URLs for temporary access without exposing the object store.",
      serviceSlugs: ["file-storage", "url-shortener"],
    },
    {
      id: "flags-logs-kv",
      title: "Flags, logs & in-memory KV",
      body: "Feature flags with sticky percentage rollouts and attribute rules; OpenSearch log aggregator with source-token auth; in-memory KV with TTL and WebSocket pub/sub.",
      tags: ["Feature flags", "OpenSearch", "WebSocket"],
      talkingPoint:
        "Sticky % rollout via hash so users don’t flip mid-session.",
      serviceSlugs: ["feature-flags", "log-aggregator", "mini-redis"],
    },
  ] as Highlight[],
  architectureHub: {
    id: "hub",
    label: "Independent deployable services",
    kind: "hub" as const,
    blurb: "Each service owns its config, store, and deploy — not a shared mesh.",
  },
  architectureInfra: [
    {
      id: "postgres",
      label: "PostgreSQL",
      kind: "infra" as const,
      blurb: "Relational persistence where services need durable records.",
    },
    {
      id: "redis",
      label: "Redis",
      kind: "infra" as const,
      blurb: "Caching, rate limits, job queues, and TTL-backed keys.",
    },
    {
      id: "rabbitmq",
      label: "RabbitMQ",
      kind: "infra" as const,
      blurb: "Durable notification queues with retries and DLQ.",
    },
    {
      id: "opensearch",
      label: "OpenSearch",
      kind: "infra" as const,
      blurb: "Structured log ingest and search across services.",
    },
  ] as ArchNode[],
  footerStack: ["Python", "FastAPI", "React", "Docker", "pytest"],
  footerNote: "Built with FastAPI + React · Independent Docker Compose stacks",
};

export function getHighlightForService(slug: string): Highlight | undefined {
  return portfolio.highlights.find((h) => h.serviceSlugs?.includes(slug));
}

export const navAnchors = [
  { id: "story", label: "Story" },
  { id: "architecture", label: "Architecture" },
  { id: "skills", label: "Skills" },
  { id: "highlights", label: "Highlights" },
  { id: "services", label: "Demos" },
] as const;
