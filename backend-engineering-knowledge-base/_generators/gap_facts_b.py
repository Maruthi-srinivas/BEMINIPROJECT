"""Topic facts for networking and PostgreSQL gaps."""

from __future__ import annotations

from gap_facts_a import add, FACTS

add(
    "D04-T003",
    "A MAC address is a layer-2 identifier on a local network. ARP resolves an IPv4 address to a MAC address on that segment by broadcasting a request and caching the reply. The cache can be poisoned because classic ARP does not authenticate the reply. Switches learn MAC-to-port mappings from source addresses. ARP does not cross a router.",
    ["Need the MAC for an IP on the local subnet", "Broadcast an ARP request", "Cache the reply", "Send the frame to that MAC"],
    "ARP cache poisoning, or a stale entry after a failover that black-holes traffic until the cache expires",
    "ARP replies that do not match the expected host, and the age of the neighbor cache",
    "def same_subnet(ip, other, prefix):\n    return ip.split('.')[:prefix] == other.split('.')[:prefix]\n",
    "ARP is shouting in one room 'who has this name?' A person in another room behind a router never hears it.",
    "A virtual IP failover updates the MAC. Hosts with a stale ARP entry keep sending frames to the dead NIC until the entry times out.",
    "you are debugging local delivery or a failover on one L2 segment",
    "the path crosses a router, where ARP on the far side is a different cache",
    ["Treating a MAC address as a stable identity across networks.", "Trusting ARP replies.", "Flushing the cache as the only fix and not shortening the timeout during failover."],
)

add(
    "D04-T004",
    "TCP is a connection-oriented, reliable byte stream with ordering, retransmission, and flow control. UDP is a connectionless datagram protocol: each message is independent, and the network may drop, reorder, or duplicate it. UDP does less so that the application can choose its own reliability, as DNS and RTP do. TCP's stream has no message boundaries.",
    ["Decide whether loss must be repaired by the transport", "If yes, use TCP and frame your own messages", "If no, use UDP and handle loss in the application", "Measure loss and reordering rather than assuming the LAN is safe"],
    "writing a UDP protocol that assumes in-order delivery, or using TCP for a small request and paying a handshake on every call",
    "packet loss, reordering, and connection-setup time versus datagram loss rate",
    "def needs_tcp(must_not_lose: bool, has_app_retry: bool) -> bool:\n    return must_not_lose and not has_app_retry\n",
    "TCP is a signed-for courier that retries. UDP is dropping a postcard in the mail and accepting that it might vanish.",
    "DNS queries use UDP because a retry of a tiny idempotent query is cheaper than a connection. A database protocol uses TCP because a lost byte is corruption.",
    "you need a reliable ordered byte stream",
    "you need bounded latency and can tolerate loss, or the message is idempotent and small",
    ["Assuming TCP preserves message boundaries.", "Assuming UDP is faster without measuring.", "Building reliability on UDP by accident and poorly."],
)

add(
    "D04-T006",
    "TCP sequence numbers count bytes in each direction. An acknowledgment names the next byte the receiver has contiguously received. A gap means the sender must retransmit the missing range. Cumulative ACKs do not say which later bytes arrived. Selective acknowledgments fill that gap. Retransmission is triggered by timeout or by duplicate ACKs.",
    ["Assign a sequence to each byte", "Receiver ACKs the next contiguous byte", "Sender detects a gap", "Retransmit the missing bytes and adjust the window"],
    "a timeout that is shorter than the real RTT, causing spurious retransmission and collapse",
    "retransmission rate and RTT versus the retransmission timeout",
    "def next_expected(received):\n    # received is a set of contiguous bytes starting at 0\n    n = 0\n    while n in received:\n        n += 1\n    return n\n",
    "Sequence numbers are page numbers. The ACK says 'I have every page up to this one.' A missing page 4 is not fixed by also receiving page 5.",
    "A service behind a lossy path shows rising retransmits and flat goodput. The fix starts by comparing RTO to measured RTT, not by adding application retries on top.",
    "you are explaining reliability or a throughput collapse on TCP",
    "you are on UDP, which has none of this machinery",
    ["Retrying the whole RPC because one segment was lost, without idempotency.", "Ignoring SACK and assuming every loss waits for a timeout.", "Treating sequence numbers as packet counts."],
)

add(
    "D04-T007",
    "Flow control is the receiver telling the sender how much buffer remains, via the window. Congestion control is the sender estimating the network's capacity and backing off on loss or delay. They are different windows. The send rate follows the minimum of the two. Slow start probes upward. Congestion avoidance grows more slowly. A loss is treated as a congestion signal by classic algorithms.",
    ["Advertise the receive window", "Grow the congestion window while the path is clean", "Cut the congestion window on loss or rising delay", "Pace sends at the minimum of the two windows"],
    "a large receive window on a lossy path, so the sender overruns the network and goodput falls",
    "congestion window, retransmits, and goodput versus offered load",
    "def send_window(receive_window, congestion_window):\n    return min(receive_window, congestion_window)\n",
    "Flow control is the listener saying 'I can hold three more sentences.' Congestion control is noticing the hallway is crowded and speaking less.",
    "A bulk export saturates a link and starves latency-sensitive calls that share it. Congestion control on the bulk flow, or a separate queue, is the lever. Raising the socket buffer alone is not.",
    "you are explaining why throughput flattened or why latency spiked under load",
    "the bottleneck is application lock time, which no window will fix",
    ["Equating the two windows.", "Disabling congestion control to 'go faster.'", "Adding parallel connections until the path collapses."],
)

add(
    "D04-T009",
    "HTTP/1.1 is a text protocol with one response in flight per connection unless pipelines are used, and pipelines stall on a slow response. HTTP/2 multiplexes streams on one connection and compresses headers, but it can block a connection on a lost TCP packet. HTTP/3 runs the same stream model over QUIC on UDP, so one lost packet stalls one stream rather than every stream. Semantics of methods and status codes stay shared. The version changes framing and head-of-line behavior.",
    ["Pick a version the path actually allows", "Reuse connections", "Watch which stream a loss stalls", "Fall back when a middlebox breaks the newer version"],
    "head-of-line blocking on HTTP/2 over a lossy TCP path, or assuming a proxy speaks HTTP/3 because the origin does",
    "stream concurrency, connection count, and tail latency under packet loss",
    "def stalled_streams(version, loss_on_connection):\n    if not loss_on_connection:\n        return 0\n    return 1 if version == 'h3' else 'all-on-connection'\n",
    "HTTP/1.1 is one conversation per phone line. HTTP/2 is several conversations on one line where a garbled sentence stalls all of them. HTTP/3 gives each conversation its own recovery.",
    "A browser to a CDN benefits from HTTP/2 or HTTP/3. A service mesh that hairpins HTTP/2 through a single TCP connection can couple unrelated requests when that connection loses a packet.",
    "you are choosing a framing version for many concurrent requests",
    "you have one request per connection and no header repetition, where the version is not the bottleneck",
    ["Assuming HTTP/2 is always lower latency.", "Pipelining HTTP/1.1 without testing proxies.", "Forgetting middleboxes when enabling HTTP/3."],
)

add(
    "D04-T010",
    "HTTP methods name intent. GET and HEAD are safe and idempotent. PUT and DELETE are idempotent. POST is not. Headers carry metadata such as content type, caching, and authentication. Status codes are the contract: 2xx success, 3xx redirection, 4xx the client's request is wrong, 5xx the server failed. A 404 is not a 500. A 409 says the state conflicts. Clients and caches treat the method and status as instructions, not as decoration.",
    ["Choose the method that matches retry and cache behavior", "Send the headers a cache or a client must obey", "Return a status that names whose fault it is", "Document which errors are retryable"],
    "a POST retried by a proxy, creating a second charge, or a 200 returned for an error payload",
    "the ratio of 4xx to 5xx, and duplicate side effects after a retry",
    "def retryable(method, status):\n    if method == 'POST':\n        return False\n    return status in (502, 503, 504)\n",
    "The method is the verb on a form. The status code is the clerk's stamp. A smile on the form does not mean the stamp said approved.",
    "An API that returns 200 with an error JSON trains clients to ignore status and breaks caches. A payment POST without an idempotency key doubles charges when the client retries on a timeout.",
    "you are defining an HTTP contract",
    "you overload POST for every action and then cannot use caches or safe retries",
    ["Returning 200 for failures.", "Retrying POST blindly.", "Using 500 for validation errors."],
)

add(
    "D04-T011",
    "HTTP caching is defined by method, status, and headers such as Cache-Control, ETag, and Last-Modified. Freshness lets a cache serve without contacting the origin until max-age passes. Validation sends If-None-Match and may receive 304. Shared caches must not store responses with Authorization unless the response explicitly says they can. GET is cacheable. POST is not, by default.",
    ["Mark the response with an explicit freshness lifetime", "Send a validator such as an ETag", "Bypass the cache for authorized private responses unless you opt in", "Revalidate when freshness ends"],
    "a shared cache storing a response that includes one user's data, or a client caching an error",
    "cache hit ratio and the number of private responses stored in a shared cache",
    "def cache_control(private, max_age):\n    scope = 'private' if private else 'public'\n    return f'{scope}, max-age={max_age}'\n",
    "A cache is a photocopy with an expiry date. The ETag is the edition number you quote when asking if the original changed.",
    "A CDN caches a public product image for an hour. It must not cache a GET /account response that varies by cookie unless Vary and private are set correctly.",
    "the representation is the same for many callers and tolerates a bounded age",
    "the response is unique per user or must be current to the second",
    ["Caching Set-Cookie responses in a shared cache.", "Omitting Vary when the body depends on a header.", "Using a query string as a cache-buster and then wondering why the origin melts."],
)

add(
    "D04-T012",
    "DNS resolution walks from a stub resolver to a recursive resolver, which queries the root, the TLD, and the authoritative server unless a cache hits. Record types include A and AAAA for addresses, CNAME for an alias, NS for delegation, MX for mail, and TXT for arbitrary text used by verification. TTL is the cache lifetime. A CNAME chain adds latency and a failure point.",
    ["Check the recursive cache", "Follow delegations from the root if needed", "Return the record and its TTL", "Honor TTL instead of caching forever"],
    "a long TTL on a record you need to fail over, or a CNAME to a name that is itself a CNAME in a loop",
    "resolver latency and the time a changed record still returns the old address",
    "def cache_until(now, ttl):\n    return now + ttl\n",
    "DNS is a chain of directories. Each clerk can answer from a photocopy until the photocopy's TTL expires.",
    "A failover that updates an A record still leaves clients on the old IP until the previous TTL expires. Health-checked load balancers move traffic faster than DNS alone.",
    "you are naming a service or explaining a failover delay",
    "you need instant drain of one task, which DNS TTL will not do",
    ["Setting TTL to a day and expecting a one-minute failover.", "Breaking a CNAME at the zone apex where the DNS spec forbids it.", "Caching NXDOMAIN for too long."],
)

add(
    "D04-T013",
    "A TLS handshake authenticates the server and agrees on session keys. The client offers versions and cipher suites. The server sends a certificate chain. The client checks the chain, the name, and the expiry. Modern TLS 1.3 does this in one round trip after the ClientHello, then both sides derive traffic keys. Session resumption avoids a full handshake. The handshake is not the bulk encryption. It sets it up.",
    ["ClientHello with supported parameters", "Server certificate and key share", "Client verifies the certificate and the hostname", "Both sides derive traffic keys and switch to encrypted records"],
    "accepting a certificate for the wrong hostname, or an old TLS version a middlebox downgrades you into",
    "handshake failures by alert code, and the fraction of resumed sessions",
    "def hostname_ok(cert_names, host):\n    return host in cert_names\n",
    "The handshake is exchanging badges and agreeing on a code phrase before you speak in that code. The badge check is the certificate verification.",
    "A service that disables certificate verification to 'fix' a hostname mismatch is accepting any impostor. The fix is the right name on the certificate or the right name in the client config.",
    "you are explaining why a connection is authenticated",
    "you turn verification off to silence an error",
    ["Skipping hostname checks.", "Leaving TLS 1.0 enabled.", "Assuming a private network does not need authentication."],
)

add(
    "D04-T014",
    "A certificate binds a public key to a name, signed by an issuer. A certificate authority is an issuer that verifiers have chosen to trust, often through a chain ending at a root in the trust store. The private key stays with the subject and signs or decrypts. The public key is in the certificate and verifies. Revocation and short lifetimes limit the damage of a stolen key. A self-signed certificate is trusted only if you installed it deliberately.",
    ["Subject proves possession of the private key", "Issuer signs the certificate", "Verifier walks the chain to a trusted root", "Verifier checks name, time, and revocation or lifetime"],
    "trusting a self-signed certificate you did not pin, or a chain that is valid for a different name",
    "days to expiry and handshake failures after a rotation",
    "def chain_ends_at_root(issuers, roots):\n    return issuers[-1] in roots\n",
    "A certificate is a sealed letter of introduction. The CA is the official whose seal you already trust. The private key is the pen that only the owner should hold.",
    "A Kubernetes ingress certificate that expires on a Saturday takes every public API down. Alerting on days-to-expiry is the operational half of the cryptography.",
    "you are issuing or verifying identity for TLS or code signing",
    "you copy a private key into a repo or a ticket",
    ["Committing private keys.", "Adding a broad private CA to every trust store.", "Ignoring expiry because the chain was valid last month."],
)

add(
    "D04-T015",
    "Symmetric encryption uses one shared key to encrypt and decrypt. It is fast and is what protects bulk TLS records. Asymmetric encryption uses a key pair. The public key can be distributed. The private key cannot. Asymmetric algorithms authenticate and exchange a symmetric session key because they are too slow and too large for bulk data. Hashing is neither. It does not encrypt.",
    ["Use asymmetric cryptography to agree on identity and a session key", "Use a symmetric key for the payload", "Rotate the session key", "Keep the private key off the wire"],
    "encrypting a large payload with RSA, or calling a hash an encryption scheme",
    "handshake CPU versus record CPU, and where private keys are stored",
    "def uses_symmetric_for_bulk(nbytes):\n    return nbytes > 0\n",
    "Symmetric crypto is a shared padlock key. Asymmetric crypto is a padlock that anyone can close and only one person can open.",
    "TLS uses the certificate's key pair to authenticate and to help derive a symmetric session key. Application code that RSA-encrypts every database field pays CPU and key-management cost it did not need.",
    "you are choosing a primitive for a real payload size",
    "you need a one-way fingerprint, which is a hash, not encryption",
    ["Storing data encrypted under a key that lives next to the data.", "Using ECB.", "Confusing encoding such as base64 with encryption."],
)

add(
    "D04-T016",
    "A WebSocket starts as an HTTP upgrade and then becomes a framed, full-duplex connection. Either side can send. Server-Sent Events stay on HTTP and carry a one-way stream of text events from server to client, with the browser reconnecting automatically. WebSockets need their own heartbeat because intermediaries time out idle TCP. SSE reconnects with Last-Event-ID if the application sets ids.",
    ["Decide whether the client must send data on the same channel", "Upgrade or open the stream", "Heartbeat or reconnect", "Resume from the last acknowledged event"],
    "a load balancer idle timeout killing a quiet WebSocket, or an SSE proxy that buffers the whole stream",
    "connection age, heartbeat misses, and the gap in event ids after reconnect",
    "def sse_frame(event_id, data):\n    return f'id: {event_id}\\ndata: {data}\\n\\n'\n",
    "A WebSocket is a phone call after the front desk transfers you. SSE is a radio station you can retune, with a bookmark of the last story you heard.",
    "A trading UI that must send orders and receive ticks uses a WebSocket. A notification ticker that only displays server events is simpler as SSE, if proxies are configured not to buffer it.",
    "you need a long-lived stream and you have checked the proxies",
    "a request/response API is enough, in which case a socket is an idle-connection leak",
    ["No heartbeat.", "Buffering SSE at a proxy.", "Storing session state only in the process that holds the socket."],
)

add(
    "D04-T017",
    "Long polling holds an HTTP request open until the server has an event or a timeout, then the client immediately opens another request. It works through ordinary HTTP stacks. It pays a request per event and a herd of reconnects at the timeout. The server must not tie up an unbounded worker per parked request. A timeout response is not an error.",
    ["Client opens a request", "Server waits until an event or a deadline", "Server returns the event or an empty timeout", "Client opens the next request immediately"],
    "a timeout of every parked request at the same instant, stampeding the server, or a worker-per-connection pool that runs out",
    "parked-request count, reconnect herd size, and event delivery delay",
    "def next_wait(timeout_s):\n    return timeout_s\n",
    "Long polling is calling a shop and being put on hold until the item arrives, then calling again.",
    "A legacy notification channel uses long polling because a corporate proxy blocks WebSockets. The server parks the request in an async wait, not on a thread per user.",
    "you cannot use a real push channel and events are infrequent",
    "event rates are high, where the request overhead dominates",
    ["Allocating a thread per parked client.", "Treating the timeout as a 500.", "Forgetting to dedupe when the client retries and the event is delivered twice."],
)

add(
    "D04-T018",
    "REST here means HTTP with resources, methods, and status codes, usually JSON. gRPC is HTTP/2 with protobuf contracts, generated clients, and streaming. REST is easy to debug with curl and caches GET. gRPC gives a schema and efficient binary calls inside a datacenter, and it is awkward for browsers without a proxy. Neither fixes a bad domain model.",
    ["Choose the caller: browser, public client, or internal service", "Pick a schema story", "Define deadlines and idempotency", "Put a proxy in front if browsers must speak to gRPC"],
    "a public JSON API modeled as a single POST RPC, or a gRPC API exposed to browsers without grpc-web",
    "contract-breakage count, payload size, and client generation lag",
    "def style(public_browser: bool):\n    return 'http-json' if public_browser else 'grpc-internal'\n",
    "REST is a set of labeled drawers a person can open with a standard key. gRPC is a preprinted form both offices already agreed on, which is faster inside the building and opaque on the street.",
    "Internal order-to-inventory calls use gRPC with deadlines. The public API stays HTTP JSON so third parties can call it without your protobuf toolchain.",
    "you are picking a service contract style",
    "you choose gRPC only because it is newer, without a schema or a deadline story",
    ["Protobuf without compatibility rules.", "REST without status codes.", "Sharing one client timeout for every method."],
)

add(
    "D04-T019",
    "A forward proxy acts for clients leaving a network. A reverse proxy acts for servers, terminating client connections and forwarding inward. A load balancer distributes requests across healthy backends using round-robin, least-connections, or consistent hashing. Health checks decide membership. A balancer that does not drain connections will send traffic to a task that is shutting down.",
    ["Terminate or forward the connection", "Pick a healthy backend", "Shift traffic off a draining backend", "Retry only idempotent calls"],
    "health checks that hit a shallow endpoint while the real dependency is down, so the balancer keeps sending users to a broken task",
    "unhealthy-backend ejection time and error rate during deploys",
    "def choose(backends):\n    live = [b for b in backends if b['healthy']]\n    return live[0] if live else None\n",
    "A reverse proxy is the restaurant host who seats you. A load balancer is that host choosing the least busy section. A forward proxy is your company's door on the way out.",
    "An ingress controller stops sending new requests to a pod that failed readiness, and it keeps existing requests until the grace period ends. Without a drain, users see resets on every deploy.",
    "you are placing a tier in front of replicated services",
    "you have one process and are adding a proxy that becomes the new single point of failure without a reason",
    ["Health-checking only the process, not the dependency.", "Retrying POST at the proxy.", "Forgetting connection drain on shutdown."],
)

add(
    "D04-T020",
    "NAT rewrites addresses so many hosts can share one public address, or so a private service can be reached through a gateway. It breaks end-to-end addressing and complicates protocols that embed IP addresses in payloads. A firewall filters flows by address, port, and state. Ports distinguish sockets on one host. Opening a port is not the same as authenticating the caller.",
    ["Map an internal flow to an external address and port", "Track connection state", "Allow only the intended ports", "Authenticate at the application, not only at the port"],
    "a stateful rule that allows a return path you did not intend, or a NAT timeout that drops an idle database connection",
    "NAT table size, firewall drop count, and idle timeouts versus application keepalive",
    "def allowed(port, allow):\n    return port in allow\n",
    "NAT is a front desk that rewrites the return address on every letter. A firewall is the door policy. The port is the apartment number, not the resident's ID.",
    "A security group opens 443 to the internet and people call the service 'exposed' even though the app still checks tokens. Idle NAT entries drop a WebSocket that did not heartbeat.",
    "you are explaining reachability or a dropped idle flow",
    "you treat an open port as an authorization decision",
    ["Embedding private IPs inside application payloads.", "Disabling stateful tracking without a plan.", "Using a long-lived connection without a keepalive inside a NAT."],
)

add(
    "D04-T021",
    "A CDN caches content at edges close to users and terminates TLS there. It reduces origin load and RTT for cacheable bytes. The origin still owns uncacheable and personalized responses. Cache keys must include every input that changes the body. A purge has to be explicit because TTL is the other way an object leaves.",
    ["Separate cacheable from personalized routes", "Define the cache key", "Set freshness", "Purge or version a URL when the origin content changes"],
    "caching a response that varies by cookie under a key that ignores the cookie",
    "edge hit ratio and origin request rate after a purge",
    "def cache_key(path, vary):\n    return path + '|' + '|'.join(vary)\n",
    "A CDN is a set of branch libraries that keep popular books so you do not travel to the main archive. A personalized letter is never shelved in the branch.",
    "Product images are served from the edge. Account pages bypass the cache. A bad cache key on a search page shows one user another user's results.",
    "the bytes are public and larger than the header overhead",
    "the response is unique per user or must be consistent immediately after a write",
    ["Purging everything on every deploy.", "Forgetting the query string in the cache key.", "Putting the origin in one region and assuming the edge fixes write latency."],
)

add(
    "D04-T022",
    "A connection pool reuses open TCP or TLS sessions so each request does not pay a handshake. Keep-alive holds a connection open for another request. The pool has a max size, an idle timeout, and a wait timeout. An unbounded pool is a file-descriptor leak with extra steps. A pool that is smaller than the offered concurrency queues callers.",
    ["Open a connection only if the pool has no idle one", "Cap the total", "Return it to the pool after the request", "Close idle ones before the server or NAT does"],
    "a pool that never validates a connection and hands out a socket the server already closed",
    "pool wait time, handshake rate, and errors on the first request after idle",
    "class Pool:\n    def __init__(self, max_open):\n        self.max_open = max_open\n        self.idle = []\n        self.open = 0\n",
    "A pool is a taxi stand with a fixed number of cars. Keep-alive is leaving the meter running between your errands instead of hailing a new cab each time.",
    "A service that opens a new TLS connection per database query spends the CPU on handshakes. A pool of 100 with a wait timeout fails fast when the database is the bottleneck instead of opening 10,000 sockets.",
    "the remote handshake is expensive relative to the request",
    "the peer is different every call, so there is nothing to reuse",
    ["No max size.", "No idle timeout.", "Retrying a request on a broken pooled connection without checking idempotency."],
)

add(
    "D04-T023",
    "Latency is how long one unit of work takes. Bandwidth is the capacity of the pipe. Throughput is how much useful work completes per unit time. Packet loss forces retransmission and can cut throughput far below the bandwidth. A high-bandwidth path can still have terrible latency. Adding bandwidth does not fix a chatty protocol's round trips.",
    ["Measure RTT separately from bytes per second", "Count loss", "Count round trips in the protocol", "Fix the dominant term before adding capacity"],
    "a protocol that needs fifty round trips looking 'slow' on a high-bandwidth, high-latency link",
    "RTT, loss percent, and useful throughput versus link bandwidth",
    "def transfer_time(bytes_, bandwidth, rtt, trips):\n    return trips * rtt + bytes_ / bandwidth\n",
    "Bandwidth is how many lanes the highway has. Latency is how long the trip takes. Packet loss is lanes closing and forcing you to drive the stretch again.",
    "A cross-region database call with a 80 ms RTT and twenty queries spends 1.6 seconds in light-speed delay before bandwidth matters. Batching queries beats a bigger NIC.",
    "you are explaining a performance number",
    "you buy bandwidth for a latency problem",
    ["Using throughput and bandwidth as synonyms.", "Ignoring loss.", "Averaging latency and hiding the tail."],
)

add(
    "D09-T003",
    "Write-ahead logging records a change to durable log storage before the database treats the change as committed. On crash, replay of the log restores committed work and discards what never committed. The log is the source of recovery. Data pages can be flushed later. A commit that returns before the WAL record is durable is not a commit.",
    ["Write the change to the WAL", "Make that WAL record durable", "Acknowledge the commit", "Apply or flush data pages afterward"],
    "acknowledging a commit before the WAL fsync, so a crash loses a transaction the client was told succeeded",
    "WAL sync latency and the lag between commit and the durable LSN",
    "-- unexecuted illustration, not a production setting\n-- commit returns after the WAL record for that transaction is flushed\n",
    "The WAL is a diary you write in ink before you update the printed ledger. If the building loses power, you redo the diary and ignore pencil notes that never made it.",
    "PostgreSQL commit waits on WAL flush according to synchronous_commit. Turning that off makes commits faster and silently drops the last transactions on a crash.",
    "you need crash recovery of committed transactions",
    "you are using a cache, which has no such log unless you add one",
    ["Disabling sync for speed and still promising durability.", "Putting WAL and data on a volume that lies about fsync.", "Deleting WAL segments that a replica still needs."],
    lang="sql",
)

add(
    "D09-T004",
    "A checkpoint flushes dirty data pages so that crash recovery does not have to replay the entire history of the database. Recovery starts from the last checkpoint's redo point and replays WAL up to the end. Checkpoints that are too infrequent make recovery long. Checkpoints that are too aggressive flood the disk and stall queries. The checkpoint is not a backup.",
    ["Start a checkpoint on a schedule or a WAL-size trigger", "Write dirty pages without blocking every query", "Record the redo LSN", "On crash, replay WAL from that LSN"],
    "recovery taking longer than the outage budget because checkpoints were rare, or a checkpoint IO spike causing query latency",
    "checkpoint duration, WAL bytes generated between checkpoints, and recovery time in a restore drill",
    "-- unexecuted: control checkpoint pressure in postgresql.conf\n-- checkpoint_timeout and max_wal_size bound how much WAL recovery must replay\n",
    "A checkpoint is photographing the shop floor so tonight's audit only reviews receipts since the photo, not since the store opened.",
    "After a power loss, PostgreSQL replays from the last checkpoint. A restore drill that has never been timed is how you discover recovery takes two hours.",
    "you are bounding crash recovery time",
    "you need a point-in-time backup, which a checkpoint does not give you",
    ["Calling a checkpoint a backup.", "Setting checkpoint frequency without watching IO.", "Never practicing recovery."],
    lang="sql",
)

add(
    "D09-T005",
    "VACUUM reclaims space from dead tuples so PostgreSQL can reuse it, and it freezes transaction ids so the system does not wrap. Autovacuum runs that work in the background when a table's dead-tuple count crosses a threshold. Vacuum does not return space to the operating system unless it can truncate free pages at the end. A long-running transaction blocks vacuum from removing tuples that transaction might still see.",
    ["Find dead tuples older than every open snapshot", "Mark their space reusable", "Update visibility and freeze old ids", "Do not wait for a manual vacuum if autovacuum can keep up"],
    "transaction-id wraparound shutdown, or a table that grows forever because a forgotten transaction holds back vacuum",
    "dead tuple count, age of the oldest transaction id, and autovacuum runtime",
    "-- unexecuted diagnostic\nSELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables;\n",
    "Vacuum is clearing abandoned plates so the tables can be reused. It does not knock down the restaurant wall and give the land back to the city.",
    "A reporting transaction left open overnight stops autovacuum from cleaning the orders table. The table bloats and sequential scans get slower until the transaction ends.",
    "the table receives updates or deletes",
    "you expect VACUUM FULL's lock on a hot table during peak",
    ["Disabling autovacuum.", "Leaving idle-in-transaction sessions open.", "Assuming vacuum shrinks the file on disk."],
    lang="sql",
)

add(
    "D09-T006",
    "A dead tuple is a row version that no current snapshot needs, left behind by an update or delete because PostgreSQL uses MVCC. Table bloat is the live data plus those dead versions plus free space that has not been reused. Bloat makes sequential scans and index scans read more pages. The fix is vacuum and shorter transactions, not a bigger cache alone.",
    ["Update or delete creates a new version and leaves the old one", "Snapshots finish", "Vacuum marks the old version reusable", "New writes reuse that space"],
    "a table several times larger than its live rows, with queries reading mostly dead bytes",
    "live tuple count versus page count, and bloat estimated from pg_stat",
    "SELECT n_live_tup, n_dead_tup FROM pg_stat_user_tables WHERE relname = 'orders';\n",
    "Dead tuples are old editions of a form left in the folder. The folder gets thick even though only the top form is current.",
    "An orders table updated on every status change, with a replica used for analytics that lags, retains dead tuples until vacuum can see that the replica has moved on. Disk and cache fill with old versions.",
    "you are explaining growth or a scan that got slower after updates",
    "you rewrite the table with VACUUM FULL during peak traffic",
    ["Adding an index to a bloated heap and expecting the heap scan to shrink.", "Blaming autovacuum without looking for a held snapshot.", "Equating file size with live data size."],
    lang="sql",
)

add(
    "D09-T007",
    "The heap is PostgreSQL's table storage: unordered row versions in pages. An index points at heap tuple identifiers. TOAST moves oversized attributes to a side table and leaves a pointer in the main row, so a page can stay small enough to scan. Toasted values may be compressed and stored out of line. Selecting the wide column fetches the TOAST data. Selecting only the narrow columns can avoid it.",
    ["Store the row in the heap", "If an attribute is large, move it to TOAST", "Keep indexes pointing at the heap", "Fetch TOAST only when the query needs that column"],
    "SELECT * on a table with large JSON or text, pulling TOAST for rows that only needed an id",
    "TOAST table size and buffer hits when the query list includes the wide column",
    "SELECT id, status FROM orders WHERE id = 1;\n-- avoids reading a toasted payload column that this query does not need\n",
    "The heap is a stack of variable forms. TOAST is the annex where the oversized attachments live, with a stub left on the form.",
    "A documents table stores the file bytes in a bytea column and every list API loads them. Splitting metadata from payload, or simply not selecting the bytea, drops latency.",
    "rows carry attributes too large for a normal page",
    "you put hot narrow counters and cold blobs in one row and always select both",
    ["Using SELECT *.", "Indexing a toasted column by accident in a way that bloats the index.", "Assuming the heap is ordered by primary key."],
    lang="sql",
)

add(
    "D09-T008",
    "A B-tree index supports equality and range order. GIN indexes composite values such as arrays, JSONB keys, and full text, and is built for elements contained in a value. GiST indexes geometric and other extensible types and nearest-neighbor strategies. BRIN stores summaries of value ranges per block range and stays small when the table is physically ordered by the indexed column. The wrong index type still gets updated on every write.",
    ["Name the predicate", "Match it to an index access method", "Check the plan uses it", "Budget the write cost of maintaining it"],
    "a B-tree on a high-cardinality JSON path that the planner never uses, or a BRIN index on unordered data that returns the whole table",
    "index-only or index scan rows versus sequential scan rows, and insert latency after the index exists",
    "CREATE INDEX CONCURRENTLY orders_created_brin ON orders USING brin (created_at);\n",
    "A B-tree is a phone book. GIN is an index of individual words. GiST is a map index. BRIN is a note that says which shelf of a time-ordered archive might hold the year you want.",
    "created_at on an append-only events table is a BRIN candidate. A unique order id is a B-tree. Searching JSONB containment wants GIN. Building all three 'just in case' taxes every insert.",
    "you have a predicate and a measured plan",
    "you add indexes for columns nobody filters on",
    ["Assuming every index speeds every query.", "Using BRIN on randomly inserted keys.", "Creating indexes without CONCURRENTLY on a live table and taking a write lock you did not plan."],
    lang="sql",
)

add(
    "D09-T009",
    "The planner turns a SQL statement into a plan by estimating the cost of candidate paths: sequential scans, index scans, joins, and aggregations. The optimizer searches that space. It does not execute the query to decide. Bad estimates produce bad plans. The executor then runs the chosen plan. A plan that was good at one data size can be wrong after the table grows.",
    ["Parse and rewrite the query", "Estimate cardinality using statistics", "Cost the candidate paths", "Execute the cheapest plan the search kept"],
    "a nested loop over a million-row underestimate, or a sequential scan chosen because a parameter is unknown at plan time",
    "estimated rows versus actual rows in EXPLAIN ANALYZE",
    "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 42;\n",
    "The planner is a dispatcher who prices several routes from a map. If the map says the bridge is empty and it is not, the cheap route is a traffic jam.",
    "A query that is fast in staging and slow in production often has a different row estimate. EXPLAIN ANALYZE showing estimated rows of 1 and actual rows of 500000 is the smoking gun.",
    "you are explaining a slow query",
    "you rewrite SQL at random without looking at estimated versus actual rows",
    ["Reading cost numbers as milliseconds.", "Adding a hint or an index before reading the plan.", "Assuming the planner knows about correlation it was not told about."],
    lang="sql",
)

add(
    "D09-T010",
    "Statistics are the planner's summary of a table: most common values, histograms, fraction of nulls, and distinct counts. ANALYZE samples the table and writes pg_statistic. Autovacuum analyzes as well as vacuums. Stale statistics after a bulk load produce plans for a table shape that no longer exists. Extended statistics capture correlation between columns that single-column stats miss.",
    ["Sample the table", "Store histograms and most common values", "Plan using those summaries", "Re-analyze after a large load or a distribution change"],
    "a plan chosen from last month's histogram after a backfill changed the data",
    "last_analyze time and the estimated-versus-actual row gap",
    "ANALYZE orders;\n",
    "Statistics are a survey, not a census. The planner believes the survey until you run another one.",
    "A nightly load of a year's orders followed by queries that still assume the table is tiny is fixed by an explicit ANALYZE at the end of the load, not by a new index first.",
    "data distribution changed or estimates are wildly wrong",
    "you analyze every minute on a table whose distribution is stable and you just add IO",
    ["Assuming autovacuum analyze kept up with a bulk load.", "Deleting stats.", "Raising the sample blindly and still ignoring cross-column correlation."],
    lang="sql",
)

add(
    "D09-T011",
    "Isolation decides which anomalies a transaction is allowed to see. PostgreSQL's read committed takes a new snapshot per statement. Repeatable read and serializable keep a snapshot for the transaction. Row-level locks such as FOR UPDATE stop two transactions from updating the same row. They do not by themselves stop phantoms unless the isolation level does. Lock wait is not a deadlock until a cycle exists.",
    ["Pick an isolation level that matches the anomaly you must forbid", "Lock the rows you will update", "Keep the transaction short", "Retry serialization failures"],
    "a read-committed check-then-insert that lets two sessions create the same logical booking",
    "serialization failures, lock-wait time, and duplicate business keys",
    "BEGIN;\nSELECT id FROM seats WHERE id = 10 FOR UPDATE;\n-- decide, then update, then COMMIT\n",
    "Isolation is deciding whether you see the menu as it was when you sat down or as it is each time you look up. A row lock is putting your hand on one plate so nobody else takes it.",
    "Two checkout requests read the last seat as free under read committed and both insert. A unique constraint is the backstop. FOR UPDATE on the seat row is the lock. Serializable plus a retry also works.",
    "two transactions can update related rows",
    "you hold a row lock across a user think time",
    ["Using read committed and assuming the first SELECT still holds.", "Catching a serialization failure and not retrying.", "Locking rows in different orders."],
    lang="sql",
)

add(
    "D09-T012",
    "An advisory lock is a lock on a key your application defines, not on a table row. PostgreSQL does not know what the key means. Session-level locks last until unlock or disconnect. Transaction-level locks last until commit or rollback. They coordinate application work such as a single worker claiming a job. They do not lock the rows the job will touch unless you also lock those rows.",
    ["Choose a bigint key that names the resource", "Take the lock at the start of the critical work", "Do the work", "Release on the same session or at transaction end"],
    "two application nodes both thinking they hold the lock because one used a session lock and checked the wrong return value",
    "the fraction of workers who acquire the lock, and jobs that run twice",
    "SELECT pg_try_advisory_lock(42);\n-- unexecuted: true means this session holds key 42\n",
    "An advisory lock is a numbered coat hook you and your coworkers agree on. The database only knows the hook number, not whose coat it is.",
    "A cron cluster uses pg_try_advisory_lock on the job id so only one node runs the payout. If the node dies, a session-level lock disappears with the connection and another node can take it.",
    "you need a cooperative mutex and you do not have a natural row to lock",
    "you needed a row lock or a unique constraint, which actually protects the data",
    ["Ignoring the boolean from pg_try_advisory_lock.", "Using a transaction lock and then doing work after commit.", "Assuming the lock survives a connection pooler that reuses sessions."],
    lang="sql",
)

add(
    "D09-T013",
    "Streaming replication ships WAL records to a standby that replays them, producing a physical copy. Logical replication ships row changes from a publication to a subscription, which can be a subset of tables and can land on a different major version or schema shape. Physical replicas are for failover and read scaling of the whole cluster. Logical replication is for selective copy and upgrades. Both lag.",
    ["Generate WAL or a logical change", "Ship it to the replica", "Apply it in order", "Monitor lag before you read or fail over"],
    "promoting a replica that has not received the latest commit, or a logical subscriber stuck on one bad row",
    "replay lag in bytes and seconds, and subscription error state",
    "-- unexecuted: physical replicas apply WAL; logical subscribers apply row changes\nSELECT slot_name, confirmed_flush_lsn FROM pg_replication_slots;\n",
    "Streaming replication is photocopying the diary pages. Logical replication is reading the diary and rewriting selected entries into another notebook.",
    "A read replica for dashboards can be physical. A migration that copies only the users table to a new instance is logical. Failing over to a lagged physical replica loses the commits that never arrived.",
    "you need a copy of the data on another node",
    "you treat a lagged replica as proof of a durable commit on the primary",
    ["Reading from a replica that your SLO says must be current.", "Forgetting a replication slot can retain WAL until the disk fills.", "Assuming logical replication copies sequences and DDL the way you hoped."],
    lang="sql",
)

add(
    "D09-T014",
    "Table partitioning splits one logical table into physical partitions, often by time range or by a list of tenants. Queries that include the partition key can prune partitions. Queries that do not include it scan all of them. Unique constraints must include the partition key. Dropping an old partition is metadata work compared with deleting millions of rows.",
    ["Choose a partition key that queries filter on", "Create partitions ahead of the data", "Plan retention as detach or drop", "Index each partition as the planner will actually use it"],
    "a query without the partition key that opens every partition, or a unique constraint that cannot be enforced globally",
    "partitions scanned per query, and time to drop an expired partition",
    "CREATE TABLE events (\n  id bigint,\n  created_at timestamptz NOT NULL,\n  PRIMARY KEY (id, created_at)\n) PARTITION BY RANGE (created_at);\n",
    "Partitioning is filing cabinets by month. Asking for a customer without saying the month means opening every cabinet.",
    "An events table partitioned by month drops March by detaching a partition. A query for one customer across all time still touches every month unless a second access path exists.",
    "retention or prune-friendly queries dominate",
    "you partition a small table and pay planning cost for no pruning",
    ["Omitting the partition key in the primary key.", "Creating no partition for next month and failing inserts.", "Expecting a global unique email across range partitions without the key."],
    lang="sql",
)

add(
    "D09-T015",
    "A connection pooler sits between the application and PostgreSQL and reuses a smaller set of server connections. Session pooling holds a server connection for a whole client session. Transaction pooling returns it after each transaction and breaks session state such as prepared statements, temporary tables, and session advisory locks. The database's max connections must cover the pooler, not every application thread.",
    ["Cap application threads separately from database connections", "Choose session or transaction pooling", "Avoid session features the mode cannot support", "Time out waiters instead of opening unlimited servers"],
    "a transaction-pooled session advisory lock that releases when the pooler gives the connection to someone else, or max_connections exhausted by bypassing the pooler",
    "client wait time for a pooled connection, and the number of server connections versus max_connections",
    "# unexecuted shape: one pool, a hard max, a wait timeout\nclass Settings:\n    max_db_connections = 20\n    acquire_timeout_s = 2\n",
    "A pooler is a switchboard with twenty lines into the database and two hundred callers. Transaction mode hangs up after each call. Session mode leaves the line open and ties up a line even while the caller thinks.",
    "PgBouncer in transaction mode in front of PostgreSQL lets a web tier with hundreds of workers share dozens of backends. Session-level advisory locks and SET statements then misbehave because the next transaction may run on another backend.",
    "application concurrency is much higher than the database can serve as one connection each",
    "you need session state and you still pick transaction pooling",
    ["Pointing every replica and the pooler at the same max_connections budget carelessly.", "Using prepared statements in transaction mode without the pooler's support.", "Hiding a slow query by adding pool capacity."],
)

add(
    "D09-T016",
    "Replication lag is how far a replica is behind the primary, in WAL bytes or in time. A read from a lagged replica can miss a commit the user just made. Failover to a lagged replica loses the commits that never shipped. Lag grows when the replica cannot replay as fast as the primary writes, or when the network stalls. Hot standby feedback and long queries on the replica interact with vacuum on the primary.",
    ["Ship WAL", "Apply WAL on the replica", "Expose lag to the reader", "Refuse a read or a promotion if lag is past the budget"],
    "a user writes a row, reads it from a replica, and does not see it",
    "replay_lag and write-then-read misses",
    "SELECT now() - pg_last_xact_replay_timestamp() AS replay_lag;\n",
    "Lag is the delay between writing a line in the diary and the photocopy catching up. Reading the photocopy early means you miss the last line.",
    "A comment posted to the primary and then read from a replica 'disappears' for the author. The fix is reading that user's write from the primary, or waiting until replay passes that LSN.",
    "you serve reads from a replica",
    "you need read-your-writes and you have not pinned that read to the primary",
    ["Alerting only on replica process up.", "Promoting the furthest-behind replica.", "Running a long query on the replica that holds back vacuum on the primary."],
    lang="sql",
)

add(
    "D09-T017",
    "A backup is a copy you can restore. A base backup plus WAL archives lets you perform point-in-time recovery to a chosen LSN or time. A logical dump is portable and slower to restore at size. A replica is not a backup, because a bad statement replicates. Recovery must be drilled. An untested backup is a hope.",
    ["Take a consistent base backup", "Archive every WAL segment the backup needs", "Record the time and the LSN", "Restore into an empty cluster on a schedule and measure it"],
    "a base backup whose WAL was deleted, so restore cannot reach consistency",
    "time since the last successful restore drill, and restore duration",
    "-- unexecuted: a dump is not a PITR story by itself\n-- pg_dump for logical copy; base backup + WAL archive for point-in-time recovery\n",
    "A backup is a spare ledger in another building. A replica is a clerk copying your current ledger, including the page you accidentally tore out.",
    "Someone runs DELETE without a WHERE. Streaming replicas apply it. Only a point-in-time restore from before the delete brings the rows back.",
    "you need to survive dropped tables, bad deploys, or a destroyed volume",
    "you keep only a replica and call it a backup",
    ["Never restoring.", "Storing the backup on the same disk as the database.", "Archiving WAL with gaps."],
    lang="sql",
)

add(
    "D09-T018",
    "High availability means a standby can take over when the primary fails. Failover promotes a replica. It should be automated only with fencing so the old primary cannot keep accepting writes. Split brain is two nodes accepting writes. The decision uses health checks plus replication position, not a single missed ping. Recovery time includes detection, promotion, and client reconnect.",
    ["Detect failure", "Fence the old primary", "Promote the best replica", "Point clients at the new primary"],
    "split brain, or promoting a replica that is missing the latest transactions",
    "recovery time in a game day, and whether the old primary can still accept writes",
    "def may_promote(lag_bytes, limit, old_primary_fenced):\n    return old_primary_fenced and lag_bytes <= limit\n",
    "Failover is handing the only pen to the deputy after you have taken the pen away from the person who left. If both keep the pen, you have two ledgers.",
    "A primary dies. The orchestrator fences it, promotes the replica with the smallest lag, and updates the connection endpoint. Clients retry idempotent work. Writes that were acknowledged and not shipped are still lost if the replica was behind.",
    "you have a defined recovery-time objective and more than one node",
    "you automate promotion without fencing",
    ["Two writers after a network partition.", "Health checks that flap.", "Forgetting connection strings and poolers still point at the old primary."],
)
