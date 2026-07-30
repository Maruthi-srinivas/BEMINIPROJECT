export type ServiceMeta = {
  slug: string;
  index: string;
  name: string;
  blurb: string;
  port: number;
  baseUrl: string;
  wsUrl?: string;
  theme: string;
  realm: string;
  game: string;
  tagline: string;
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
    theme: "theme-zelda",
    realm: "Sheikah Gateways",
    game: "Zelda: Breath of the Wild",
    tagline: "Warp shrines that fold the open world into a single glyph.",
  },
  {
    slug: "auth-service",
    index: "02",
    name: "Auth Service",
    blurb: "Register, login, JWT access and refresh tokens.",
    port: 8002,
    baseUrl: env.VITE_AUTH_SERVICE_URL || "http://localhost:8002",
    theme: "theme-cyberpunk",
    realm: "Night City NetID",
    game: "Cyberpunk 2077",
    tagline: "Rip chrome credentials and burn ice on every login.",
  },
  {
    slug: "rate-limiter",
    index: "03",
    name: "Rate Limiter",
    blurb: "Define policies and check quotas in real time.",
    port: 8003,
    baseUrl: env.VITE_RATE_LIMITER_URL || "http://localhost:8003",
    theme: "theme-elden",
    realm: "Golden Order Seals",
    game: "Elden Ring",
    tagline: "Grace meters who may pass the fog gate — and who may not.",
  },
  {
    slug: "file-storage",
    index: "04",
    name: "File Storage",
    blurb: "Buckets, object upload/download, signed URLs.",
    port: 8004,
    baseUrl: env.VITE_FILE_STORAGE_URL || "http://localhost:8004",
    theme: "theme-skyrim",
    realm: "Dragon Vault",
    game: "The Elder Scrolls V: Skyrim",
    tagline: "Stash relics in frostbound chests sealed by Thu'um keys.",
  },
  {
    slug: "notifications",
    index: "05",
    name: "Notifications",
    blurb: "Queue email and webhook deliveries with status tracking.",
    port: 8005,
    baseUrl: env.VITE_NOTIFICATIONS_URL || "http://localhost:8005",
    theme: "theme-horizon",
    realm: "Machine Signal Relay",
    game: "Horizon Forbidden West",
    tagline: "Fire signal flares across the wilds to hunters and machines.",
  },
  {
    slug: "job-queue",
    index: "06",
    name: "Job Queue",
    blurb: "Enqueue tasks and manage interval schedules.",
    port: 8006,
    baseUrl: env.VITE_JOB_QUEUE_URL || "http://localhost:8006",
    theme: "theme-witcher",
    realm: "White Wolf Contracts",
    game: "The Witcher 3",
    tagline: "Pin contracts on the notice board and hunt them down on schedule.",
  },
  {
    slug: "api-gateway",
    index: "07",
    name: "API Gateway",
    blurb: "JWT-gated reverse proxy with local rate limits.",
    port: 8007,
    baseUrl: env.VITE_API_GATEWAY_URL || "http://localhost:8007",
    theme: "theme-masseffect",
    realm: "Citadel Relay",
    game: "Mass Effect",
    tagline: "Authorize mass-effect corridors between systems.",
  },
  {
    slug: "log-aggregator",
    index: "08",
    name: "Log Aggregator",
    blurb: "Ingest structured logs and search across services.",
    port: 8008,
    baseUrl: env.VITE_LOG_AGGREGATOR_URL || "http://localhost:8008",
    theme: "theme-fallout",
    realm: "Vault-Tec Terminal",
    game: "Fallout",
    tagline: "Scroll amber archives under flickering vault fluorescents.",
  },
  {
    slug: "feature-flags",
    index: "09",
    name: "Feature Flags",
    blurb: "Percentage rollouts and attribute targeting.",
    port: 8009,
    baseUrl: env.VITE_FEATURE_FLAGS_URL || "http://localhost:8009",
    theme: "theme-tsushima",
    realm: "Ghost Banners",
    game: "Ghost of Tsushima",
    tagline: "Raise clan banners for chosen warriors across the island.",
  },
  {
    slug: "mini-redis",
    index: "10",
    name: "Mini Redis",
    blurb: "In-memory keys with TTL and WebSocket pub/sub.",
    port: 8010,
    baseUrl: env.VITE_MINI_REDIS_URL || "http://localhost:8010",
    wsUrl: env.VITE_MINI_REDIS_WS_URL || "ws://localhost:8010",
    theme: "theme-nms",
    realm: "Atlas Memory Bank",
    game: "No Man's Sky",
    tagline: "Cache stardust memories before entropy claims them.",
  },
];

export function getService(slug: string): ServiceMeta | undefined {
  return services.find((service) => service.slug === slug);
}
