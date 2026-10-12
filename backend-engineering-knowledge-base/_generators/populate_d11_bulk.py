"""Bulk registration for D11-T002..D11-T025."""
from populate_d11_core import ans, default_trade_rows, mermaid_cache_aside, mermaid_cluster, mermaid_redis_types, mermaid_sentinel, std_interview


def _r(
    register,
    tid: str,
    title: str,
    theme: str,
    overview_tail: str,
    first: list[str],
    internal: list[str],
    mermaid: str,
    cap: str,
    examples: list[str],
    code_file: str,
    code: str,
    mistakes: list[str],
    debug: list[str],
    bq: list[str],
    iq: list[str],
    aq: list[str],
    sq: list[str],
    fq: list[str],
    ex1: str,
    ex2: str,
    ex3: str,
    sol1: str,
    sol2: str,
    sol3: str,
    revision: list[str],
    flash: list[tuple[str, str]],
    supports: str,
    confused: str,
    combine: str,
    completion: list[str],
    practical: list[str] | None = None,
    trade_extra: list[str] | None = None,
):
    prev = f"`{tid.replace('T', '-T').split('-')[0]}-T{int(tid.split('-T')[1]) - 1:03d}`" if int(tid.split("-T")[1]) > 1 else "`D07-T001`, `D05-T002`"
    register(
        tid,
        overview=[
            f"{title} is a core Redis and caching topic for backend interviews and production systems.",
            overview_tail,
            "Interviewers use it to see whether you reason about latency, consistency, and operations together rather than listing Redis commands.",
            f"Build on earlier domain 11 notes; dependencies in inventory point to {prev} and database fundamentals.",
        ],
        first_principles=first,
        internal=internal,
        mermaid=mermaid,
        mermaid_caption=cap,
        examples=examples,
        code_file=code_file,
        code=code,
        code_run="Run in integration test with Redis 7+ or documented stub.",
        code_output="Behavior described in topic note section F.",
        code_notes=[
            "Treat Redis as a remote service: timeouts, retries with jitter, and circuit breakers on the miss path.",
            "Keep keys namespaced (`service:entity:id`) to avoid collisions and to enable scan-based invalidation.",
        ],
        practical=practical
        or [
            "Expose hit ratio, evicted keys, and used memory on dashboards tied to release markers.",
            "Document stale-read tolerance per entity in the same place you document TTL.",
        ],
        trade_table=default_trade_rows(),
        trade_extra=trade_extra or ["Operational cost rises with another moving part; runbooks must cover Redis failover."],
        mistakes=mistakes,
        debug=debug,
        interview=std_interview(theme, bq, iq, aq, sq, fq),
        ex1=ex1,
        ex2=ex2,
        ex3=ex3,
        sol1=sol1,
        sol2=sol2,
        sol3=sol3,
        revision=revision,
        flash=flash,
        before=prev,
        supports=supports,
        confused=confused,
        combine=combine,
        completion=completion,
    )


def bulk_register(register) -> None:
    _r(
        register,
        "D11-T002",
        "Cache hit ratio and cache efficiency",
        "cache hit ratio",
        "Hit ratio is the fraction of reads served from the cache; efficiency ties that ratio to bytes stored, eviction rate, and origin load removed.",
        [
            "Hit ratio = hits / (hits + misses). Misses still pay full origin cost, so a low ratio can mean the cache is pure overhead.",
            "Efficiency also asks whether cached entries are large relative to benefit and whether TTL matches change frequency.",
            "A high ratio on a tiny slice of traffic may not reduce DB QPS if the DB bottleneck is elsewhere.",
        ],
        [
            "Instrument at the application boundary where hit/miss is known, not only Redis INFO stats.",
            "Break down ratio by endpoint, key prefix, and tenant to find useless caches.",
            "Combine with origin QPS and p99 miss latency to decide memory sizing.",
        ],
        mermaid_cache_aside(),
        "Efficiency requires measuring hits and misses on the same code path.",
        ["If 90% of requests hit but they are health checks, you optimized the wrong thing.", "Efficiency drops if you cache huge JSON blobs for rarely repeated keys."],
        "examples/d11_t002_metrics.py",
        "hits = cache_hits; misses = cache_misses; ratio = hits / (hits + misses) if (hits + misses) else 0",
        ["Reporting ratio without denominators hides low traffic endpoints.", "Using Redis keyspace hits without app-level miss detection undercounts misses."],
        ["Hit ratio dropped after deploy: key prefix change.", "Ratio high but DB load high: caching wrong query or shard hot spot."],
        ["Define cache hit ratio.", "Why can hit ratio be misleading?", "What is a good hit ratio?", "How do you measure hits and misses?", "What is cache efficiency beyond ratio?"],
        ["How do you size Redis from hit ratio data?", "What SLO uses hit ratio?", "How does object size affect efficiency?", "What is the cost of a miss?", "How do you A/B cache TTL?"],
        ["Little's law and cache at scale.", "Hit ratio versus working set fit.", "Multi-tenant fairness in cache.", "When to shard cache by tenant.", "Efficiency of negative caching."],
        ["Hit ratio 99% but users see stale prices.", "Sudden ratio drop at midnight.", "One pod has low ratio.", "Cache added but DB CPU flat.", "Ratio good on staging, bad in prod."],
        ["Link to TTL topic?", "How does eviction affect ratio?", "Relation to CDN cache metrics?"],
        "Emit hit/miss counters and compute ratio in Grafana.",
        "Ratio fell after adding a new query param to URLs without updating cache keys.",
        "Pick TTL 60s vs 3600s for product metadata given 5-minute admin update SLA.",
        "Use Prometheus counters `cache_hit_total` and `cache_miss_total`.",
        "Include all query params in cache key hash or normalize them.",
        "3600s if stale up to an hour is acceptable; 60s if marketing needs faster visibility; add explicit invalidation on admin write.",
        ["Hit ratio needs hits and misses.", "Segment metrics by endpoint.", "Efficiency includes bytes and origin savings."],
        [("Good ratio?", "Depends on working set fit, not a universal 95%.")],
        "`D11-T003` cache-aside patterns.",
        "Hit rate in Redis INFO versus application hit ratio.",
        "`D13-T015` observability, `D07-T019` indexes.",
        ["Compute hit ratio from app metrics.", "Explain misleading high ratio.", "Pick TTL using SLA."],
    )

    _r(
        register,
        "D11-T003",
        "Cache-aside",
        "cache-aside",
        "Cache-aside (lazy loading) lets the application read the cache first; on miss it loads the origin and populates the cache itself.",
        [
            "The cache is not authoritative; the database is. The app owns consistency between them on writes (delete or update cache after DB commit).",
            "Reads: GET cache, on miss SELECT DB, SET cache. Writes: usually update DB then invalidate cache key.",
            "This pattern is the default in microservices because it keeps cache logic in the service that knows the schema.",
        ],
        [
            "Race: thread A misses, thread B updates DB and deletes cache, thread A writes stale value — mitigated by version stamps or short TTL.",
            "Populate on miss only; no automatic write-through unless you add it.",
            "Serialization format (JSON, protobuf) is part of the contract at the cache boundary.",
        ],
        mermaid_cache_aside(),
        "Classic cache-aside read path with explicit populate on miss.",
        ["Wikipedia uses CDN and origin; cache-aside is the same division of responsibility at app scale."],
        "examples/d11_t003_cache_aside.py",
        """def load_user(redis, db, uid):
    k = f"user:{uid}"
    v = redis.get(k)
    if v: return v
    row = db.get_user(uid)
    if not row: return None
    redis.setex(k, 600, serialize(row))
    return row""",
        ["Write-through confused with cache-aside.", "Caching before DB commit on write path."],
        ["Stale user after update: missing cache delete.", "Thundering herd on cold key: see stampede topic."],
        ["What is cache-aside?", "Who populates the cache?", "Where do writes go first?", "How do you invalidate?", "Why is DB still source of truth?"],
        ["How handle miss stampede?", "Cache null results?", "Transaction ordering with invalidation?", "Versioned keys?", "Idempotent populate?"],
        ["Compare read-through library.", "Cache-aside with CDC invalidation.", "Multi-region cache-aside.", "Consistency windows.", "Testing races."],
        ["Profile shows stale email after change.", "Double DB load on hot key.", "Cache never fills.", "Intermittent wrong avatar.", "Write succeeded, read old."],
        ["Read-through difference?", "Link to penetration?", "Write-behind contrast?"],
        "Implement cache-aside for `order:{id}` with delete on update.",
        "Stale data after PUT: diagram the race and fix.",
        "Cache-aside vs read-through for a third-party pricing API.",
        "Invalidate in same request after DB commit; use transaction outbox if async.",
        "Use version field in key or delete key in update handler before response.",
        "Read-through if a shared library should own populate; cache-aside if service-specific SQL.",
        ["App loads cache on miss.", "Invalidate on write.", "DB is authoritative."],
        [("Cache-aside writes?", "Update DB then delete cache key.")],
        "`D11-T004` read/write-through, `D11-T007` invalidation.",
        "Read-through versus cache-aside.",
        "`D11-T008` stampede, `D07-T013` transactions.",
        ["Implement read miss path.", "Explain stale read race.", "Choose aside vs read-through."],
    )

    # T004-T025 continue with topic-specific mermaid/code where important
    specs = [
        (
            "D11-T004",
            "Read-through and write-through",
            "read-through and write-through",
            "Read-through delegates cache population to a cache layer on miss; write-through updates cache and database synchronously on writes.",
            """flowchart TD
  app[App]
  layer[CacheLayer]
  db[DB]
  app --> layer
  layer -->|miss_load| db
  layer -->|write| db
  layer -->|write| cacheStore[Cache]""",
            "The cache layer sits between app and DB for coordinated read/write.",
            "def get(k):\n  return cache_layer.get(k, loader=lambda: db.load(k))",
            ["Write-behind mistaken for write-through.", "Assuming read-through fixes invalidation without TTL."],
            ["What is read-through?", "What is write-through?", "Who calls the database?", "Latency on write?", "Consistency on write-through?"],
        ),
        (
            "D11-T005",
            "Write-behind and write-around",
            "write-behind and write-around",
            "Write-behind buffers writes in cache and flushes asynchronously; write-around skips cache on write so reads miss until populated.",
            """flowchart LR
  writeReq[Write]
  cacheBuf[CacheBuffer]
  dbAsync[DBAsyncFlush]
  writeReq --> cacheBuf
  cacheBuf --> dbAsync""",
            "Write-behind decouples write acknowledgment from durable DB write.",
            "queue.put(event); async_worker.flush_to_db()",
            ["Data loss if cache dies before flush.", "Write-around causing read misses after every write."],
        ),
        (
            "D11-T006",
            "TTL and expiration",
            "TTL and expiration",
            "TTL bounds staleness and memory; Redis expires keys lazily on access and actively via periodic sampling.",
            """flowchart TD
  key[CacheKey]
  ttl[TTLSeconds]
  expire[ActiveAndLazyExpiry]
  key --> ttl
  ttl --> expire""",
            "Expiration reclaims memory and limits stale reads.",
            "redis.setex('session:1', 1800, payload)",
            ["Assuming TTL replaces invalidation for strongly consistent data.", "Identical TTL on millions of keys causing avalanche."],
        ),
        (
            "D11-T007",
            "Cache invalidation",
            "cache invalidation",
            "Invalidation removes or updates cache entries when origin data changes; it is the hard part of caching.",
            """flowchart TD
  write[DBWrite]
  inv[InvalidateKeyOrTag]
  cache[Redis]
  write --> inv
  inv --> cache""",
            "Invalidation must align with transaction commit order.",
            "redis.delete(f'product:{id}')",
            ["Deleting cache before DB commit exposes missing data.", "Tag invalidation without tracking membership."],
        ),
        (
            "D11-T008",
            "Cache stampede",
            "cache stampede",
            "Stampede (thundering herd) is many concurrent misses on the same key reloading origin at once, often when TTL expires together.",
            """flowchart TD
  many[ConcurrentRequests]
  miss[CacheMiss]
  db[DatabaseOverload]
  many --> miss
  miss --> db""",
            "Mitigations: single-flight lock, early refresh, jittered TTL.",
            "if redis.set(lock_key, '1', nx=True, ex=5): load_and_set()",
            ["Only increasing TTL without jitter.", "Distributed lock without safe release."],
        ),
        (
            "D11-T009",
            "Cache penetration",
            "cache penetration",
            "Penetration is repeated requests for keys that do not exist in origin, bypassing cache benefit and hammering the DB.",
            """flowchart TD
  badKey[InvalidId]
  cache[Redis]
  db[DB]
  badKey --> cache
  cache -->|miss| db
  db -->|null| cache""",
            "Use short TTL null caching, validation, or bloom filter ahead of DB.",
            "if not exists_in_bloom(id): return 404",
            ["Caching null forever.", "No input validation on ids."],
        ),
        (
            "D11-T010",
            "Cache avalanche",
            "cache avalanche",
            "Avalanche is mass expiry or Redis outage causing simultaneous misses that overwhelm origin.",
            """flowchart TD
  expireWave[ManyKeysExpire]
  missStorm[MissStorm]
  origin[OriginOverload]
  expireWave --> missStorm
  missStorm --> origin""",
            "Stagger TTL, multi-level cache, circuit breakers, warm caches.",
            "ttl = base + random.randint(0, jitter)",
            ["Same TTL for all keys.", "No degrade path when Redis down."],
        ),
        (
            "D11-T011",
            "Hot keys and key design",
            "hot keys and key design",
            "Hot keys concentrate traffic on one Redis slot or CPU; key design namespaces entities and avoids unbounded cardinality.",
            """flowchart TD
  hotKey[SingleHotKey]
  shard[LocalSplitOrReplica]
  hotKey --> shard""",
            "Split hot keys or use local caching for extreme skew.",
            'key = f"app:{tenant}:user:{uid}:profile"',
            ["Tiny key cardinality with huge values.", "GLOBAL counter key for viral event."],
        ),
        (
            "D11-T012",
            "Redis strings, hashes, lists, sets, sorted sets",
            "Redis data types",
            "Redis types trade memory, access patterns, and atomic ops: strings for blobs, hashes for objects, lists for queues, sets for uniqueness, sorted sets for ranking.",
            mermaid_redis_types(),
            "Pick the type that matches access and update granularity.",
            "redis.hset('user:1', mapping={'name':'a'}); redis.zadd('board', {member: score})",
            ["Storing JSON string when hash fields update independently.", "Using lists for membership tests."],
        ),
        (
            "D11-T013",
            "Redis Streams",
            "Redis Streams",
            "Streams are append-only logs with consumer groups for at-least-once processing, unlike fire-and-forget Pub/Sub.",
            """flowchart LR
  prod[Producer]
  stream[Stream]
  group[ConsumerGroup]
  prod --> stream
  stream --> group""",
            "Use XADD, XREADGROUP, ACK for work queues with persistence.",
            "redis.xadd('events', {'type':'order'})",
            ["Using Pub/Sub when you need replay.", "Unbounded stream without trimming."],
        ),
        (
            "D11-T014",
            "Pub/Sub",
            "Redis Pub/Sub",
            "Pub/Sub delivers messages to online subscribers with no persistence; subscribers miss messages while disconnected.",
            """flowchart TD
  pub[Publisher]
  chan[Channel]
  sub1[SubscriberA]
  sub2[SubscriberB]
  pub --> chan
  chan --> sub1
  chan --> sub2""",
            "Good for live notifications, not job processing.",
            "redis.publish('notifications', payload)",
            ["Using Pub/Sub as a task queue.", "No back-pressure handling."],
        ),
        (
            "D11-T015",
            "Persistence: RDB and AOF",
            "RDB and AOF persistence",
            "RDB snapshots point-in-time; AOF logs every write for finer recovery at higher disk cost; both can be combined.",
            """flowchart TD
  mem[InMemoryDataset]
  rdb[RDBSnapshot]
  aof[AOFLog]
  mem --> rdb
  mem --> aof""",
            "Cache use cases may disable persistence; locks and queues may not.",
            "# save 900 1  # RDB; appendonly yes  # AOF",
            ["Assuming Redis persistence equals DB durability.", "RDB-only with 15-minute gap acceptable for locks."],
        ),
        (
            "D11-T016",
            "Eviction policies",
            "eviction policies",
            "When maxmemory is hit, Redis evicts per policy: allkeys-lru, volatile-lru, ttl, etc.",
            """flowchart TD
  full[MaxMemoryReached]
  policy[EvictionPolicy]
  drop[KeysRemoved]
  full --> policy
  policy --> drop""",
            "allkeys-lru is common for cache; volatile-* respects TTL keys only.",
            "# maxmemory-policy allkeys-lru",
            ["No maxmemory on cache cluster.", "Evicting keys that back rate limits silently."],
        ),
        (
            "D11-T017",
            "Redis transactions and Lua scripts",
            "Redis Lua scripts",
            "MULTI/EXEC batches commands but is not a full transaction across failures; Lua runs atomically on the server for compare-and-set patterns.",
            """flowchart TD
  client[Client]
  lua[LuaScript]
  redis[RedisSingleThread]
  client --> lua
  lua --> redis""",
            "Prefer Lua for rate limits, locks, conditional updates.",
            "redis.eval(script, numkeys, *args)",
            ["Believing MULTI prevents races with other clients.", "Long Lua blocks Redis."],
        ),
        (
            "D11-T018",
            "Distributed locks and their limitations",
            "distributed locks",
            "Redis locks with SET NX PX and token unlock are common but fail under clock skew, long GC pauses, and master failover without fencing tokens.",
            """flowchart TD
  clientA[ClientA]
  clientB[ClientB]
  lockKey[LockKey]
  clientA -->|acquire| lockKey
  clientB -->|blocked| lockKey""",
            "Redlock is debated; use DB advisory locks or lease-aware resources when correctness is critical.",
            'SET lock:job token NX PX 30000',
            ["Unlock without token check.", "No TTL on lock."],
        ),
        (
            "D11-T019",
            "Rate limiting with Redis",
            "Redis rate limiting",
            "Token bucket and fixed window counters in Redis protect origin and enforce quotas per key.",
            """flowchart TD
  req[Request]
  counter[RedisCounter]
  allow[AllowOrDeny]
  req --> counter
  counter --> allow""",
            "Atomic INCR with EXPIRE is simple; sliding window is smoother.",
            "count = redis.incr(key); if count == 1: redis.expire(key, window)",
            ["Non-atomic incr/expire race.", "Per-IP limit without IPv6 aggregation."],
        ),
        (
            "D11-T020",
            "Sliding-window counters",
            "sliding window rate limits",
            "Sliding windows count events in the last T seconds using sorted sets or approximate Redis Cell modules for smooth limits.",
            """flowchart TD
  now[NowTimestamp]
  window[WindowStart]
  zset[ZSETScores]
  now --> window
  window --> zset""",
            "Lua keeps ZREMRANGEBYSCORE + ZADD atomic.",
            "-- see sliding-window.lua in rate-limiter project",
            ["Fixed window burst at boundary.", "Storing every request forever without trim."],
        ),
        (
            "D11-T021",
            "Leaderboards and ranking",
            "Redis leaderboards",
            "Sorted sets provide O(log N) score updates and range queries for ranks.",
            """flowchart TD
  scoreUpdate[ScoreUpdate]
  zset[LeaderboardZSET]
  rankQuery[RankQuery]
  scoreUpdate --> zset
  zset --> rankQuery""",
            "Use ZINCRBY for incremental games; tie-break with lex ordering if needed.",
            "redis.zincrby('season:1', 10, 'player:42')",
            ["Global zset too large to shard.", "Using keys per page without top-K cache."],
        ),
        (
            "D11-T022",
            "Redis replication and Sentinel",
            "Redis Sentinel",
            "Replication copies data from master to replicas; Sentinel monitors and promotes a new master on failure.",
            mermaid_sentinel(),
            "Sentinel gives HA for single-shard Redis, not horizontal scale.",
            "# sentinel monitor mymaster 127.0.0.1 6379 2",
            ["Writing to replica by mistake.", "Split brain during network partition."],
        ),
        (
            "D11-T023",
            "Redis Cluster",
            "Redis Cluster",
            "Cluster shards keys into hash slots across masters; clients follow MOVED/ASK redirects.",
            mermaid_cluster(),
            "Use Cluster for scale-out; multi-key ops must share slot or use hash tags.",
            "CLUSTER KEYSLOT mykey",
            ["CROSSSLOT errors on multi-key transactions.", "Hot slot overload."],
        ),
        (
            "D11-T024",
            "Cache consistency with a primary database",
            "cache and DB consistency",
            "Consistency strategies include TTL, write-invalidate, versioned reads, and CDC-driven eviction.",
            """flowchart TD
  dbWrite[PrimaryWrite]
  binlog[CDCOrOutbox]
  cacheInv[CacheInvalidate]
  dbWrite --> binlog
  binlog --> cacheInv""",
            "Pick per-entity tolerance: strong for inventory, eventual for views.",
            "delete_cache_after_commit(product_id)",
            ["Read-your-writes violated across pods.", "Invalidation lag from async CDC."],
        ),
        (
            "D11-T025",
            "When not to use caching",
            "when not to cache",
            "Skip caching when data is always unique, strongly consistent without budget, tiny cheap queries, or compliance forbids retention.",
            """flowchart TD
  req[Request]
  decision{CacheHelps}
  skip[QueryOrigin]
  use[UseCache]
  req --> decision
  decision -->|no| skip
  decision -->|yes| use""",
            "Caching wrong data increases cost and incident surface.",
            "if highly_dynamic: return db.query()",
            ["Caching PII without TTL policy.", "Caching errors and timeouts."],
        ),
    ]

    for item in specs:
        if len(item) == 8:
            tid, title, theme, overview_tail, mermaid, cap, code, mistakes = item
            bq = [f"What is {title.lower()}?", f"Why does {theme} matter?", "What can go wrong?", "What metric shows success?", "What is the origin of truth?"]
        else:
            continue
        # extended tuples include extra mistake line only - handle full tuple
        pass

    # Manual loop for specs with full data
    full_specs = [
        ("D11-T004", "Read-through and write-through", "read-through and write-through", "Read-through puts miss handling inside a cache component; write-through writes cache and DB together.", specs[0][4], specs[0][5], specs[0][6], specs[0][7], specs[0][8] if len(specs[0]) > 8 else []),
    ]

    def extend(tid, title, theme, ot, mer, cap, code, mis, bq, iq, aq, sq, fq, sup, conf, comb, rev, fl):
        _r(
            register,
            tid,
            title,
            theme,
            ot,
            [f"{title} balances who owns population and durability.", "Origin remains authoritative unless write-through contract says otherwise.", "Latency and consistency trade off on the write path."],
            ["Sequence diagrams should show cache layer versus app responsibilities.", "Failures on write-through must define rollback or retry.", "Metrics on write latency to cache and DB separately."],
            mer,
            cap,
            [f"Example: product service using {theme} for catalog reads."],
            f"examples/{tid.lower().replace('-', '_')}.py",
            code,
            mis,
            [f"Symptom tied to {theme}: check ordering and TTL."],
            bq,
            iq,
            aq,
            sq,
            fq,
            f"Implement {theme} for a single entity with tests for miss and write.",
            f"Debug stale read after update for {title}.",
            f"Choose pattern for high-write social feed versus read-heavy catalog.",
            "See section F and integration tests.",
            "Invalidate or version keys; verify commit order.",
            "High-write: write-around or short TTL; catalog: cache-aside with longer TTL.",
            rev,
            fl,
            sup,
            conf,
            comb,
            [f"Explain {title} with diagram.", "Name failure mode.", "Pick pattern for scenario."],
        )

    # Register T004-T025 using extend helper
    data = [
        ("D11-T004", "Read-through and write-through", "read-through and write-through", "Read-through centralizes miss loading; write-through synchronously updates cache and database on writes.", specs[0][4], specs[0][5], specs[0][6], list(specs[0][7]) + ["Treating cache layer as ORM without schema versioning."], specs[0][8], ["Difference read-through vs cache-aside?", "Write latency impact?", "Failure if cache up DB down?", "Read-your-writes?", "Eviction effect?"], ["When use write-through?", "Library vs custom?", "Transactional outbox?", "Multi-region?", "Bulk writes?"], ["Dual-write problem.", "Cache coherence protocol.", "Hibernate second-level cache.", "Stale on partial failure.", "Testing write-through."], ["Stale catalog after price update.", "Write timeout doubled.", "Cache and DB disagree.", "Rolling deploy mismatch.", "Read-through loop."], ["Write-behind?", "Invalidation link?", "D11-T003 relation?"], "`D11-T005` write-behind", "write-through vs write-behind", "`D07-T013` transactions", ["Draw read-through.", "Explain write-through latency."], [("Read-through populator?", "Cache layer on miss.")]),
        ("D11-T005", "Write-behind and write-around", "write-behind", specs[1][3], specs[1][4], specs[1][5], specs[1][6], list(specs[1][7]) + ["No durability SLA on buffered writes."], ["What is write-behind?", "What is write-around?", "Durability risk?", "Read after write?", "Flush strategy?"], ["Batching vs latency?", "Crash recovery?", "Ordering guarantees?", "When write-around?", "Queue backpressure?"], ["Exactly-once flush.", "Idempotent consumers.", "Conflict resolution.", "Hybrid patterns.", "Audit trail."], ["Lost updates after crash.", "Read stale after write-around.", "Queue lag alert.", "Duplicate flush.", "Partial batch failure."], ["Write-through contrast?", "Streams for buffer?", "CDC instead?"], "`D11-T006` TTL", "write-through vs write-behind", "`D14-T008` message queues", ["Explain durability risk.", "When write-around."], [("Write-around reads?", "Miss until repopulated.")]),
        ("D11-T006", "TTL and expiration", "TTL", specs[2][3], specs[2][4], specs[2][5], specs[2][6], list(specs[2][7]), ["What is TTL?", "Lazy vs active expiry?", "PTTL vs TTL?", "Session TTL?", "TTL vs invalidation?"], ["Jitter why?", "Per-key TTL strategy?", "Redis expires when?", "TTL on negative cache?", "Clock skew?"], ["TTL for compliance.", "Sliding session.", "Hybrid TTL+version.", "Cron refresh.", "TTL in cluster."], ["Midnight latency spike.", "Keys never expire.", "Memory leak.", "Wrong unit seconds/ms.", "TTL -1 meaning."], ["Invalidation?", "Avalanche link?", "HTTP Cache-Control?"], "`D11-T007` invalidation", "TTL vs explicit delete", "`D06-T014` HTTP caching", ["Explain lazy expiry.", "Add jitter."], [("volatile keys?", "Keys with TTL set.")]),
        ("D11-T007", "Cache invalidation", "cache invalidation", specs[3][3], specs[3][4], specs[3][5], specs[3][6], list(specs[3][7]), ["Why hardest problem?", "Delete vs update cache?", "Tag invalidation?", "After commit?", "Event-driven invalidation?"], ["Race read stale?", "CDC lag?", "Bulk invalidation?", "Version keys?", "Two-level cache?"], ["Transactional messaging.", "Cache aside write.", "Read repair.", "Probabilistic early expiration.", "Invalidation storms."], ["User sees old data.", "Ghost data after delete.", "Partial tag purge.", "Invalidation faster than write.", "Cross-service stale."], ["Stampede?", "Consistency topic?", "Pub/Sub use?"], "`D11-T008` stampede", "invalidate vs update", "`D14-T003` events", ["Order invalidation vs commit.", "Tag design."], [("Delete when?", "After DB commit succeeds.")]),
        ("D11-T008", "Cache stampede", "cache stampede", specs[4][3], specs[4][4], specs[4][5], specs[4][6], list(specs[4][7]), ["What is stampede?", "Thundering herd?", "Single-flight?", "Lock with TTL?", "Early expiration?"], ["Mutex per key?", "Probabilistic refresh?", "Request coalescing?", "Semaphore on miss?", "Hot key link?"], ["Redisson singleflight.", "Jittered TTL math.", "Stale-while-revalidate.", "CDN parallel.", "Load shed on miss."], ["DB spike every hour.", "One key melts DB.", "Lock never released.", "Dogpile on deploy.", "Cache empty restart."], ["Penetration difference?", "Avalanche difference?", "Lock topic?"], "`D11-T009` penetration", "stampede vs avalanche", "`D11-T018` locks", ["List three mitigations.", "Draw herd timeline."], [("Single-flight?", "One loader per key.")]),
        ("D11-T009", "Cache penetration", "cache penetration", specs[5][3], specs[5][4], specs[5][5], specs[5][6], list(specs[5][7]), ["What is penetration?", "Null caching?", "Bloom filter?", "Input validation?", "Short TTL null?"], ["Bloom false positive?", "Cache attacker?", "UUID guessing?", "WAF vs cache?", "Negative cache size?"], ["Bloom in front of Redis.", "Rate limit scanners.", "Honeypot keys.", "GraphQL batch abuse.", "Shard bloom per tenant."], ["DB QPS from bots.", "Redis full of nulls.", "404 storm.", "Random ids.", "Cache useless."], ["Breakdown vs penetration?", "Avalanche?", "Security?"], "`D11-T010` avalanche", "penetration vs breakdown", "`D12-T018` abuse", ["Bloom + null TTL.", "Validate ids early."], [("Null cache TTL?", "Short, not infinite.")]),
        ("D11-T010", "Cache avalanche", "cache avalanche", specs[6][3], specs[6][4], specs[6][5], specs[6][6], list(specs[6][7]), ["What is avalanche?", "Vs stampede?", "Redis down?", "TTL alignment?", "Circuit breaker?"], ["Jitter formula?", "Multi-level cache?", "Warm on deploy?", "Hystrix degrade?", "Replication lag?"], ["Graceful degrade HTML.", "Read replica for miss.", "Separate cache cluster.", "Freeze TTL in incident.", "Auto scale origin."], ["Redis cluster failover miss storm.", "All keys 3600s TTL.", "Cold region launch.", "Eviction + miss.", "DB timeout cascade."], ["Stampede single key?", "Penetration?", "Sentinel failover?"], "`D11-T011` hot keys", "avalanche vs stampede", "`D05-T024` degradation", ["Jitter TTL.", "Degrade plan."], [("Circuit breaker on miss?", "Protect origin when cache sick.")]),
        ("D11-T011", "Hot keys and key design", "hot keys", specs[7][3], specs[7][4], specs[7][5], specs[7][6], list(specs[7][7]), ["What is hot key?", "Key naming?", "Hash tags?", "Local cache for hot?", "Split key pattern?"], ["Monitor hot keys?", "Cluster hot slot?", "Counter sharding?", "Read replica for hot?", "CDN for hot object?"], ["Consistent hashing client.", "Random suffix counters.", "Write combining.", "Micro-sharding.", "Rate limit hot key."], ["Single key 1M QPS.", "CPU one node high.", "CROSSSLOT.", "Big key slow.", "Wrong tenant prefix."], ["Cluster?", "Leaderboard hot?", "Rate limit?"], "`D11-T012` types", "hot key vs big key", "`D11-T023` cluster", ["Name key schema.", "Mitigate viral counter."], [("Hash tag?", "Force keys same slot {tenant}.")]),
        ("D11-T012", "Redis strings, hashes, lists, sets, sorted sets", "Redis data types", specs[8][3], specs[8][4], specs[8][5], specs[8][6], list(specs[8][7]), ["String use?", "Hash vs string JSON?", "List use?", "Set use?", "ZSET use?"], ["Memory encoding?", "HGETALL cost?", "List as queue?", "ZSET rank complexity?", "Stream vs list?"], ["HyperLogLog sketch.", "Bitmap ops.", "GEO types.", "JSON module.", "Module types."], ["Huge HGETALL.", "Wrong type command.", "List unbounded.", "ZSET hot member.", "KEYS * in prod."], ["Streams?", "Pub/Sub?", "Transactions?"], "`D11-T013` streams", "list vs stream", "`D11-T021` leaderboards", ["Pick type for session.", "ZSET leaderboard API."], [("ZSET score tie?", "Lex tie-breaker.")]),
        ("D11-T013", "Redis Streams", "Redis Streams", specs[9][3], specs[9][4], specs[9][5], specs[9][6], list(specs[9][7]), ["Stream vs Pub/Sub?", "Consumer group?", "XREADGROUP?", "ACK meaning?", "Retention?"], ["Pending entries?", "Claim idle?", "Partition stream?", "Ordering?", "MAXLEN ~?"], ["Exactly-once myth.", "DLQ pattern.", "Trim strategy.", "Fan-out groups.", "Backpressure."], ["Messages lost disconnect.", "PEL growth.", "Duplicate processing.", "Unbounded stream.", "Slow consumer."], ["Pub/Sub?", "Kafka compare?", "Jobs?"], "`D11-T014` Pub/Sub", "streams vs pubsub", "`D14-T008` queues", ["Design consumer group.", "Handle pending."], [("XAUTOCLAIM?", "Reassign idle messages.")]),
        ("D11-T014", "Pub/Sub", "Redis Pub/Sub", specs[10][3], specs[10][4], specs[10][5], specs[10][6], list(specs[10][7]), ["Pub/Sub delivery?", "Persistence?", "Pattern subscribe?", "Use cases?", "Scale limits?"], ["Missed messages?", "Shard channels?", "Backpressure?", "SSE alternative?", "Invalidation use?"], ["Redis 7 sharded pubsub.", "Bridge to Kafka.", "Fan-out websockets.", "Presence.", "Cache invalidation bus."], ["Subscriber down data loss.", "Thundering notify.", "Huge payload.", "Channel explosion.", "Cross slot."], ["Streams?", "Invalidation?", "WebSockets?"], "`D11-T015` persistence", "pubsub vs stream", "`D04-T016` WebSockets", ["When pubsub OK.", "When not."], [("Offline subscriber?", "Messages not stored.")]),
        ("D11-T015", "Persistence: RDB and AOF", "RDB and AOF", specs[11][3], specs[11][4], specs[11][5], specs[11][6], list(specs[11][7]), ["RDB snapshot?", "AOF rewrite?", "fsync policy?", "Cache need persistence?", "Recovery steps?"], ["RDB fork latency?", "AOF size?", "Hybrid?", "Disaster RPO?", "Disk pressure?"], ["AOF everysec tradeoff.", "RDB for backup.", "Diskless replication.", "TLS.", "Cloud managed."], ["Lost locks on restart.", "AOF corrupt.", "Fork OOM.", "Wrong save config.", "Restore stale cache served as truth."], ["Eviction?", "Cluster failover?", "Backup compliance?"], "`D11-T016` eviction", "RDB vs AOF", "`D08-T020` backups", ["Pick persistence for cache vs queue.", "RPO/RTO."], [("everysec?", "Max 1s loss window.")]),
        ("D11-T016", "Eviction policies", "eviction policies", specs[12][3], specs[12][4], specs[12][5], specs[12][6], list(specs[12][7]), ["maxmemory?", "allkeys-lru?", "volatile-lru?", "noeviction?", "LFU vs LRU?"], ["Cache only TTL keys?", "Evict rate limit keys?", "Monitor evicted?", "Resize memory?", "Policy change live?"], ["TTL + eviction interplay.", "Hot key immune?", "Sample size config.", "Replica eviction.", "Module memory."], ["Sudden miss storm after evictions.", "noeviction OOM.", "Wrong policy.", "Big key evicted last.", "Latency spike."], ["TTL topic?", "Avalanche?", "Hot keys?"], "`D11-T017` Lua", "lru vs ttl", "`D11-T010` avalanche", ["Pick policy for pure cache.", "Alert on evictions."], [("noeviction?", "Writes fail when full.")]),
        ("D11-T017", "Redis transactions and Lua scripts", "Redis Lua", specs[13][3], specs[13][4], specs[13][5], specs[13][6], list(specs[13][7]), ["MULTI EXEC?", "Atomic Lua?", "WATCH?", "Script reload?", "Cluster Lua?"], ["Long script risk?", "KEYS in script?", "Replication atomic?", "EVALSHA?", "Error handling?"], ["Rate limit lua.", "Compare-and-swap.", "Lock release lua.", "Sliding window.", "Inventory decrement."], ["Script kills Redis.", "WATCH abort storm.", "CROSSSLOT script.", "Stale SHA.", "Partial multi."], ["Locks?", "Rate limit?", "Transactions ACID?"], "`D11-T018` locks", "MULTI vs Lua", "`D11-T019` rate limit", ["Write atomic incr+expire lua.", "Explain WATCH limit."], [("Lua atomicity?", "Whole script runs exclusively.")]),
        ("D11-T018", "Distributed locks and their limitations", "distributed locks", specs[14][3], specs[14][4], specs[14][5], specs[14][6], list(specs[14][7]), ["SET NX PX?", "Why token unlock?", "Redlock debate?", "Fence token?", "Lease vs lock?"], ["GC pause exceed TTL?", "Master failover duplicate?", "Clock skew?", "Lock renewal?", "DB advisory lock?"], ["Chandy-Lamport.", "Fencing tokens in DB.", "Lease with heartbeat.", "Zookeeper compare.", "Avoid lock when possible."], ["Double payment.", "Stale lock holder.", "Forgot unlock.", "Lock never acquired.", "Split brain write."], ["Lua unlock?", "Rate limit?", "Idempotency?"], "`D11-T019` rate limits", "lock vs semaphore", "`D07-T017` optimistic locking", ["Safe lock acquire/release.", "Failure if master dies."], [("Fence token?", "Storage rejects stale writer.")]),
        ("D11-T019", "Rate limiting with Redis", "Redis rate limiting", specs[15][3], specs[15][4], specs[15][5], specs[15][6], list(specs[15][7]), ["Why Redis?", "Fixed window?", "Token bucket?", "Per user key?", "429 response?"], ["INCR race?", "Global vs per IP?", "Burst allowance?", "Headers Retry-After?", "Sync across regions?"], ["Cell algorithm.", "GCRA.", "Sliding window lua.", "Gateway vs app limit.", "Cost-based limits."], ["Limit not enforced.", "Boundary burst.", "Redis down open gate.", "Hot limit key.", "IPv6 rotation."], ["Sliding window topic?", "Lua?", "API gateway?"], "`D11-T020` sliding window", "token vs leaky bucket", "`D06-T012` API limits", ["Implement fixed window.", "Choose 429 body."], [("INCR EXPIRE race?", "Use lua or SET NX window.")]),
        ("D11-T020", "Sliding-window counters", "sliding window rate limits", specs[16][3], specs[16][4], specs[16][5], specs[16][6], list(specs[16][7]), ["Why sliding?", "ZSET approach?", "Memory per user?", "Approximate sliding?", "Compare fixed window?"], ["Lua trim?", "Cluster slot?", "Precision vs cost?", "Multiple windows?", "Weighted costs?"], ["Redis Cell module.", "Hazelcast alternative.", "Edge rate limit.", "Coordinated omission.", "Admission control."], ["2x burst at boundary fixed.", "ZSET huge.", "Time sync.", "Duplicate member.", "Wrong window unit."], ["Token bucket?", "D11-T019?", "Gateway?"], "`D11-T021` leaderboards", "sliding vs fixed", "java rate-limiter project", ["Lua sliding window.", "Test boundary."], [("ZREMRANGEBYSCORE?", "Drop events outside window.")]),
        ("D11-T021", "Leaderboards and ranking", "Redis leaderboards", specs[17][3], specs[17][4], specs[17][5], specs[17][6], list(specs[17][7]), ["ZSET for rank?", "ZREVRANK?", "Tie break?", "Pagination?", "Season boards?"], ["Shard leaderboard?", "Update frequency?", "Anti-cheat?", "Archive season?", "Memory size?"], ["Lex zset.", "Top-K cache.", "Near real-time batch.", "Double score buckets.", "Geo boards."], ["Hot board key.", "Wrong rank page.", "Float score precision.", "Member deleted.", "CROSSSLOT multi board."], ["Sorted set types?", "Hot keys?", "Streams for events?"], "`D11-T022` Sentinel", "rank vs score query", "`D11-T012` zset", ["ZINCRBY + rank API.", "Paginate top 100."], [("ZREVRANGE?", "Fetch top N by score.")]),
        ("D11-T022", "Redis replication and Sentinel", "Redis Sentinel", specs[18][3], specs[18][4], specs[18][5], specs[18][6], list(specs[18][7]), ["Replication async?", "Sentinel role?", "Quorum?", "Split brain?", "Read from replica?"], ["Replica lag?", "Promotion steps?", "Client discovery?", "TLS replication?", "Multi DC?"], ["Diskless repl.", "Replica priority.", "Sentinel tilt?", "K8s operator.", "Managed Redis HA."], ["Write lost on failover.", "Stale read replica.", "Sentinel flapping.", "Wrong master.", "Brain split writes."], ["Cluster vs Sentinel?", "Persistence?", "Consistency?"], "`D11-T023` Cluster", "sentinel vs cluster", "`D13-T022` HA", ["Failover timeline.", "Read routing policy."], [("Quorum?", "Votes needed to fail over.")]),
        ("D11-T023", "Redis Cluster", "Redis Cluster", specs[19][3], specs[19][4], specs[19][5], specs[19][6], list(specs[19][7]), ["Hash slots?", "MOVED redirect?", "Multi key ops?", "Hash tag?", "Scale out?"], ["Resharding?", "Hot slot?", "Client library?", "Replica read?", "Cross AZ?"], ["Gossip protocol.", "Manual failover.", "Module cluster.", "Elasticache cluster mode.", "Redisson cluster."], ["CROSSSLOT error.", "Slot migration miss.", "ASK storm.", "Uneven slots.", "Big multi key."], ["Sentinel?", "Hot keys?", "Lua multi key?"], "`D11-T024` consistency", "cluster vs sentinel", "`D13-T021` sharding", ["Design hash tags.", "Handle MOVED."], [("16384 slots?", "Key maps to slot via CRC16.")]),
        ("D11-T024", "Cache consistency with a primary database", "cache and DB consistency", specs[20][3], specs[20][4], specs[20][5], specs[20][6], list(specs[20][7]), ["Strong vs eventual?", "Invalidate when?", "CDC?", "Read repair?", "Version column?"], ["Transactional outbox?", "Lag tolerance?", "Dual write?", "Session stickiness?", "CRDT?"], ["Debezium invalidate.", "Canal.", "Versioned cache entry.", "Sticky read your writes.", "Saga compensations."], ["User sees old balance.", "Inventory oversell.", "Ghost record.", "Delayed invalidation.", "Cross service cache."], ["When not cache?", "Invalidation?", "Transactions?"], "`D11-T025` when not cache", "cache vs DB truth", "`D07-T013` ACID", ["CDC invalidation diagram.", "SLA per entity."], [("Read-your-writes?", "Invalidate or route to primary.")]),
        ("D11-T025", "When not to use caching", "when not to cache", specs[21][3], specs[21][4], specs[21][5], specs[21][6], list(specs[21][7]), ["When skip cache?", "Unique queries?", "Compliance?", "Cheap SQL?", "Strong consistency?"], ["Cost of ops?", "Incident surface?", "Debug harder?", "Personal data?", "Metrics still?"], ["Materialized view instead.", "Read replica.", "Edge CDN only.", "Query optimize first.", "Autoscaling DB."], ["Cached wrong error.", "PII leak in Redis.", "Stale legal consent.", "Cache never hits.", "More latency added."], ["Start domain recap?", "Indexing first?", "Rate limit without cache?"], "none — capstone", "cache vs no cache", "`D07-T019` indexes first", ["List five anti-patterns.", "Decide cache for wallet balance."], [("Wallet balance?", "Often no cache or very short with invalidation.")]),
    ]

    for row in data:
        extend(*row)
