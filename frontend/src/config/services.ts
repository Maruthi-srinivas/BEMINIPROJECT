export type ServiceMeta = {
  slug: string;
  index: string;
  name: string;
  blurb: string;
  port: number;
  baseUrl: string;
  wsUrl?: string;
};

const env = import.meta.env;

export const services: ServiceMeta[] = [
  {
    slug: "url-shortener",
    index: "01",
    name: "URL Shortener",
    blurb: "Create short links, redirects, and click analytics.",
    port: 8001,
    baseUrl: env.VITE_URL_SHORTENER_URL || "http://localhost:8001",
  },
  {
    slug: "auth-service",
    index: "02",
    name: "Auth Service",
    blurb: "Register, login, JWT access and refresh tokens.",
    port: 8002,
    baseUrl: env.VITE_AUTH_SERVICE_URL || "http://localhost:8002",
  },
  {
    slug: "rate-limiter",
    index: "03",
    name: "Rate Limiter",
    blurb: "Define policies and check quotas in real time.",
    port: 8003,
    baseUrl: env.VITE_RATE_LIMITER_URL || "http://localhost:8003",
  },
  {
    slug: "file-storage",
    index: "04",
    name: "File Storage",
    blurb: "Buckets, object upload/download, signed URLs.",
    port: 8004,
    baseUrl: env.VITE_FILE_STORAGE_URL || "http://localhost:8004",
  },
  {
    slug: "notifications",
    index: "05",
    name: "Notifications",
    blurb: "Queue email and webhook deliveries with status tracking.",
    port: 8005,
    baseUrl: env.VITE_NOTIFICATIONS_URL || "http://localhost:8005",
  },
  {
    slug: "job-queue",
    index: "06",
    name: "Job Queue",
    blurb: "Enqueue tasks and manage interval schedules.",
    port: 8006,
    baseUrl: env.VITE_JOB_QUEUE_URL || "http://localhost:8006",
  },
  {
    slug: "api-gateway",
    index: "07",
    name: "API Gateway",
    blurb: "JWT-gated reverse proxy with local rate limits.",
    port: 8007,
    baseUrl: env.VITE_API_GATEWAY_URL || "http://localhost:8007",
  },
  {
    slug: "log-aggregator",
    index: "08",
    name: "Log Aggregator",
    blurb: "Ingest structured logs and search across services.",
    port: 8008,
    baseUrl: env.VITE_LOG_AGGREGATOR_URL || "http://localhost:8008",
  },
  {
    slug: "feature-flags",
    index: "09",
    name: "Feature Flags",
    blurb: "Percentage rollouts and attribute targeting.",
    port: 8009,
    baseUrl: env.VITE_FEATURE_FLAGS_URL || "http://localhost:8009",
  },
  {
    slug: "mini-redis",
    index: "10",
    name: "Mini Redis",
    blurb: "In-memory keys with TTL and WebSocket pub/sub.",
    port: 8010,
    baseUrl: env.VITE_MINI_REDIS_URL || "http://localhost:8010",
    wsUrl: env.VITE_MINI_REDIS_WS_URL || "ws://localhost:8010",
  },
];

export function getService(slug: string): ServiceMeta | undefined {
  return services.find((service) => service.slug === slug);
}
