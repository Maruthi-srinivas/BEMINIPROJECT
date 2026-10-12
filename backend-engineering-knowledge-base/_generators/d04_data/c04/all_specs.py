"""Compact specs for D04-T002..T023."""

from ..topic_builder import TopicSpec
from ..topic_factory import A
from .t002 import SPEC as T002

# fmt: off
def _ex(title, e1, e2, e3):
    return [
        (f"Design or debug exercise for {title}: {e1}", e2),
        (f"Operational scenario for {title}: {e3}", "You name layered checks and a safe mitigation."),
        (f"Trade-off for {title}: pick two designs and compare.", "You state benefit, cost, and when to choose each."),
    ]


def _sol():
    return [
        "Document assumptions, show the calculation or sequence, and note how you would verify in staging.",
        "List evidence (metrics, captures, configs) that confirms the hypothesis before changing production.",
        "Compare options with one measurable criterion such as latency, cost, or operability.",
    ]


def mk(
    id,
    name,
    slug,
    deps,
    elevator,
    principles,
    internals,
    mermaid,
    facts,
    code_file,
    code,
    mistakes,
    debugging,
    tradeoff_rows,
    revision_items,
    related,
    completion,
    examples=None,
):
    f = facts
    beginner = [
        (f"What is {name}?", A(f[0], f[1], f[2], f[3]), f"What is {name}?"),
        (f"Why does {name} matter for backends?", A(f[4], f[5], f[6], f[7]), "Why it matters"),
        (f"Name one failure mode involving {name}.", A(f[8], f[9], f[10], f[11]), "Failure mode"),
        (f"How does {name} interact with TCP/IP?", A(f[12], f[13], f[14], f[15]), "TCP/IP interaction"),
        (f"What tool helps observe {name}?", A(f[16], f[17], f[18], f[19]), "Observation tools"),
    ]
    intermediate = [
        (f"Explain {name} in one request path.", A(f[20], f[21], f[22], f[23]), "Request path"),
        (f"How do load balancers affect {name}?", A(f[24], f[25], f[26], f[27]), "Load balancers"),
        (f"Security consideration for {name}?", A(f[28], f[29], f[30], f[31]), "Security"),
        (f"Performance pitfall with {name}?", A(f[32], f[33], f[34], f[35]), "Performance"),
        (f"How do containers change {name}?", A(f[36], f[37], f[38], f[39]), "Containers"),
    ]
    advanced = [
        (f"Edge case for {name}?", A(f[40], f[41], f[42], f[43]), "Edge case"),
        (f"How does {name} behave under packet loss?", A(f[44], f[45], f[46], f[47]), "Packet loss"),
        (f"Multi-region angle on {name}?", A(f[48], f[49], f[50], f[51]), "Multi-region"),
        (f"How would you test {name} in CI?", A(f[52], f[53], f[54], f[55]), "CI testing"),
        (f"Version or compatibility note for {name}?", A(f[56], f[57], f[58], f[59]), "Compatibility"),
    ]
    scenarios = [
        (f"Outage: symptoms match {name} misconfiguration.", A(f[60], f[61], f[62], f[63]), "Outage scenario"),
        (f"Latency regression tied to {name}.", A(f[64], f[65], f[66], f[67]), "Latency scenario"),
        (f"Security audit flags {name}.", A(f[68], f[69], f[70], f[71]), "Audit scenario"),
        (f"Migration changes {name}.", A(f[72], f[73], f[74], f[75]), "Migration scenario"),
        (f"Interview deep dive on {name}.", A(f[76], f[77], f[78], f[79]), "Deep dive scenario"),
    ]
    follow_ups = [
        (f"How does {name} relate to the previous D04 topic?", A(f[80], f[81], f[82], f[83]), "Previous topic"),
        (f"What D04 topic follows {name}?", A(f[84], f[85], f[86], f[87]), "Next topic"),
        (f"How does {name} connect to backend APIs?", A(f[88], f[89], f[90], f[91]), "API connection"),
    ]
    return TopicSpec(
        id=id,
        name=name,
        subdomain=name,
        slug=slug,
        deps=deps,
        elevator=elevator,
        principles=principles,
        internals=internals,
        mermaid=mermaid,
        examples=examples or [f[0], f[20], f[40]],
        code_file=code_file,
        code=code,
        practical=[f[24], f[28], f[52]],
        tradeoff_rows=tradeoff_rows,
        mistakes=mistakes,
        debugging=debugging,
        beginner=beginner,
        intermediate=intermediate,
        advanced=advanced,
        scenarios=scenarios,
        follow_ups=follow_ups,
        exercises=_ex(name, "sketch the flow", "Diagram includes clients, network, and service.", "users see intermittent errors"),
        solutions=_sol(),
        revision_items=revision_items,
        related=related,
        completion=completion,
    )


T003 = mk(
    "D04-T003", "MAC addresses, ARP", "d04-t003-mac-addresses-arp",
    ["D04-T002", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "MAC addresses identify link-layer interfaces on a LAN; ARP resolves IPv4 addresses to MACs for on-segment delivery.",
    [
        "Ethernet frames carry source and destination MAC addresses on a broadcast domain.",
        "ARP broadcasts who-has requests for an IPv4 address and caches replies in a table with timeouts.",
        "Switches learn MAC locations; routers terminate broadcast domains.",
        "Gratuitous ARP can announce moves; spoofing ARP is a classic MITM on untrusted LANs.",
    ],
    [
        "When a packet is on-link, the host ARPs the destination IP or uses the gateway MAC for off-link traffic.",
        "ARP cache entries expire; stale entries cause unreachable neighbors until refresh.",
        "Cloud overlays may hide ARP from tenants while still using MAC underlay.",
        "Containers on a bridge share a broadcast domain unless segmented.",
    ],
    """flowchart TD
  ipPkt[IPv4_packet]
  arp[ARP_resolve]
  frame[Ethernet_frame]
  ipPkt --> arp
  arp --> frame""",
    [
        "MACs are 48-bit and assigned to NICs; they do not cross routers.",
        "ARP maps IP to MAC on the same L2 segment.",
        "Default gateway ARP is required for off-subnet traffic.",
        "ARP tables age out to handle mobility.",
        "Backends rarely set MACs; the kernel does.",
        "Mis-ARP looks like flaky connectivity.",
        "Switches flood unknown unicast until learned.",
        "RARP is obsolete; DHCP replaced it.",
        "Silent ARP failures cause TCP SYN timeouts.",
        "Duplicate IP triggers ARP conflicts.",
        "Wireshark shows ARP before TCP SYN on LAN.",
        "Bonded NICs share virtual MAC.",
        "VPC may use overlay without visible ARP.",
        "Kubernetes CNI plugins manage L2/L3.",
        "Security: dynamic ARP inspection on switches.",
        "tcpdump -n arp is the first LAN check.",
        "Cloud LB nodes answer ARP for VIPs.",
        "Gratuitous ARP updates peers after failover.",
        "IPv6 uses NDP instead of ARP.",
        "Proxy ARP makes remote subnets appear local.",
        "On-link delivery uses resolved MAC as next hop.",
        "LB DNAT may change destination MAC at hop.",
        "Firewalls still need IP and port rules.",
        "TLS does not replace ARP trust.",
        "Spoofed ARP enables LAN MITM.",
        "Static ARP entries reduce spoof risk.",
        "Microbursts of ARP indicate scan or storm.",
        "Bridge hairpin may require special MAC learning.",
        "Sidecars do not change ARP on host NIC.",
        "ARP timeout too low increases broadcast load.",
        "ARP timeout too high slows failover.",
        "Jumbo frames need matching MTU end-to-end.",
        "Bond failover sends gratuitous ARP.",
        "Wi-Fi roaming triggers ARP refresh.",
        "Duplicate MAC flaps switch ports.",
        "Container MAC per veth is local to host.",
        "Overlay ARP may be encapsulated in UDP.",
        "Cross-AZ traffic may not use ARP visibly.",
        "Anycast VIP MAC moves on BGP withdraw.",
        "Test ARP with arping in staging LAN.",
        "CI cannot easily test ARP without L2 lab.",
        "ARP is IPv4-specific; plan NDP for v6.",
        "Old kernels log duplicate ARP warnings.",
        "Mis-cabled VLAN breaks ARP domain.",
        "Storm after loop floods ARP table CPU.",
        "Rate-limit ARP on access ports.",
        "Document VIP failover ARP behavior.",
        "Migration changes gateway MAC seen by hosts.",
        "Drain node before VIP move to reduce stale ARP.",
        "Audit flat L2 networks for ARP spoof risk.",
        "Interview: explain why ping gateway then ARP.",
        "Tie to CIDR: on-link vs off-link decision.",
        "Next topic TCP uses IP learned via ARP path.",
        "APIs still depend on correct L3/L2 beneath.",
    ],
    "examples/d04_t003_arp.py",
    'print("ARP is observed with tcpdump; not simulated here")',
    ["Ignoring ARP when TCP to on-link IP fails", "Assuming ARP works across routers", "Forgetting gratuitous ARP on VIP failover", "Flat VLANs without DAI", "Confusing MAC with IP in logs"],
    ["Check ARP cache and gateway reachability", "Look for duplicate IP warnings", "Verify VLAN and subnet match", "Capture ARP during SYN failure"],
    [("Static ARP", "Spoof resistance", "Ops burden", "Critical appliances", "Large dynamic pools"), ("Proxy ARP", "Remote subnets on one LAN", "Confusing routing", "Legacy networks", "Modern VPC designs")],
    ["MAC is link-local", "ARP resolves IPv4 to MAC", "NDP replaces ARP in IPv6", "Stale ARP causes blackholes", "VIP failover uses gratuitous ARP"],
    "Understand before: `D04-T002`.\nSupports: `D04-T004` TCP over IP.\nOften confused with: DNS names.",
    ["Explain on-link versus off-link ARP", "Read tcpdump ARP before SYN", "Describe gratuitous ARP on failover", "List ARP spoof risk", "Contrast ARP with NDP"],
)

# T004 TCP vs UDP - facts tailored
F004 = """UDP is connectionless with ports for multiplexing; TCP provides reliable ordered byte streams with retransmissions.
DNS queries often use UDP with truncation leading to TCP retry.
QUIC and HTTP/3 use UDP with user-space reliability.
TCP head-of-line blocking affects single-stream waits.
UDP fits metrics and real-time where loss is acceptable.
TCP fits HTTP/1.1 and most database protocols.
Load balancers track TCP state but may pass UDP statelessly.
Firewalls must allow protocol-specific timeouts.
TLS over TCP adds handshakes; QUIC integrates TLS.
Packet loss hurts TCP throughput via congestion control.
UDP loss is visible to application unless QUIC handles it.
Containers share kernel TCP stack per node.
NAT mapping differs: TCP connections versus UDP flows.
Ephemeral ports exhaust under many UDP flows too.
Multi-region TCP crosses long RTT; UDP DNS may be local cache.
Test both protocols in integration suites.
HTTP/3 changes assumptions about TCP everywhere.
SYN floods target TCP listeners.
UDP amplification attacks abuse stateless servers.
Video may prefer UDP with app-level FEC.
Databases require TCP durability.
gRPC runs on HTTP/2 over TCP.
Game backends mix UDP for input and TCP for auth.
QoS markings rarely end-to-end on Internet.
MTU issues affect both; TCP has PMTUD.
Zero-copy sendfile is TCP-oriented.
Sidecars proxy TCP byte streams.
Service mesh mTLS wraps TCP between proxies.
UDP DNS caching reduces repeated queries.
TCP keep-alive probes idle connections.
Migration from TCP to QUIC needs client support.
Interview contrasts when to pick each transport.
Previous ARP delivers IP frames; transport sits above.
Next handshake topic details TCP setup.
REST APIs still ride TCP unless HTTP/3.""".splitlines()

T004 = mk(
    "D04-T004", "TCP vs UDP", "d04-t004-tcp-vs-udp",
    ["D04-T003", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "TCP offers reliable, ordered delivery; UDP offers minimal datagram service—backend choice depends on loss tolerance and latency needs.",
    ["TCP numbers bytes with sequence numbers and acknowledges in-order data.", "UDP sends self-contained datagrams without built-in retransmission.", "Both use IP addresses plus ports to identify endpoints.", "Application protocols pick the transport: HTTP historically TCP, DNS primarily UDP, HTTP/3 QUIC over UDP."],
    ["Kernel TCP maintains send/receive buffers, congestion window, and reassembly.", "UDP sockets read whole datagrams; partial reads discard remainder unless MSG_PEEK used.", "Middleboxes may block UDP except DNS/NTP.", "Performance tuning differs: TCP window scaling versus UDP application pacing."],
    """flowchart LR
  tcp[TCP_reliable_stream]
  udp[UDP_datagrams]
  app[Application]
  app --> tcp
  app --> udp""",
    F004,
    "examples/d04_t004_ports.py",
    "import socket\nprint(socket.SOCK_STREAM, socket.SOCK_DGRAM)",
    ["Using TCP for loss-tolerant multicast fanout", "Using UDP for money transfers without app reliability", "Ignoring UDP MTU fragmentation", "Assuming QUIC is plain UDP without encryption", "Opening wide UDP ranges without need"],
    ["Check protocol in metrics labels", "Compare loss on UDP DNS vs TCP HTTPS", "Verify firewall rules per protocol", "Capture with tcpdump udp or tcp"],
    [("TCP", "Reliability and ordering", "Latency and HOL blocking", "HTTP, SQL, gRPC", "Loss-tolerant telemetry"), ("UDP", "Low overhead", "No delivery guarantee", "DNS, metrics, QUIC base", "Ledger writes without QUIC/TCP")],
    ["TCP reliable ordered stream", "UDP datagrams without reliability", "Ports multiplex services", "Pick per protocol requirements", "HTTP/3 uses QUIC on UDP"],
    "Understand before: `D04-T003`.\nSupports: `D04-T005` handshake.\nOften confused with: HTTP versus transport.",
    ["Choose TCP or UDP for a new protocol", "Explain DNS UDP then TCP fallback", "Describe TCP HOL blocking", "State one UDP abuse risk", "Name HTTP/3 transport change"],
)

# Continue with handcrafted critical topics T005, T008, T009, T011, T012, T013 - use mk with custom facts strings
# For brevity remaining topics use mk with embedded multiline facts

def facts_block(*lines):
    return [ln.strip() for ln in lines if ln.strip()]


T005_FACTS = list(facts_block(
    "The TCP three-way handshake establishes a connection with SYN, SYN-ACK, and ACK.",
    "The client sends SYN with an initial sequence number ISN; server replies SYN-ACK with its ISN and ack client ISN plus one.",
    "The client completes with ACK acknowledging server ISN plus one; both sides may then send data.",
    "Connection setup costs one RTT for data after handshake in classic TCP.",
    "Backends see SYN backlog before accept queue; SYN floods target this stage.",
    "Graceful close uses FIN packets; the side that sends the first FIN enters FIN-WAIT-1.",
    "The peer acknowledges FIN with ACK and may send its own FIN; active closer eventually reaches TIME-WAIT after the final ACK.",
    "TIME-WAIT lasts approximately two maximum segment lifetimes to absorb late duplicates.",
    "Simultaneous open and close are special cases with extra states.",
    "TLS may start after TCP handshake completes unless TLS 1.3 0-RTT resumption is used.",
    "Load balancers may proxy handshake to backends or offload SYN cookies.",
    "Half-open connections expire via retransmission timeouts.",
    "RST aborts a connection immediately without graceful shutdown.",
    "Keep-alive probes reuse established connections to avoid new handshakes.",
    "Container NAT reuses quadruples; ephemeral port limits matter.",
    "Capture SYN,SYN-ACK,ACK to prove handshake health.",
    "SYN retransmits imply blackhole or filter before accept.",
    "Wrong sequence ACKs yield RST or ignored segments.",
    "Middleboxes may strip options like window scaling.",
    "MSS negotiation happens in SYN options.",
    "Handshake RTT dominates short API calls on distant clients.",
    "Connection pooling avoids repeated handshakes to databases.",
    "Terminate with FIN for clean connection accounting.",
    "Active close side often sees TIME-WAIT; passive close may skip it.",
    "SO_LINGER changes close behavior versus immediate RST.",
    "Kubernetes kube-proxy tracks conntrack for NATed flows.",
    "Sidecars intercept connect() extending handshake path.",
    "mTLS adds another handshake after TCP.",
    "HTTP keep-alive reuses TCP for multiple requests.",
    "Interviewers ask to draw three-way handshake accurately.",
    "Security: SYN cookies mitigate SYN flood without storing state.",
    "Performance: TLS 1.3 reduces crypto round trips after TCP.",
    "Multi-region handshakes add RTT per new connection.",
    "CI should reuse connections in load tests.",
    "Version differences: TCP Fast Open optional data in SYN.",
    "Outage: SYN backlog full causes client timeouts.",
    "Latency: many short TCP connections without pool.",
    "Audit: ensure TLS follows TCP not mixed order.",
    "Migration: changing LB SYN proxy mode drops connections.",
    "Deep dive: explain why both ISNs are independent.",
    "Previous topic compared TCP to UDP.",
    "Next topic covers sequence numbers and retransmits.",
    "APIs benefit from fewer handshakes via pooling.",
))

while len(T005_FACTS) < 92:
    T005_FACTS.append(T005_FACTS[len(T005_FACTS) % len(T005_FACTS)])

T005 = mk(
    "D04-T005", "TCP handshake and connection termination", "d04-t005-tcp-handshake-and-connection-termination",
    ["D04-T004", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "TCP opens with a three-way handshake (SYN, SYN-ACK, ACK) and closes with FIN/ACK exchange; understanding this explains connection latency and TIME-WAIT.",
    [
        "SYN synchronizes sequence numbers and negotiates options like MSS and window scaling.",
        "Neither side sends application data until the handshake completes unless TCP Fast Open is negotiated.",
        "Graceful shutdown exchanges FIN and ACK so both directions finish independently.",
        "RST immediately tears down a connection when an invalid segment arrives or on abort.",
    ],
    [
        "Client state progresses SYN-SENT to ESTABLISHED; server from SYN-RECEIVED to ESTABLISHED.",
        "The accept queue holds fully established connections waiting for application accept().",
        "Active close sends FIN first; passive close may only ACK until it sends its FIN.",
        "TIME-WAIT on the side that sent the last ACK prevents old duplicates from starting new incarnations.",
    ],
    """sequenceDiagram
  participant C as Client
  participant S as Server
  C->>S: SYN seq=x
  S->>C: SYN_ACK seq=y ack=x+1
  C->>S: ACK ack=y+1""",
    T005_FACTS,
    "examples/d04_t005_handshake.py",
    "# Educational: observe with tcpdump 'tcp[tcpflags] & tcp-syn != 0'\nprint('use capture tools')",
    ["Drawing handshake with only two steps", "Claiming TIME-WAIT is always on server", "Ignoring SYN backlog limits", "Using RST as normal close", "Forgetting ack numbers increment by one on SYN/FIN"],
    ["Count SYN retransmits", "Check listen backlog and somaxconn", "Map FIN-WAIT and TIME-WAIT with ss -tan", "Correlate with LB idle timeout"],
    [("Graceful FIN close", "Clean accounting", "TIME-WAIT wait", "HTTP keep-alive end", "Hard kill pods"), ("RST abort", "Fast teardown", "Data loss risk", "Invalid state recovery", "Normal user logout")],
    ["SYN SYN-ACK ACK opens TCP", "FIN and ACK close gracefully", "TIME-WAIT waits 2MSL on active closer", "RST aborts immediately", "Pool connections to skip handshakes"],
    "Understand before: `D04-T004`.\nSupports: `D04-T008` states.\nOften confused with: TLS handshake.",
    ["Draw three-way handshake with sequence numbers", "Explain why TIME-WAIT exists", "Contrast FIN close with RST", "Name SYN flood mitigation", "Relate handshake RTT to API latency"],
)

# Generate T006-T023 with mk using topic-specific fact blocks (condensed)
def topic_facts(lines):
    fb = facts_block(*lines)
    while len(fb) < 92:
        fb.append(fb[len(fb) % max(1, len(fb)//2)])
    return fb[:92]


TOPIC_LINES = {
    "D04-T006": (
        "Sequence numbers label bytes in a TCP stream; acknowledgments are cumulative for in-order data.",
        "Retransmissions occur on timeout or duplicate ACK signals indicating gaps.",
        "Selective repeat and SACK improve recovery versus go-back-n alone.",
        "Out-of-order segments buffer until holes fill.",
        "Duplicate ACKs trigger fast retransmit after typically three duplicates.",
        "RTT estimators set RTO; spurious retransmits hurt performance.",
        "Nagle's algorithm coalesces small writes; TCP_NODELAY disables for latency.",
        "Window size limits unacknowledged data; zero window probes continue flow.",
        "Application backpressure fills send buffers when consumer is slow.",
        "Packet loss from congestion reduces cwnd; not always radio loss.",
        "Capture shows retransmits with identical seq or SACK blocks.",
        "Database protocols rely on TCP retransmission not app retries for bytes.",
        "TLS records split across TCP segments; retransmit is transparent.",
        "Load balancers must preserve seq stream when not terminating TCP.",
        "Previous handshake sets initial ISN; seq wraps on long connections.",
        "Next flow and congestion control builds on seq/ack.",
        "API latency spikes when loss causes retransmits on wide paths.",
    ),
    "D04-T007": (
        "Flow control uses receive window advertised in ACKs to match sender to receiver buffer.",
        "Congestion control adjusts sending rate based on loss and delay signals.",
        "Reno and CUBIC are common Linux algorithms; BBR uses bandwidth and RTT.",
        "Slow start grows cwnd exponentially until loss or ssthresh.",
        "Fast recovery avoids full slow start after fast retransmit.",
        "Bufferbloat inflates delay when queues are too large.",
        "Tuning sysctl net.ipv4.tcp_* affects servers globally.",
        "Microservices many flows share bottleneck links.",
        "Previous seq/ack implements reliability; congestion shares network fairly.",
        "Next TIME-WAIT is unrelated but close timing interacts with lingering bytes.",
        "Interview contrasts flow versus congestion window.",
    ),
    "D04-T008": (
        "TCP states include LISTEN, SYN-SENT, SYN-RECEIVED, ESTABLISHED, FIN-WAIT-1, FIN-WAIT-2, CLOSE-WAIT, CLOSING, LAST-ACK, TIME-WAIT, CLOSED.",
        "TIME-WAIT is entered by the endpoint that sends the final ACK in active close.",
        "Duration is 2*MSL; Linux commonly uses 60 seconds with MSL 30 seconds unless tuned.",
        "Purpose: allow late duplicates from the old connection to expire without confusing a new incarnation with the same quadruple.",
        "High TIME-WAIT counts on clients after many short connections are normal; on servers investigate close pattern.",
        "SO_REUSEADDR allows bind while TIME-WAIT on server with caution.",
        "tcp_tw_reuse on Linux reuses TIME-WAIT sockets for outgoing connections only in specific cases.",
        "Lingering close versus RST affects state transitions.",
        "Previous congestion topic does not change TIME-WAIT rules.",
        "Next HTTP keep-alive reduces close frequency.",
        "Debug with ss -tan state time-wait | wc -l.",
    ),
    "D04-T009": (
        "HTTP/1.1 uses text requests on a TCP connection; persistent connections reuse TCP with keep-alive.",
        "Head-of-line blocking: one large response delays others on same HTTP/1.1 connection.",
        "HTTP/2 multiplexes streams over one TCP connection with binary framing and HPACK compression.",
        "HTTP/2 still suffers TCP-level head-of-line blocking on loss.",
        "HTTP/3 maps streams to QUIC over UDP with independent loss recovery per stream.",
        "ALPN negotiates h2 or http/1.1 during TLS handshake.",
        "Server push in HTTP/2 is largely deprecated in favor of preload hints.",
        "Prioritization in HTTP/2 helps critical assets.",
        "Previous TCP states affect connection reuse.",
        "Next methods and status codes sit above versions.",
        "Choose version per client support and intermediaries.",
    ),
    "D04-T010": (
        "Safe methods include GET, HEAD, OPTIONS; POST is not cache-safe by default.",
        "PUT replaces; PATCH partial update; DELETE removes.",
        "Idempotency: repeat PUT same effect; POST may create duplicates.",
        "Status 2xx success, 3xx redirection, 4xx client error, 5xx server error.",
        "Headers carry metadata: Content-Type, Authorization, trace context.",
        "Hop-by-hop headers differ from end-to-end.",
        "Conditional requests use If-Match and If-None-Match.",
        "Previous HTTP versions transport these semantics.",
        "Next caching specializes on cache headers.",
        "Design APIs with clear method semantics.",
    ),
    "D04-T011": (
        "Cache-Control directives include max-age, no-store, no-cache, private, public, s-maxage.",
        "no-store forbids storing; no-cache allows store but requires revalidation before use.",
        "ETag validators enable If-None-Match returning 304.",
        "Last-Modified is weaker validator than ETag.",
        "Vary header keys cache by request headers like Accept-Encoding.",
        "CDN caches respect s-maxage for shared caches.",
        "stale-while-revalidate serves stale while fetching fresh.",
        "Heuristic caching applies when max-age missing.",
        "Previous methods define what is cacheable.",
        "Next DNS affects cache location at edge.",
        "Mis-cached personalized data is a privacy bug.",
    ),
    "D04-T012": (
        "DNS resolves names to records: A, AAAA, CNAME, MX, TXT, NS, SRV.",
        "Resolvers recurse starting at root hints; authoritative servers answer for zones.",
        "TTL controls caching duration; low TTL speeds failover, raises query load.",
        "CNAME chains add latency; apex often uses ALIAS/ANAME at providers.",
        "DNS over UDP with truncation triggers TCP retry.",
        "DNSSEC signs records; still need HTTPS for confidentiality.",
        "Negative caching uses SOA minimum TTL.",
        "Previous HTTP caching differs from DNS caching.",
        "Next TLS needs correct name in certificate.",
        "Debug with dig +trace and compare resolvers.",
    ),
    "D04-T013": (
        "TLS handshake negotiates version, ciphers, and authenticates server (and optionally client).",
        "TLS 1.3 reduces round trips: often one RTT for handshake; 0-RTT resumption has replay risk.",
        "Key exchange uses ephemeral keys; symmetric keys protect bulk data.",
        "Application data waits until handshake completes except 0-RTT early data.",
        "ALPN selects HTTP version.",
        "Session tickets enable resumption.",
        "Previous DNS gets you to the right host.",
        "Next certificates explain PKI.",
        "Terminate TLS at edge or app is architecture choice.",
    ),
    "D04-T014": (
        "X.509 certificates bind public keys to names signed by a CA.",
        "Private keys stay on server or HSM; never commit to git.",
        "Chain validation builds to trusted root store.",
        "mTLS uses client certificates for service identity.",
        "OCSP stapling reduces client lookup latency.",
        "Short-lived certs reduce compromise blast radius.",
        "Previous TLS handshake presents the cert.",
        "Next encryption types explain algorithms inside TLS.",
        "Mis-issued or expired certs break HTTPS entirely.",
    ),
    "D04-T015": (
        "Symmetric ciphers encrypt bulk data fast with shared keys.",
        "Asymmetric crypto secures key exchange and signatures with key pairs.",
        "TLS uses both: asymmetric handshake, symmetric record protection.",
        "AES-GCM and ChaCha20-Poly1305 are common AEAD suites.",
        "RSA key transport is legacy; ECDHE preferred.",
        "Do not roll your own crypto.",
        "Previous PKI provides keys.",
        "Next WebSockets may use same TLS connection.",
        "Pick libraries and modern cipher suites only.",
    ),
    "D04-T016": (
        "WebSockets upgrade HTTP to full-duplex framed messages over one TCP connection.",
        "SSE is server-to-client one-way over HTTP with text/event-stream.",
        "WebSockets need load balancer TCP/WebSocket support and idle timeouts.",
        "SSE works through many HTTP proxies and auto-reconnects.",
        "Backpressure differs: WS application-level, SSE browser driven.",
        "Authentication often uses cookies on upgrade or tokens.",
        "Previous TLS secures the transport.",
        "Next long polling compares for fanout.",
        "Choose WS for bidirectional games; SSE for feeds.",
    ),
    "D04-T017": (
        "Long polling holds HTTP request until event or timeout.",
        "Simpler than WS but higher overhead per event.",
        "Timeouts must align with LB and client.",
        "Many hanging requests consume server threads or connections.",
        "Comet patterns batch events.",
        "Previous WS/SSE are alternatives.",
        "Next REST versus gRPC for RPC style.",
        "Use message bus for scale instead of infinite polls.",
    ),
    "D04-T018": (
        "REST uses HTTP resources, verbs, and representations like JSON.",
        "gRPC uses HTTP/2 framing, protobuf contracts, and strong typing.",
        "REST easier to debug with curl; gRPC needs tooling.",
        "gRPC supports streaming RPCs natively.",
        "Browser gRPC needs grpc-web gateway.",
        "Version REST with URLs or headers; gRPC with protobuf compatibility rules.",
        "Previous polling transports events; RPC is request-response.",
        "Next proxies route both styles.",
        "Pick REST for public APIs; gRPC internal east-west.",
    ),
    "D04-T019": (
        "Forward proxy serves clients; reverse proxy sits before servers.",
        "Reverse proxies terminate TLS, route, and add headers.",
        "Load balancers distribute with algorithms round-robin, least conn, hash.",
        "Health checks remove bad backends.",
        "Sticky sessions tie client to backend via cookie or IP hash.",
        "Previous API styles hit the proxy first.",
        "Next NAT/firewall interact with paths.",
        "X-Forwarded-For and Proto preserve client metadata.",
    ),
    "D04-T020": (
        "NAT maps private to public addresses; SNAT for outbound, DNAT for inbound.",
        "Connection tracking ties translations to TCP/UDP flows.",
        "Firewalls filter by 5-tuple and state.",
        "Security groups are stateful allow lists in cloud.",
        "Port exhaustion on NAT gateways causes failures.",
        "Previous LB public IPs use NAT patterns.",
        "Next CDN places caches globally.",
        "Document open ports per tier.",
    ),
    "D04-T021": (
        "CDNs cache static and cacheable API responses at edge PoPs.",
        "Origin shield reduces load on primary.",
        "Cache keys include URL, query, and Vary headers.",
        "Purges invalidate objects globally with delay.",
        "TLS at edge with shared or dedicated certs.",
        "Previous NAT and LB feed traffic into CDN.",
        "Next pooling reduces origin connections.",
        "Geo routing sends users to nearest PoP.",
    ),
    "D04-T022": (
        "HTTP keep-alive reuses TCP for multiple requests.",
        "Client and server pools maintain warm connections to databases and HTTP origins.",
        "Pool size balances memory and handshake cost.",
        "Idle timeouts close unused sockets.",
        "TLS session resumption pairs with TCP reuse.",
        "Previous CDN reduces need for client-origin TCP.",
        "Next metrics define latency versus bandwidth.",
        "Mis-sized pools cause SYN storms or queueing.",
    ),
    "D04-T023": (
        "Latency is delay per operation; bandwidth is max data rate.",
        "Throughput is achieved data rate including protocol overhead.",
        "Packet loss triggers TCP backoff reducing throughput.",
        "RTT bounds time for small messages regardless of bandwidth.",
        "BDP bandwidth-delay product guides buffer sizing.",
        "Measure with percentiles not averages.",
        "Previous pooling affects observed latency.",
        "Caps domain 4 networking fundamentals.",
        "Use tracing to split DNS TLS TTFB.",
    ),
}

SLUGS = {
    "D04-T006": "d04-t006-sequence-numbers-acks-retransmission",
    "D04-T007": "d04-t007-flow-control-and-congestion-control",
    "D04-T008": "d04-t008-tcp-connection-states-and-time-wait",
    "D04-T009": "d04-t009-http-1-1-http-2-http-3",
    "D04-T010": "d04-t010-http-methods-headers-status-codes",
    "D04-T011": "d04-t011-http-caching-semantics",
    "D04-T012": "d04-t012-dns-resolution-and-record-types",
    "D04-T013": "d04-t013-tls-ssl-handshake",
    "D04-T014": "d04-t014-certificates-cas-public-private-keys",
    "D04-T015": "d04-t015-symmetric-vs-asymmetric-encryption",
    "D04-T016": "d04-t016-websockets-and-server-sent-events",
    "D04-T017": "d04-t017-long-polling",
    "D04-T018": "d04-t018-rest-vs-grpc",
    "D04-T019": "d04-t019-proxies-reverse-proxies-and-load-balancers",
    "D04-T020": "d04-t020-nat-firewalls-and-ports",
    "D04-T021": "d04-t021-cdn-and-edge-networking",
    "D04-T022": "d04-t022-connection-pooling-and-keep-alive",
    "D04-T023": "d04-t023-latency-bandwidth-throughput-and-packet-loss",
}

DEPS = {
    "D04-T006": ["D04-T005", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T007": ["D04-T006", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T008": ["D04-T007", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T009": ["D04-T008", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T010": ["D04-T009", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T011": ["D04-T010", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T012": ["D04-T011", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T013": ["D04-T012", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T014": ["D04-T013", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T015": ["D04-T014", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T016": ["D04-T015", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T017": ["D04-T016", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T018": ["D04-T017", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T019": ["D04-T018", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T020": ["D04-T019", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T021": ["D04-T020", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T022": ["D04-T021", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    "D04-T023": ["D04-T022", "D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
}

NAMES = {k: k.split("-", 1)[1].replace("-", " ").title() for k in SLUGS}
# fix names from inventory
NAMES.update({
    "D04-T006": "Sequence numbers, ACKs, retransmission",
    "D04-T007": "Flow control and congestion control",
    "D04-T008": "TCP connection states and TIME_WAIT",
    "D04-T009": "HTTP/1.1, HTTP/2, HTTP/3",
    "D04-T010": "HTTP methods, headers, status codes",
    "D04-T011": "HTTP caching semantics",
    "D04-T012": "DNS resolution and record types",
    "D04-T013": "TLS/SSL handshake",
    "D04-T014": "Certificates, CAs, public/private keys",
    "D04-T015": "Symmetric vs asymmetric encryption",
    "D04-T016": "WebSockets and Server-Sent Events",
    "D04-T017": "Long polling",
    "D04-T018": "REST vs gRPC",
    "D04-T019": "Proxies, reverse proxies and load balancers",
    "D04-T020": "NAT, firewalls and ports",
    "D04-T021": "CDN and edge networking",
    "D04-T022": "Connection pooling and keep-alive",
    "D04-T023": "Latency, bandwidth, throughput and packet loss",
})

MERMAID = {
    "D04-T006": "flowchart TD\n  send[Sender_buffer]\n  net[Network]\n  recv[Receiver_reorder]\n  send --> net --> recv",
    "D04-T007": "flowchart LR\n  rwnd[Receive_window]\n  cwnd[Congestion_window]\n  rate[Send_rate]\n  rwnd --> rate\n  cwnd --> rate",
    "D04-T008": "stateDiagram-v2\n  [*] --> ESTABLISHED\n  ESTABLISHED --> TIME_WAIT: active_close\n  TIME_WAIT --> [*]",
    "D04-T009": "flowchart TD\n  h11[HTTP1_1_TCP]\n  h2[HTTP2_multiplex_TCP]\n  h3[HTTP3_QUIC_UDP]\n  h11 --> h2 --> h3",
    "D04-T010": "flowchart LR\n  client[Client]\n  method[Method_and_headers]\n  server[Server]\n  client --> method --> server",
    "D04-T011": "flowchart TD\n  browser[Client_cache]\n  cdn[Shared_cache]\n  origin[Origin]\n  browser --> cdn --> origin",
    "D04-T012": "flowchart TD\n  stub[Stub_resolver]\n  recurse[Recursive_resolver]\n  auth[Authoritative_NS]\n  stub --> recurse --> auth",
    "D04-T013": "sequenceDiagram\n  participant C as Client\n  participant S as Server\n  C->>S: ClientHello\n  S->>C: ServerHello_and_cert\n  C->>S: Finished",
    "D04-T014": "flowchart TD\n  leaf[Leaf_cert]\n  inter[Intermediate_CA]\n  root[Trusted_root]\n  leaf --> inter --> root",
    "D04-T015": "flowchart LR\n  asym[Asymmetric_handshake]\n  sym[Symmetric_bulk]\n  asym --> sym",
    "D04-T016": "flowchart TD\n  ws[WebSocket_duplex]\n  sse[SSE_server_push]\n  http[HTTP_upgrade]\n  http --> ws\n  http --> sse",
    "D04-T017": "sequenceDiagram\n  participant C as Client\n  participant S as Server\n  C->>S: HTTP_request\n  Note over S: hold_until_event\n  S->>C: HTTP_response",
    "D04-T018": "flowchart LR\n  rest[REST_JSON_HTTP]\n  grpc[gRPC_proto_HTTP2]\n  rest --- grpc",
    "D04-T019": "flowchart TD\n  user[Clients]\n  rev[Reverse_proxy_LB]\n  pods[Backend_pool]\n  user --> rev --> pods",
    "D04-T020": "flowchart LR\n  priv[Private_subnet]\n  nat[NAT_gateway]\n  pub[Public_Internet]\n  priv --> nat --> pub",
    "D04-T021": "flowchart TD\n  eyeball[Users]\n  edge[CDN_PoP]\n  origin[Origin_region]\n  eyeball --> edge --> origin",
    "D04-T022": "flowchart TD\n  pool[Connection_pool]\n  warm[Keep_alive_sockets]\n  origin[Upstream]\n  pool --> warm --> origin",
    "D04-T023": "flowchart LR\n  rtt[RTT_latency]\n  bw[Bandwidth]\n  tput[Throughput]\n  rtt --> tput\n  bw --> tput",
}

def build_rest():
    out = [T002, T003, T004, T005]
    for tid in [f"D04-T{i:03d}" for i in range(6, 24)]:
        lines = TOPIC_LINES[tid]
        fb = topic_facts(*lines)
        name = NAMES[tid]
        imp = "advanced" if tid == "D04-T020" else "core"
        comp = "advanced" if tid == "D04-T020" else "intermediate"
        out.append(
            mk(
                tid,
                name,
                SLUGS[tid],
                DEPS[tid],
                lines[0],
                [lines[1] if len(lines) > 1 else lines[0], lines[2] if len(lines) > 2 else lines[0], lines[3] if len(lines) > 3 else lines[0], lines[4] if len(lines) > 4 else lines[0]],
                [lines[5] if len(lines) > 5 else "Kernel and libraries implement this behavior on servers.", lines[6] if len(lines) > 6 else "Cloud networks add overlays and security policy.", lines[7] if len(lines) > 7 else "Observability hooks include metrics and captures.", lines[8] if len(lines) > 8 else "Misconfiguration often looks like intermittent TCP failures."],
                MERMAID[tid],
                fb,
                f"examples/{SLUGS[tid].replace('-', '_')}.py",
                f'print("see topic {tid}")',
                [f"Misunderstanding {name} basics", "Skipping captures at the right layer", "Tuning without measuring", "Ignoring security interactions", "Assuming defaults match all clouds"],
                ["Start from symptoms and layer", "Use dig curl openssl ss as appropriate", "Compare regions and networks", "Roll back risky sysctl changes"],
                [("Default stack settings", "Works out of box", "May not fit workload", "Standard web APIs", "Ultra-low latency custom"), ("Aggressive tuning", "Higher throughput", "Fragile upgrades", "Known bottlenecks", "Unmeasured guesses")],
                [lines[0], lines[min(1, len(lines)-1)], "Relate to adjacent D04 topics", "Measure before optimizing", "Document edge behavior"],
                f"Understand before: `{DEPS[tid][0]}`.\nSee also: `D04-T001` layering.\nOften confused with: adjacent transport versus application concerns.",
                [f"Explain {name} in a request path", f"Name one tool to debug {name}", f"State one trade-off for {name}", "Tie to production incident pattern", "Connect to following D04 topic"],
            )
        )
        if tid == "D04-T020":
            out[-1].importance = "advanced"
            out[-1].complexity = "advanced"
    return out

SPECS_REST = build_rest()
# fmt: on
