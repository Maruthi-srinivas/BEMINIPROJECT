"""Topic facts for NoSQL, Redis, concurrency stubs, and messaging gaps."""

from __future__ import annotations

from gap_facts_a import add

add(
    "D10-T004",
    "A wide-column store groups rows by a partition key and stores many columns or cells inside that partition, often sorted by a clustering key. Cassandra and Bigtable are the reference designs. Reads are fast when they hit one partition. A query that scans every partition is a distributed full scan. The data model is the query model.",
    ["Choose a partition key that matches the lookup", "Cluster columns in the order you will read", "Keep a partition from growing without bound", "Reject queries that would fan out to every node"],
    "a hot partition or a query that fans out because the WHERE clause is not the partition key",
    "partition size, p99 of the primary query, and fan-out count",
    "def partition_key(user_id):\n    return user_id  # queries must include this key\n",
    "A wide-column partition is one filing cabinet. The clustering key is the order of folders inside it. Asking every cabinet in the building is not a lookup.",
    "A timeline stored as user_id plus time stays on one partition and reads the latest page cheaply. Storing it by a random id makes the home timeline a scatter-gather.",
    "the access path is a known key and a range inside one partition",
    "you need ad hoc queries across many partitions",
    ["Using a timestamp alone as the partition key.", "Letting a partition grow forever.", "Adding a secondary index and expecting it to be as cheap as the primary key."],
)

add(
    "D10-T005",
    "A graph database stores entities as vertices and relationships as edges, and it is built to traverse them. The cost follows the size of the traversed neighborhood, not a join of whole tables. A super-node with millions of edges turns a 'friend of friend' query into a scan. Graphs are a poor fit for bulk columnar analytics.",
    ["Model nouns as vertices and relationships as edges", "Write the traversal you will actually run", "Bound depth and fan-out", "Treat super-nodes as a special case"],
    "a traversal that touches a super-node and times out, or using a graph to replace a simple key lookup",
    "vertices visited per query and latency of the deepest allowed traversal",
    "def friends_of_friends(graph, user, limit):\n    seen = set()\n    for friend in graph.neighbors(user):\n        for other in graph.neighbors(friend):\n            if len(seen) >= limit:\n                return seen\n            seen.add(other)\n    return seen\n",
    "A graph query is walking from person to person along named roads. It is fast until you reach the town square where every road meets.",
    "A permission system stores users, groups, and resources as a graph and traverses 'member of' edges. One group that contains every contractor becomes a super-node and the check gets slow.",
    "the product question is a relationship traversal of bounded depth",
    "the question is a key lookup or a large aggregation",
    ["Unlimited depth.", "No plan for super-nodes.", "Rebuilding a relational report as a graph because graphs sound flexible."],
)

add(
    "D10-T006",
    "Access-pattern modeling starts from the queries and writes the store must serve, then shapes keys, partitions, and indexes to those paths. A table that is elegant and does not match a query will be scanned. List the read and write rate of each path before you pick a database. Patterns that conflict, such as 'fetch by user' and 'fetch by time across users,' often need two layouts.",
    ["List each query and its rate", "Name the key that query has", "Design one layout per hot path", "Reject a design that cannot name the path"],
    "a single generic document shape that makes the hottest query a collection scan",
    "the fraction of requests served by a key lookup versus a scan",
    "PATHS = [\n    ('get_order', 'order_id', 'point'),\n    ('list_user_orders', 'user_id', 'partition'),\n]\n",
    "You build the shelves for the way people actually take boxes down, not for a taxonomy that looks neat in a diagram.",
    "An orders service reads by order id and lists by user id. One primary key cannot optimize both. A second table or a secondary index is an explicit choice with a write cost.",
    "you can name the hot queries",
    "you design a universal schema and hope indexes appear later",
    ["Starting from entities instead of queries.", "Ignoring write amplification of the second path.", "Load-testing only the point read."],
)

add(
    "D10-T007",
    "Denormalization copies data so a read can finish from one place. Embedding stores a child inside the parent document. Referencing stores an id and reads the child elsewhere, sometimes in a second query. Embedding wins when the child is small, owned by the parent, and read with it. Referencing wins when the child is large, shared, or updated on its own. The cost is stale copies and write amplification.",
    ["Ask whether the child is read with the parent", "Ask who updates the child", "Embed or reference based on those answers", "Define how a copied field is updated"],
    "an embedded array that grows without bound, or a referenced profile that is joined on every request and was the latency you tried to remove",
    "document size, extra reads per request, and stale-copy incidents",
    "def embed(child_count, shared):\n    return child_count < 100 and not shared\n",
    "Embedding is printing the author's name on every copy of a pamphlet. Referencing is printing a catalog number and keeping one author card.",
    "A comment thread embeds the last fifty comments in the post document so the page is one read. The user record stays referenced because the same user appears on many posts and changes their display name.",
    "one read must return the whole aggregate",
    "the embedded child is unbounded or shared and frequently updated",
    ["Embedding unbounded arrays.", "Denormalizing without a story for updates.", "Referencing everything and calling it normalized purity."],
)

add(
    "D10-T008",
    "A secondary index locates rows by an attribute that is not the primary key. In a distributed database it is either local to each partition, which makes writes cheaper and queries a scatter, or global, which makes the query one lookup and the write a distributed update. Secondary indexes lag in eventually consistent systems. They are not free on the write path.",
    ["Name the filter that is not the primary key", "Choose local or global", "Pay the write cost", "Know whether the index read is stale"],
    "a query that fans out to every local index, or a global index that fails and blocks the write",
    "write latency added by index maintenance, and fan-out of secondary lookups",
    "def index_write_cost(global_index, partitions):\n    return partitions if global_index else 1\n",
    "A secondary index is a second catalog by subject. Every new book must be filed twice. If each branch keeps its own subject catalog, a subject search visits every branch.",
    "Finding orders by email in a user-id partitioned store needs a secondary structure. A global index answers in one hop and makes every order write update another partition.",
    "a real query filters on a non-primary attribute",
    "you add indexes for hypothetical reports and slow the write path",
    ["Assuming a secondary index is as consistent as the base row.", "Building a global index without a write budget.", "Scanning because the index was local and nobody measured fan-out."],
)

add(
    "D10-T009",
    "A TTL expires an item after a duration. The store deletes it lazily or with a background process. Expiration is not a transaction. A read might still see an item around its deadline, and a delete might lag. TTL is for caches, sessions, and ephemeral events, not for legal retention. If the expiry must be exact, the application has to check a timestamp too.",
    ["Store the item with a deadline", "Reject or ignore it after the deadline on read", "Let the background delete reclaim space", "Do not use TTL as the only compliance control"],
    "a session that is still accepted after logout because expiry is lazy, or a disk fill because deletes cannot keep up",
    "expired-but-present reads, and the lag of the expiry worker",
    "import time\n\ndef alive(expires_at, now=None):\n    now = time.time() if now is None else now\n    return now < expires_at\n",
    "TTL is a carton of milk with a date. The store may not pull it off the shelf the second the clock hits midnight, so the buyer still has to read the date.",
    "A password-reset token lives for fifteen minutes. The row carries an expiry timestamp the checker enforces, and a TTL eventually deletes it. Logout of a session uses an explicit delete, not only a TTL.",
    "the data is allowed to disappear and a little lateness is acceptable",
    "you need a precise legal deletion time or an audit trail of the delete",
    ["Using TTL as a security revoke.", "Assuming deletion is immediate.", "Setting a TTL so long that the table is an unbounded log."],
)

add(
    "D10-T010",
    "A consistency model states what a read may return after writes. Strong consistency lets a read see the latest acknowledged write. Eventual consistency lets replicas disagree for a while. Causal consistency preserves the order of related operations. The model is a contract with anomalies, not a slogan. Choose it per operation, because a payment and a page view do not need the same contract.",
    ["Name the anomaly the user can tolerate", "Pick a model that forbids the ones they cannot", "Read from a leader when you need the latest write", "Measure staleness instead of hoping"],
    "reading a replica and telling a user their write failed because the read missed it",
    "stale-read rate and user-visible lost updates",
    "def read_from_leader(need_latest):\n    return need_latest\n",
    "Consistency is the promise about which version of a document you are allowed to be handed. Eventual means the clerks compare notes later. Strong means they check the latest page first.",
    "A profile edit must be read-your-writes for the author, so that read hits the primary. A product view can be seconds stale. Using one model for both either overpays or loses edits.",
    "you can say which anomalies are unacceptable",
    "you call the database 'consistent' without naming an anomaly",
    ["Equating replication with strong consistency.", "Using quorum reads everywhere by habit.", "Ignoring the client's own retry."],
)

add(
    "D10-T012",
    "Replication copies data so a node can fail or serve reads. Sharding splits data so no single node holds everything. Replication does not add write capacity on a single-leader system. Sharding does, and it forces a partition key. Resharding moves data. A shard that is also unreplicated is one disk away from data loss.",
    ["Replicate first if the goal is surviving a node failure", "Shard when one node cannot hold or write the data", "Pick a key that spreads load", "Plan how a key moves"],
    "a hot shard, or a replica set of one that people called highly available",
    "bytes and QPS per shard, and whether every shard has a replica",
    "def shard_for(key, n):\n    return hash(key) % n\n",
    "Replication is carbon copies. Sharding is tearing the phone book into volumes. Copies help when a volume burns. Volumes help when one book is too heavy. They solve different problems.",
    "A MongoDB replica set keeps a primary and secondaries. When the working set no longer fits one primary, the collection is sharded by a high-cardinality key and each shard is itself a replica set.",
    "you are separating failure tolerance from capacity",
    "you shard a dataset that fits on one machine and then pay scatter-gather forever",
    ["Sharding without replication.", "Using a monotonically increasing shard key.", "Assuming replicas increase write throughput on a single primary."],
)

add(
    "D10-T014",
    "Eventual consistency means that if writes stop, replicas converge to the same value. It does not say when, and it does not say what a read returns before that. Conflicts need a rule: last write wins, a merge function, or an application repair. Clients observe stale reads, and sometimes two different values. It is a good trade for high availability during a partition if the data can merge.",
    ["Accept a write on a reachable replica", "Replicate it asynchronously", "Detect a conflict", "Merge with a stated rule"],
    "last-write-wins dropping a slower but more important update, such as a stock decrement",
    "replica divergence time and lost-update count",
    "def last_write_wins(a, b):\n    return a if a['ts'] >= b['ts'] else b\n",
    "Eventual consistency is two notebooks that get compared at the end of the day. Until then, they disagree. The comparison rule decides which pencil mark survives.",
    "A shopping cart can merge line items. A bank balance cannot use last-write-wins. The cart is a candidate for eventual consistency. The balance is not.",
    "the data has a merge rule and availability beats freshness",
    "the operation is a decrement or a unique constraint you cannot reconcile after the fact",
    ["Using eventual consistency for payments.", "Having no conflict rule.", "Describing a bug as 'eventual' when the replicas never converge."],
)

add(
    "D10-T015",
    "MongoDB indexes are B-trees on fields or compound keys. The query uses an index when the predicate matches a prefix of the compound key. Aggregation pipelines transform documents through stages such as match, group, sort, and lookup. An early match uses an index. A lookup is a join and can be expensive. Explain shows whether a stage is a collection scan.",
    ["Match on an index prefix first", "Sort only in an order the index supports or budget the memory sort", "Group after the set is small", "Read the explain plan"],
    "a pipeline that lookups a large collection before it filters, or a compound index whose field order does not match the query",
    "documents examined versus returned, and aggregation memory spills",
    "db.orders.createIndex({ userId: 1, createdAt: -1 })\n",
    "A compound index is a phone book sorted by city and then by name. You can find a city, or a city plus a name. You cannot jump straight to a name in every city.",
    "A feed query matches userId and sorts by createdAt, so the index is that pair. An aggregation that unwinds a huge array before matching scans the collection and spills.",
    "you have a MongoDB predicate or pipeline to justify",
    "you add an index per field and never look at explain",
    ["Leading the index with a low-selectivity field the query does not equality-match.", "Using $lookup as a habit.", "Allowing disk spills to hide a bad stage order."],
    lang="javascript",
)

add(
    "D10-T016",
    "A MongoDB multi-document transaction lets several reads and writes commit or abort together on a replica set. It is not free the way a single-document write is. Single-document writes are already atomic. Transactions need a replica set, have a lifetime limit, and can abort on conflicts. If the data is modeled so one document is the aggregate, you often do not need a transaction.",
    ["Prefer one document when the invariant fits", "Start a transaction only for a real multi-document invariant", "Keep it short", "Retry transient aborts"],
    "a long transaction that times out, or using a transaction to paper over a data model that should have been one document",
    "transaction abort rate and duration",
    "session.startTransaction()\n// unexecuted: several writes, then commit, retry on transient error\n",
    "A single document write is one sealed envelope. A multi-document transaction is a rubber band around several envelopes, and the rubber band has a timer.",
    "Transferring credits between two account documents needs a transaction or an application outbox. Updating fields inside one order document does not.",
    "an invariant really spans documents",
    "you wrap every write in a transaction by default",
    ["Holding a transaction open across a user action.", "Ignoring TransientTransactionError retries.", "Assuming multi-document transactions exist on a standalone node."],
    lang="javascript",
)

add(
    "D10-T019",
    "Choosing a database starts from the access pattern, the consistency need, the size, and the operational skills you have. A relational database is the default when queries are ad hoc and invariants are transactional. A key-value or wide-column store fits a known primary-key path at high throughput. A search engine fits text queries. A cache is not a database. One system can use more than one store if the boundary is explicit.",
    ["Write the queries and the invariants", "Eliminate stores that cannot express them", "Cost the operations", "Pick the store the team can run"],
    "choosing a specialized store for a workload that is ordinary SQL, or the reverse, forcing a join-shaped workload onto a key-value store",
    "whether the primary query is a point read, a transaction, or a search, and the on-call burden",
    "def pick(ad_hoc_sql, search, known_key):\n    if search:\n        return 'search index'\n    if ad_hoc_sql:\n        return 'relational'\n    if known_key:\n        return 'key-value or wide-column'\n    return 'write the query first'\n",
    "Picking a database is picking a vehicle after you know the cargo and the roads, not before.",
    "Orders with payments and ad hoc support queries belong in PostgreSQL. Session tokens belong in Redis. Product text search belongs in a search index fed by the database, not instead of it.",
    "the query and the failure mode are written down",
    "the choice is fashionable or already on someone's résumé",
    ["Using the cache as the system of record.", "Introducing a second database for one query without an ownership story.", "Ignoring operational cost."],
)

add(
    "D11-T003",
    "Cache-aside means the application reads the cache first and, on a miss, reads the database and writes the cache. The database is the source of truth. The cache is filled by readers. A write updates the database and then deletes or updates the cache. The race is a reader refilling the cache with stale data after a writer has deleted it.",
    ["Look up the key", "On a miss, read the database", "Fill the cache", "On a write, update the database and invalidate the key"],
    "a stale fill that overwrites a newer invalidation, so the cache serves old data until TTL",
    "hit ratio and stale-read incidents after writes",
    "def cache_aside_get(cache, db, key):\n    value = cache.get(key)\n    if value is None:\n        value = db.get(key)\n        cache.set(key, value, ttl=60)\n    return value\n",
    "Cache-aside is checking your pocket notebook and, if the page is blank, copying it from the official ledger and keeping the copy for a minute.",
    "A product page reads Redis, falls back to PostgreSQL, and stores the JSON for 60 seconds. An update deletes the key. A TTL caps how long a lost delete can linger.",
    "reads dominate and the database remains the source of truth",
    "you write only to the cache and call it cache-aside",
    ["No TTL.", "Updating the cache before the database commit.", "Ignoring the stale-fill race."],
)

add(
    "D11-T004",
    "Read-through loads a missing key inside the cache layer, which calls the database itself. Write-through writes the cache and the database together before acknowledging. The application talks to the cache as if it were the store. Write-through favors consistency over write latency. Read-through favors a simpler application read path. Both still need a failure policy when the database is down.",
    ["Application calls the cache", "The cache loads or stores through to the database", "Acknowledge only after the policy's durability step", "Define the outage behavior"],
    "write-through latency equal to the database on every write, or a read-through loader that stampedes",
    "fraction of reads served from memory and write latency added by the database round trip",
    "def write_through(cache, db, key, value):\n    db.put(key, value)\n    cache.set(key, value)\n",
    "Read-through is a librarian who fetches the archive copy when the shelf is empty. Write-through is refusing to say the book is filed until both the shelf and the archive are updated.",
    "A managed cache in front of a user-profile table uses read-through so every service shares one loader. Write-through is used for a setting that must not acknowledge until the database commit returns.",
    "you want one loading policy shared by all callers",
    "the write path cannot afford to wait for the database and you still call it write-through",
    ["Acknowledging a write-through before the database commit.", "A loader with no single-flight.", "Hiding database errors behind a cache hit of stale data without saying so."],
)

add(
    "D11-T005",
    "Write-behind acknowledges the write in the cache and flushes to the database later. Write-around writes only to the database and leaves the cache to be filled by a later read, which avoids polluting the cache with data nobody reads. Write-behind can lose acknowledged writes if the cache dies before the flush. Write-around makes the next read cold on purpose.",
    ["Classify the write as flush-later or bypass", "If write-behind, queue the flush durably enough for your promise", "If write-around, invalidate stale cache entries", "Bound the flush lag"],
    "a crashed cache that held acknowledged write-behind data which never reached the database",
    "flush lag and data loss on a cache restart",
    "def write_around(db, cache, key, value):\n    db.put(key, value)\n    cache.delete(key)\n",
    "Write-behind is taking a customer's order on a notepad and filing it in the ledger later. If the notepad burns, the order is gone. Write-around is filing only in the ledger and not cluttering the counter.",
    "Counters that can be rebuilt may use write-behind. A payment must not. Bulk imports that will not be read soon use write-around so they do not evict the hot catalog.",
    "you have explicitly chosen to risk or to bypass the cache",
    "you need the acknowledgment to mean the database has the write",
    ["Write-behind for payments.", "An unbounded flush queue.", "Write-around that forgets to invalidate an old cached value."],
)

add(
    "D11-T006",
    "A TTL on a cache entry deletes or ignores it after a duration. It bounds staleness when an invalidation is lost. It does not make the entry correct. A short TTL raises the miss rate and the database load. A long TTL lengthens the stale window. Jitter stops every key from expiring on the same second.",
    ["Set a TTL that matches the allowed staleness", "Add jitter", "Still invalidate on writes when correctness needs it", "Size the database for the miss rate at expiry"],
    "every key expiring together and stampeding the database, or a TTL so long that users see yesterday's price",
    "miss rate at expiry time and the age of the oldest served value",
    "import random\n\ndef ttl_with_jitter(base):\n    return base + random.randint(0, base // 10)\n",
    "TTL is an expiry date on a photocopy. Jitter is not putting the same date on every photocopy, so the crowd does not arrive at the archive together.",
    "Feature-flag snapshots live 30 seconds with jitter. A price change also deletes the key. The TTL is the backstop, not the only correctness tool.",
    "you need a bound on staleness even if a delete is lost",
    "you set a one-hour TTL on a permission decision",
    ["Synchronized expiry.", "TTL without invalidation for data that changed.", "A TTL of zero that turns the cache into a hop."],
)

add(
    "D11-T007",
    "Cache invalidation removes or replaces an entry when the source of truth changes. Delete-on-write is the usual cache-aside policy. Update-on-write stores the new value. The hard parts are knowing every key that contains the changed fact, doing the delete after the database commit, and the race where a reader refills a stale value. Versioned keys make the old key harmless.",
    ["Commit the database write", "Delete or version every derived key", "Let readers refill", "Keep a TTL so a missed delete expires"],
    "forgetting a derived key, so one page stays stale, or deleting before the commit so a reader refills the old row",
    "stale reads after a write, counted by comparing cache generation to database generation",
    "def invalidate(cache, keys):\n    for key in keys:\n        cache.delete(key)\n",
    "Invalidation is recalling every photocopy of a page. If you forget the photocopy in the branch office, that office keeps lying.",
    "Changing a product price must delete the product key, the category page key, and the search snippet key. Missing the snippet is the bug customers notice.",
    "a write changes a fact that has been copied into a cache",
    "you cannot name the keys that contain the fact",
    ["Invalidating before commit.", "Naming only the primary key.", "Assuming a delete is visible on every cache node instantly."],
)

add(
    "D11-T008",
    "A cache stampede is many requests missing the same key and all loading the database at once. It happens on expiry, on deploy, or on a cold key that is suddenly hot. Single-flight lets one request load and the others wait. A lock with a short timeout, early refresh, and jitter are the usual controls. The database must still survive one loader.",
    ["Detect a miss", "Elect one loader", "Others wait or serve stale", "Fill the key and release the waiters"],
    "a lock that expires before the load finishes, so several loaders run anyway, or waiters that pile up past the client deadline",
    "database QPS on a single key at expiry, and loader count",
    "import threading\nlocks = {}\n\ndef single_flight(key, loader):\n    lock = locks.setdefault(key, threading.Lock())\n    with lock:\n        return loader()\n",
    "A stampede is every customer asking the same clerk to fetch the same box at the opening bell. Single-flight is one customer fetching it while the others wait at the counter.",
    "A celebrity profile expires and ten thousand requests hit the user service. A single-flight lock plus a slightly stale serve keeps the database at one query.",
    "one key is hot and expensive to rebuild",
    "you add a lock per key for data that is cheap and cold",
    ["A lock TTL shorter than the query.", "No stale-while-revalidate.", "Stampeding on startup by warming nothing."],
)

add(
    "D11-T009",
    "Cache penetration is a stream of requests for keys that do not exist, so every request misses and hits the database. An attacker or a buggy client can do this on purpose. Caching a short-lived negative result, validating the key shape, and rate-limiting unknown keys close the hole. A bloom filter can reject keys the system has never stored, with false positives that only cause an extra lookup.",
    ["Validate the key", "Check a negative cache or filter", "Rate-limit repeated misses", "Load the database only for plausible keys"],
    "a database overloaded by random ids that were never going to hit",
    "miss rate on keys that do not exist, and database QPS from those misses",
    "def allow_lookup(key, negative_cache):\n    if not key.isalnum():\n        return False\n    if negative_cache.get(key):\n        return False\n    return True\n",
    "Penetration is people asking for books the library has never owned, and each question still sending a runner to the archive.",
    "A public GET /products/{id} that accepts any string is used to spray random ids. The service rejects malformed ids, caches 'missing' for 30 seconds, and rate-limits the rest.",
    "untrusted callers can request arbitrary keys",
    "you cache every negative forever and pin memory",
    ["No validation.", "A negative cache with no TTL.", "Treating penetration as an ordinary miss storm."],
)

add(
    "D11-T010",
    "A cache avalanche is a large fraction of keys expiring or a cache node dying at the same time, so the database receives the full read load. It differs from a stampede, which is one key. Prevention is jittered TTLs, replicated cache, multiple shards, and a database that can absorb a partial loss. Serving stale data for a short time is a deliberate degradation.",
    ["Spread expiry times", "Replicate or shard the cache", "Shed or serve stale when the cache is gone", "Capacity-plan the database for a cache loss"],
    "a cold restart of the only cache cluster taking the database down with it",
    "database QPS when cache hit ratio drops, and the fraction of keys sharing one TTL",
    "def db_load(read_qps, hit_ratio):\n    return read_qps * (1 - hit_ratio)\n",
    "An avalanche is every photocopy in the building expiring at noon, not one popular page.",
    "A Redis cluster restart with no jitter and no stale-serve sends the entire product catalog at the primary database. The database's connection limit is hit and writes fail too.",
    "many keys can disappear together",
    "you run a single cache node and no degradation plan",
    ["Identical TTLs.", "No cache replica.", "Assuming the database 'has headroom' without a number."],
)

add(
    "D11-T011",
    "A hot key is one key whose traffic does not fit on a single cache shard's CPU or network. Key design decides which data shares a slot. Prefixes that map to one shard, huge values, and a single global counter are the usual causes. Replicas of the hot key, local in-process caches, and splitting the key into partitions spread the load. The key must still be invalidatable.",
    ["Measure QPS per key", "Avoid a key that every request needs", "Split or replicate the hot key", "Keep an invalidation path for every copy"],
    "one Redis shard at 100 percent CPU while the others are idle",
    "QPS and bytes per key, and CPU of the hottest shard",
    "def split_counter(user_id, buckets=16):\n    return f'likes:{user_id}:{hash(user_id) % buckets}'\n",
    "A hot key is one hook that everyone hangs their coat on until the hook snaps. Extra hooks only help if people use different ones.",
    "A global 'site-config' key is read on every request and pins one shard. An in-process cache with a one-second TTL takes that read off Redis. A per-user feed key is fine until one celebrity is on it.",
    "one key or one shard is hotter than the rest",
    "you split keys and then cannot invalidate all the pieces",
    ["A single global counter on one key.", "A multi-megabyte value.", "Hash tags that force a whole tenant onto one slot."],
)

add(
    "D11-T012",
    "Redis strings hold bytes, numbers, and bitfields. Hashes hold field maps and fit an object with many small attributes. Lists are ordered linked sequences. Sets are unique unordered members. Sorted sets are members with a score, ordered by that score. The type decides the commands and the cost. A list used as a random-access array is the wrong type.",
    ["Pick the type that matches the operation", "Know the cost of that command", "Bound the collection size", "Avoid a command that is O(n) on a hot key"],
    "LRANGE or SMEMBERS on a million-member key blocking the server",
    "command latency and collection cardinality",
    "HSET user:1 name ada\nZADD leaderboard 10 user:1\n",
    "A string is one labeled jar. A hash is a tray of small jars. A sorted set is a ranked list. You do not pour out a million-name list on every request.",
    "A user profile stored as a hash lets you update one field. A leaderboard stored as a sorted set answers top ten. A list of every historical event in one key becomes a blocking read.",
    "the operation matches a Redis type's cheap command",
    "you need a query language or a value larger than a request should wait for",
    ["One giant list.", "Using KEYS in production.", "Storing JSON in a string and updating it with a lost-update race."],
    lang="text",
)

add(
    "D11-T013",
    "Redis Streams is an append-only log of entries with ids. Consumer groups track which entries each consumer has pending. Acknowledgments remove an entry from the pending list. Unacked entries can be reclaimed if a consumer dies. Streams are not a durable multi-datacenter bus by themselves. The stream can be trimmed, which drops history.",
    ["Append an entry", "Read it in a consumer group", "Process it", "Acknowledge it or let another consumer claim it"],
    "trimming a stream before consumers acknowledge, or leaving pending entries forever after a crash",
    "pending-entry age and stream length",
    "XADD jobs * type email\nXREADGROUP GROUP g1 c1 COUNT 10 STREAMS jobs >\n",
    "A stream is a notebook of jobs. A consumer group is a set of workers with bookmarks. An acknowledgment is crossing a job off. If you tear out pages, the bookmark may point at nothing.",
    "A single-node background job channel uses a stream and a consumer group. A crashed worker's pending jobs are claimed after a timeout. The design is wrong if the job must survive the loss of that Redis node without AOF or a replica.",
    "you want a log and competing consumers inside Redis",
    "you need a durable cross-cluster event bus",
    ["No claim of pending entries.", "Trimming too aggressively.", "Assuming a stream replaces Kafka's retention and replication."],
    lang="text",
)

add(
    "D11-T014",
    "Redis Pub/Sub delivers a message to subscribers that are connected at that moment. It does not store the message. A subscriber that is down misses it. There is no acknowledgment. It fits ephemeral signals such as 'invalidate this key' to live processes. It does not fit a job queue.",
    ["Publish a message", "Deliver it only to current subscribers", "Accept that offline subscribers miss it", "Use a stream or a queue if you needed storage"],
    "using Pub/Sub as a job queue and losing every message published during a deploy",
    "subscriber count and messages published while a subscriber was disconnected",
    "PUBLISH cache-invalidate product:42\n",
    "Pub/Sub is a loudspeaker in a room. People who stepped out do not hear the announcement, and nobody writes it down.",
    "Each API node subscribes to an invalidation channel and drops its local cache entry. A node that restarts loads fresh data on the next request. The channel is not the order pipeline.",
    "every listener that cares is connected, and loss is acceptable",
    "the message is work that must be done at least once",
    ["Persisting business events only in Pub/Sub.", "Expecting a backlog.", "No other path for a missed invalidation besides TTL."],
    lang="text",
)

add(
    "D11-T015",
    "RDB is a point-in-time snapshot of Redis. AOF logs every write and can fsync on a timer or every command. Snapshots are compact and lose the writes after the last snapshot. AOF loses less and replays more slowly. Neither is a substitute for a replica if the machine is gone and the file was only local. Restart time includes loading the snapshot or replaying the log.",
    ["Choose a loss window", "Snapshot, append, or both", "Put the file on a disk that survives the process", "Measure restart time"],
    "an AOF policy of 'every second' that still loses a second of acknowledged writes, or a restart that takes longer than the outage budget",
    "seconds of data loss in a kill test, and time to load the dataset",
    "# unexecuted policy sketch\n# appendfsync everysec loses up to about one second of writes\n",
    "RDB is a photograph. AOF is a receipt tape. A photograph is quicker to look at and misses everything after the flash. The tape is longer to reread and misses less.",
    "A cache that can be rebuilt may use a rare snapshot or none. A Redis that holds a job stream needs AOF and a replica, and the team must have timed a restart.",
    "you have decided Redis holds data you cannot simply recompute",
    "you enable AOF and believe a single disk is high availability",
    ["No persistence and no rebuild path.", "Never testing a restart.", "Fsync every command on a hot cache that did not need it."],
    lang="text",
)

add(
    "D11-T016",
    "An eviction policy decides which key to remove when Redis reaches maxmemory. noeviction returns errors on writes. allkeys-lru removes the least recently used key among all keys. volatile-ttl removes keys that have a TTL. A policy that only evicts volatile keys will fill memory if most keys have no TTL. Eviction is not expiration. Expiration follows a TTL. Eviction follows pressure.",
    ["Set maxmemory", "Choose a policy that matches which keys may disappear", "Give TTLs to data that is allowed to vanish", "Alert before memory is full"],
    "evicting a key the application treated as durable, or refusing writes because the policy is noeviction and memory is full",
    "evicted key count and used memory versus maxmemory",
    "def may_evict(has_ttl, policy):\n    if policy == 'noeviction':\n        return False\n    if policy.startswith('volatile'):\n        return has_ttl\n    return True\n",
    "Eviction is throwing out boxes when the closet is full. Expiration is throwing out a box on the date written on it, even if the closet has room.",
    "A cache uses allkeys-lru and every key is disposable. A Redis that also stores a lock or a queue must not use a policy that can evict that key, or the lock and the queue must live in another instance.",
    "the instance is a cache with a memory cap",
    "you store durable jobs and a cache in one instance with eviction on",
    ["No maxmemory.", "Evicting keys that have no rebuild path.", "Confusing TTL deletes with memory eviction."],
)

add(
    "D11-T017",
    "A Redis transaction with MULTI/EXEC queues commands and runs them without another client interleaved. It is not a rollback journal. A command can still fail and the rest still run. WATCH provides optimistic concurrency: if the watched key changes, EXEC aborts. A Lua script runs atomically on the server and can branch. Scripts must be short because they block the single thread.",
    ["Watch the keys you decided on", "Queue the updates or run a short script", "Abort if a watched key changed", "Keep the script off the network and off unbounded loops"],
    "a Lua script that loops over a huge set and stalls every other command, or assuming MULTI rolls back",
    "script duration and EXEC abort rate",
    "local cur = tonumber(redis.call('GET', KEYS[1]) or '0')\nif cur >= tonumber(ARGV[1]) then return 0 end\nredis.call('INCR', KEYS[1])\nreturn 1\n",
    "MULTI is a stack of sticky notes the clerk applies without serving anyone else, but a bad note does not undo the earlier notes. Lua is handing the clerk one small card to follow without interruption.",
    "A rate-limit check-and-increment is a Lua script so two clients cannot both read under the limit and both increment. A script that scans a million-member set blocks the node.",
    "the invariant is a few keys and a few commands",
    "you need a multi-key transaction across shards, which a single script does not give you",
    ["Long scripts.", "Expecting rollback.", "Forgetting WATCH and losing an update."],
    lang="lua",
)

add(
    "D11-T018",
    "A distributed lock using Redis usually sets a key with a unique token and an expiry so a crashed holder does not keep the lock forever. The holder must only delete the key if the token still matches, typically in a script. Expiry can release the lock while the holder is still working. Redlock across several nodes is an attempt to reduce that window and is still not a consensus system. The resource needs fencing if two holders would corrupt data.",
    ["Set the key only if absent, with a token and a TTL", "Do the work for less time than the TTL or renew carefully", "Delete only if the token matches", "Fence the protected resource"],
    "two workers both acting because the lock expired before the work finished",
    "lock TTL versus work duration, and double-execution count",
    "if redis.call('get', KEYS[1]) == ARGV[1] then\n  return redis.call('del', KEYS[1])\nend\nreturn 0\n",
    "A Redis lock is a coat-check ticket that expires. If you are still wearing the coat when the ticket expires, the clerk may hand the same hook to someone else.",
    "A job worker sets lock:job:42 with a 30-second TTL. The job takes two minutes. Another worker starts the job at second 31. A database fence token stops the late worker from committing.",
    "you need to reduce duplicate work and you have a fence on the real resource",
    "you treat a single Redis lock as a proof that two writers cannot commit",
    ["No token on delete.", "TTL shorter than the work.", "No fencing token on the database write."],
    lang="lua",
)

add(
    "D11-T019",
    "Rate limiting with Redis counts actions per key in a window using INCR and a TTL, a token bucket in a hash, or a sorted set of timestamps. The script must do the check and the update atomically. The limiter fails open or closed when Redis is down, and that choice is a product decision. Limits are per user, token, or IP, and a NAT can make many users share an IP.",
    ["Name the subject and the limit", "Update the counter atomically", "Reject when the count exceeds the limit", "Decide fail-open or fail-closed"],
    "a non-atomic read and increment that lets a burst through, or a limit keyed only by IP behind a carrier NAT",
    "rejected request rate and Redis errors treated as allow or deny",
    "local n = redis.call('INCR', KEYS[1])\nif n == 1 then redis.call('PEXPIRE', KEYS[1], ARGV[1]) end\nreturn n\n",
    "A rate limiter is a turnstile that counts people per minute. If two attendants both glance at the counter before either clicks it, extra people slip through.",
    "A public API increments rl:token:{id} inside a Lua script and returns 429 when the count passes 100 per second. If Redis is unreachable, the gateway fails open for reads and closed for writes.",
    "you need a shared count across many API nodes",
    "you count only inside one process and call it global",
    ["GET then INCR as two round trips.", "No TTL so the key lives forever.", "One limit for all customers."],
    lang="lua",
)

add(
    "D11-T020",
    "A sliding-window counter estimates how many events fell in the last T seconds by weighting the previous fixed window and the current one, or by storing each event's timestamp in a sorted set and dropping those older than T. The sorted-set version is exact and costs memory per event. The weighted-counter version is small and approximate. Both beat a fixed window's boundary burst, where a client sends twice the limit around the reset.",
    ["Define the window length", "Drop or discount events older than the window", "Count what remains", "Reject when the count exceeds the limit"],
    "a fixed window that allows two bursts back to back at the boundary, or a sorted set that stores every request and fills memory",
    "allowed bursts at the window boundary, and memory per limited key",
    "def weighted(prev, curr, elapsed, window):\n    return prev * (1 - elapsed / window) + curr\n",
    "A fixed window is a counter that resets every minute, so a rude guest spends the whole allowance at 0:59 and again at 1:00. A sliding window keeps looking at the last sixty seconds only.",
    "An API that allowed 100 calls per clock minute saw 200 calls in two seconds around the minute mark. A sliding window of 60 seconds removes that seam.",
    "the burst at a fixed boundary is a real abuse or fairness problem",
    "a coarse fixed window is enough and the extra memory is not",
    ["Calling a fixed window sliding.", "Storing unbounded timestamps.", "Forgetting the approximation error of the weighted formula."],
)

add(
    "D11-T021",
    "A leaderboard maps a member to a score and asks for rank and the top of the range. Redis sorted sets do this with ZADD, ZREVRANGE, and ZREVRANK. Rank is the index in score order. Ties need a second key in the score or the member id so order is stable. A global sorted set is a hot key. Sharding by time or by cohort splits the heat and makes a true global rank a merge.",
    ["Update the member's score", "Query a bounded range from the top", "Define tie-breaking", "Split the key if one board is hot"],
    "a single global key so large or so hot that one shard stalls, or unstable ordering when scores tie",
    "sorted-set cardinality, top-query latency, and CPU of the shard that owns the board",
    "ZADD board 100 user:1\nZREVRANGE board 0 9 WITHSCORES\n",
    "A leaderboard is a ranked notice board. Asking for the top ten is easy. Asking for your exact rank in a billion names is a bigger piece of cardboard, and one nail may not hold it.",
    "A game stores daily scores in a sorted set per region per day. The global top ten merges a handful of regional tops. One worldwide key for every player update melts a shard.",
    "you need rank or top-k by a numeric score",
    "you need arbitrary filters, which is a query, not a sorted set",
    ["One key for the world.", "Unstable ties.", "ZRANGE of the entire set to the client."],
    lang="text",
)

add(
    "D11-T022",
    "Redis replication copies the primary's writes to replicas, asynchronously by default. A replica can serve stale reads. Sentinel watches nodes and starts a failover by promoting a replica when it decides the primary is unreachable. Failover can lose the writes the replica had not received. A quorum of Sentinels must agree so one unlucky network blip does not promote. Clients must learn the new primary.",
    ["Replicate writes asynchronously", "Let Sentinels observe the primary", "Promote only with quorum", "Point clients at the new primary"],
    "split brain or lost writes on failover, or clients still writing to the old primary",
    "replication offset lag and failover time in a drill",
    "def may_promote(sentinels_agreeing, quorum, lag_ok):\n    return sentinels_agreeing >= quorum and lag_ok\n",
    "Replication is an apprentice copying the ledger a few lines behind. Sentinel is a committee that hands the apprentice the official pen when the master disappears. Lines not yet copied are lost.",
    "A cache's replica set fails over with Sentinel and the application reconnects via the Sentinel endpoint. A rate-limit counter may go backward by the lost writes. A lock key may vanish. The design has to tolerate that.",
    "you need automatic failover of one Redis primary",
    "you need zero lost writes, which async replication does not promise",
    ["One Sentinel.", "Ignoring client rediscovery.", "Reading a replica and expecting the write you just acknowledged."],
)

add(
    "D11-T023",
    "Redis Cluster shards the keyspace into 16384 hash slots. A node owns a range of slots. Multi-key commands work only when every key is in the same slot, which hash tags force by hashing the substring inside braces. Resharding moves slots. During a move, a client may get an ASK or MOVED redirect. The cluster survives a minority of node failures only if replicas exist for the slots those nodes owned.",
    ["Hash the key to a slot", "Route to the node that owns it", "Keep multi-key commands inside one slot", "Move slots with replication still in place"],
    "a multi-key transaction across slots, or a hot slot because every key used the same hash tag",
    "keys per slot, redirect rate, and whether every slot has a replica",
    "def same_slot(a, b):\n    # hash tags: {user42}:a and {user42}:b share a slot\n    return '{user42}' in a and '{user42}' in b\n",
    "Cluster mode is 16384 pigeonholes and several mailboxes. A letter goes to the mailbox that owns its pigeonhole. Two letters are handled together only if they share a pigeonhole.",
    "A rate limiter that does INCR on one key is fine. A script that updates a user and a global counter crosses slots and fails. The global counter needs another design.",
    "the dataset or the write rate exceeds one Redis node",
    "you need frequent multi-key transactions across arbitrary keys",
    ["Hash tags that pin a tenant to one slot forever.", "No replicas.", "Assuming a Lua script can touch every node."],
)

add(
    "D11-T024",
    "Cache consistency with a primary database means a reader should not observe a value older than a write the system has acknowledged, within the policy you stated. The usual policy is cache-aside with delete-after-commit plus a TTL. Stronger policies version the row and store the version in the cache so an old fill cannot overwrite a new one. The cache is not in the database transaction unless you use a pattern that makes the database the only acknowledgment point.",
    ["Commit the database transaction", "Invalidate or version the cache entry", "Fill on read with the version check", "Bound residual staleness with a TTL"],
    "a cache entry newer in time but older in version that overwrites the fresh value",
    "reads that return a version older than the latest committed version",
    "def fill(cache, key, value, version):\n    current = cache.get_version(key)\n    if current is None or version >= current:\n        cache.set(key, value, version)\n",
    "Consistency is refusing to glue an older photocopy on top of a newer one. The version number is the edition printed on the page.",
    "An order status update commits in PostgreSQL, then deletes the Redis key. A concurrent reader may refill from a replica that has not caught up. Reading the fill from the primary, or storing the row version, closes that hole.",
    "the cache copies database state that users write",
    "you update the cache first and treat that as the commit",
    ["No version and no TTL.", "Filling from a lagged replica.", "Two writers with no order."],
)

add(
    "D11-T025",
    "A cache is the wrong tool when the data is rarely reread, must be strongly consistent on every read, is larger than memory, or is cheaper to compute than to store and invalidate. Caching adds staleness, invalidation, and an outage mode. A database with a good index may already meet the latency. Measure a miss path before you add a tier that can fail.",
    ["Measure read repetition and database latency", "Estimate invalidation difficulty", "Compare with an index or a query fix", "Add a cache only if the miss path still meets the SLO"],
    "a cache in front of a write-heavy, rarely reread admin page that is now stale and more complex",
    "hit ratio and the latency of the uncached query after an index",
    "def worth_caching(reads_per_write, db_ms, target_ms):\n    return reads_per_write > 10 and db_ms > target_ms\n",
    "A cache is a photocopy machine. It is a waste when you print each page once and then correct the original.",
    "An internal report run once an hour should be a SQL query or a materialized view, not a Redis key nobody knows how to invalidate. A product page read a thousand times a second is the opposite.",
    "the same read is hot and the source is too slow after a fair query plan",
    "the working set does not fit, the data is write-heavy, or correctness cannot tolerate staleness",
    ["Caching to avoid an index.", "No hit-ratio goal.", "A cache that can fail and no plan for the database load."],
)
