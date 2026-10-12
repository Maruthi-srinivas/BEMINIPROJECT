"""Register D11-T001..D11-T025 content. Called by generate_d11_content.py."""
from populate_d11_core import (
    ans,
    default_trade_rows,
    mermaid_cache_aside,
    mermaid_cluster,
    mermaid_redis_types,
    mermaid_sentinel,
    std_interview,
)


def _code_cache_aside_py() -> str:
    return '''def get_product(redis, db, product_id: int):
    key = f"product:{product_id}"
    cached = redis.get(key)
    if cached is not None:
        return cached
    row = db.fetch_one("SELECT payload FROM products WHERE id = %s", (product_id,))
    if row is None:
        return None
    redis.setex(key, 300, row["payload"])
    return row["payload"]'''


def _code_sliding_lua() -> str:
    return '''-- KEYS[1]=zset key, ARGV[1]=now_ms, ARGV[2]=window_ms, ARGV[3]=limit
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
local count = redis.call('ZCARD', key)
if count < limit then
  redis.call('ZADD', key, now, now .. '-' .. math.random(1000000))
  redis.call('PEXPIRE', key, window)
  return 1
end
return 0'''


def _code_lock_lua() -> str:
    return '''-- SET lock_key token NX PX ttl_ms (from client)
-- unlock: if redis.call("get",KEYS[1])==ARGV[1] then return redis.call("del",KEYS[1]) else return 0 end'''


def _iv(theme: str, bq, iq, aq, sq, fq) -> dict:
    return std_interview(theme, bq, iq, aq, sq, fq)


def populate(register) -> None:
    # D11-T001
    register(
        "D11-T001",
        overview=[
            "Caching stores a copy of expensive-to-compute or expensive-to-fetch data closer to the consumer so repeated work is avoided.",
            "It works because real workloads are skewed: a small fraction of keys or pages receive most reads, and RAM is orders of magnitude faster than disk or cross-service RPC for hot data.",
            "In backend interviews, 'why caching works' is the setup for hit ratio, consistency, and failure handling; you must separate latency wins from correctness risks.",
            "Prerequisites: relational read paths (`D07-T001`) and request lifecycle (`D05-T002`). Later topics assume you can explain a miss versus a hit on the read path.",
        ],
        first_principles=[
            "Every read has a cost model: CPU to compute, I/O to disk, network to another service, and serialization. Caching trades memory for repeating that cost.",
            "Temporal locality means recently used data is likely reused. Spatial locality means nearby data may be reused; caches exploit temporal locality first.",
            "A cache entry is a derived artifact: it can be wrong if the origin changes and the cache is not updated. That is why TTL and invalidation exist in later topics.",
        ],
        internal=[
            "Components: origin store (database), cache store (Redis or local), application logic that checks the cache first on reads.",
            "On a hit, the app returns the cached bytes without touching the origin. On a miss, the app loads from origin, optionally transforms, then stores in cache with TTL or version metadata.",
            "Memory hierarchy analogy: L1/L2 CPU caches, page cache in the OS, application cache, CDN edge, and database buffer pool are all the same pattern at different distances from the CPU.",
        ],
        mermaid="""flowchart TD
  readPath[ReadRequest]
  l1[LocalOptional]
  redisLayer[Redis]
  origin[Database]
  readPath --> l1
  l1 -->|miss| redisLayer
  redisLayer -->|miss| origin
  origin --> redisLayer
  redisLayer --> readPath""",
        mermaid_caption="Read path with optional local layer then shared Redis before the database.",
        examples=[
            "Analogy: a waiter who remembers today's specials avoids walking to the kitchen for every table. The kitchen menu is still authoritative if the chef changes the dish.",
            "Product catalog pages are classic: 10k SKUs but 200 drive 80% of views. Caching those 200 rows cuts database QPS dramatically.",
            "Do not cache without measuring: if hit ratio is 5%, you added complexity and another failure domain for little gain.",
        ],
        code_file="examples/d11_t001_cache_read.py",
        code=_code_cache_aside_py(),
        code_run="Requires Redis and a DB stub; run as a module test with fakeredis or integration test.",
        code_output="First call miss (DB query); second call hit (no DB).",
        code_notes=[
            "Important lines: check cache before DB; setex sets TTL so stale data has a bounded lifetime.",
            "Edge cases: null product should not be cached forever without a short TTL (see penetration topic).",
        ],
        practical=[
            "Instrument hits and misses per endpoint. Alert when miss latency drives p99 while mean stays flat.",
            "Size Redis memory from working set of hot keys, not total table size. Use correlation IDs to trace a slow miss path.",
        ],
        trade_table=default_trade_rows(),
        trade_extra=["Under load, a cache shifts bottleneck from DB to Redis memory and network. Plan eviction before you run out of RAM."],
        mistakes=[
            "Assuming caching fixes a slow query without indexing the origin.",
            "Caching personalized responses under a key that omits user id.",
            "Treating Redis as durable primary storage without persistence design.",
        ],
        debug=[
            "Symptom: DB CPU unchanged after adding Redis. Check hit ratio and whether keys match request parameters.",
            "Symptom: sporadic slow requests. Often large miss payloads or connection pool exhaustion on origin.",
        ],
        interview=_iv(
            "why caching works",
            [
                "What problem does a cache solve?",
                "What is temporal locality?",
                "Why is RAM faster than disk for hot reads?",
                "What is a cache hit versus a miss?",
                "When does caching not help?",
            ],
            [
                "How do you measure whether a cache is worth operating?",
                "What metrics prove a cache helps?",
                "How does skew affect cache sizing?",
                "What is the working set?",
                "How do you roll out a new cache safely?",
            ],
            [
                "How can caching hide a broken origin?",
                "What is the consistency cost of caching?",
                "Compare CDN, app cache, and DB buffer pool.",
                "How do multi-layer caches interact?",
                "What happens during a cold start?",
            ],
            [
                "DB CPU is high but you added Redis. What do you check?",
                "Latency improved at p50 but not p99. Why?",
                "Marketing launch tomorrow; how do you warm the cache?",
                "Redis memory is full. What breaks first?",
                "Two regions, one database. Where do you cache?",
            ],
            [
                "How does this connect to database indexes?",
                "What topic covers invalidation?",
                "When should you skip caching entirely?",
            ],
        ),
        ex1="Implement `get_product` cache-aside with metrics counters for hit and miss. Acceptance: second call does not query DB; TTL is 300s.",
        ex2="Dashboard shows 40% hit ratio on a catalog endpoint that should be 95%. List three concrete checks on keys, TTL, and deployment.",
        ex3="Choose local Caffeine versus Redis for feature flags. State consistency and rollout implications.",
        sol1="See topic note section F; add `metrics.incr('product_cache_hit')` on hit branch.",
        sol2="Verify key includes product_id, confirm all pods point to same Redis, check if deploy flushed Redis or changed key prefix.",
        sol3="Redis if flags must be consistent across pods within seconds; local if flags are immutable per deploy and you accept staggered visibility.",
        exec_status="not executed (documentation example)",
        revision=["Caches exploit skew and reuse.", "Measure hit ratio before scaling Redis.", "Every cache entry is derived and can be stale."],
        flash=[("What is a hit?", "Origin not consulted."), ("What is working set?", "Keys that fit in cache and matter for traffic.")],
        before="`D07-T001` relational reads and `D05-T002` request path.",
        supports="`D11-T002` hit ratio, `D11-T003` cache-aside.",
        confused="CDN edge cache versus application Redis.",
        combine="`D07-T019` indexes, `D06-T012` rate limits.",
        completion=[
            "Explain locality and skew without notes.",
            "Draw read path with hit and miss.",
            "Name two metrics that prove cache value.",
            "State when caching fails to help.",
        ],
    )

    # Remaining topics registered via bulk helper
    from populate_d11_bulk import bulk_register  # noqa: WPS433

    bulk_register(register)
