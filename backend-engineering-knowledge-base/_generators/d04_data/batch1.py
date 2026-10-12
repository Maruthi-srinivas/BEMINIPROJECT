"""D04-T001 through D04-T006 topic definitions."""

from .topic_factory import A, make_topic, q

COMMON_DEPS = ["`D01-T001`", "`D01-T002`", "`D03-T001`", "`D03-T002`"]


def _interview(*groups):
    keys = ["beginner", "intermediate", "advanced", "scenarios", "follow_ups"]
    return {k: list(g) for k, g in zip(keys, groups)}


def topic_001():
    return make_topic(
        id="D04-T001",
        name="OSI and TCP/IP models",
        subdomain="OSI and TCP/IP models",
        note_path="03_COMPUTER_NETWORKS/notes/d04-t001-osi-and-tcp-ip-models.md",
        importance="core",
        complexity="intermediate",
        deps=["D01-T001", "D01-T002", "D03-T001", "D03-T002"],
        overview=[
            "Layered network models describe how bits move from an application on one host to an application on another without every program reimplementing Ethernet, routing, and reliability.",
            "The OSI model has seven layers; the TCP/IP model used on the Internet collapses some of them into four practical layers: link, internet, transport, and application.",
            "The concept exists because heterogeneous hardware and protocols must interoperate. Each layer exposes a service to the layer above and hides its own mechanics.",
            "In backend interviews you use layers to localize failures: DNS and TLS issues are usually application or session concerns, while packet loss and retransmits belong to transport.",
            "Prerequisites: basic programming and operating-system process and socket concepts (`D03-T001`). Later topics such as TCP (`D04-T004`) and HTTP (`D04-T009`) assume you can name which layer they occupy.",
        ],
        first_principles=[
            "At the physical layer, signals on a wire or radio carry bits. The link layer frames those bits for a local network segment and uses addresses like MAC. The network layer (IP) forwards datagrams across routers using logical addresses. The transport layer (TCP or UDP) multiplexes applications with ports and optionally provides reliability. The application layer encodes HTTP, DNS, TLS records, and business payloads.",
            "Encapsulation means each layer adds a header (and sometimes a trailer) around the payload from the layer above. A TCP segment becomes the payload of an IP packet, which becomes the payload of an Ethernet frame. On receive, each layer strips its header and passes the remainder upward.",
            "The OSI model separates presentation and session layers that TCP/IP often folds into application protocols. TLS sits logically between HTTP and TCP even though we colloquially say HTTPS is application layer.",
            "Why it works: fixed interfaces between layers let you swap Wi-Fi for fiber without rewriting HTTP servers. Limitations: real stacks blur lines (TCP congestion control interacts with IP routing), and security crosses layers.",
        ],
        internal=[
            "When a backend service calls `connect` on a TCP socket, the kernel transport layer builds SYN segments, IP chooses source and destination addresses and TTL, and the link layer resolves the next-hop MAC via ARP (`D04-T003`).",
            "Load balancers and NAT boxes terminate or translate at specific layers. An L4 balancer forwards TCP connections using IPs and ports. An L7 balancer parses HTTP and may terminate TLS.",
            "Data flow for an HTTPS GET: application forms HTTP request bytes, TLS encrypts them into TLS records, TCP segments and acknowledges, IP routes packets, link transmits frames.",
            "State is per layer: TCP connection state in the kernel, TLS session keys in the crypto library, HTTP keep-alive mapping in the server worker. Misattributing state causes bugs like fixing HTTP caching when the problem is DNS TTL.",
        ],
        mermaid="""flowchart TD
  app[Application_HTTP_TLS]
  transport[Transport_TCP_UDP]
  network[Network_IP]
  link[Link_Ethernet_WIFI]
  app --> transport
  transport --> network
  network --> link""",
        diagram_caption="Top-down encapsulation on send; bottom-up decapsulation on receive. TLS is drawn inside application because it wraps HTTP bytes before TCP.",
        examples=[
            "Analogy: international shipping uses nested containers. The product is the payload, the inner box is TCP, the pallet is IP, the truck is Ethernet. You track problems by which container was damaged.",
            "Backend example: a 502 from a gateway is often application or proxy layer, while `connection timed out` during SYN is transport or network reachability.",
            "Do not say OSI layer numbers from memory without mapping to TCP/IP. Interviewers prefer you explain encapsulation and where TLS and HTTP live.",
        ],
        code_intro="File: `examples/d04_t001_layers.py` — classify common backend strings by layer (educational, not executed).",
        code="""def layer_of(symptom: str) -> str:
    s = symptom.lower()
    if "dns" in s or "certificate" in s or "http/" in s:
        return "application"
    if "syn" in s or "reset" in s or "time_wait" in s:
        return "transport"
    if "ttl exceeded" in s or "no route" in s:
        return "network"
    if "arp" in s or "link down" in s:
        return "link"
    return "unknown"


if __name__ == "__main__":
    assert layer_of("HTTP/1.1 502 Bad Gateway") == "application"
    assert layer_of("SYN retransmits") == "transport"
    print("ok", layer_of("TTL exceeded in transit"))""",
        code_footer="How to run: `python examples/d04_t001_layers.py`. Expected: `ok network`. This file was not executed in the doc pipeline.",
        practical=[
            "When triaging production outages, write the failing hop and layer on the incident ticket. That stops the team from tuning TCP buffers when the root cause is an expired TLS certificate.",
            "Service meshes and sidecars intercept transport or application traffic depending on configuration; knowing the layer clarifies latency added per request.",
            "Observability: metrics at L7 (status codes, latency histograms) complement L4 (SYN counts) and synthetic DNS checks.",
        ],
        tradeoffs_table="""| Model | Benefit | Cost | Choose when | Avoid when |
| --- | --- | --- | --- | --- |
| OSI 7-layer | Fine-grained vocabulary | Easy to over-memorize | Teaching, security reviews | You need exact on-wire behavior |
| TCP/IP 4-layer | Matches Internet stacks | Hides presentation/session | Backend debugging | You need formal ISO terminology |
| End-to-end principle | Smart edges, dumb network | Harder in-house QoS | Internet-scale systems | Closed corporate WAN with strict QoS |
| Layer violation shortcuts | Performance (TOA, kernel bypass) | Fragile, hard to debug | Specialized appliances | General microservices |""",
        mistakes="""- Claiming TLS is always layer 6 only; explain it protects application bytes above TCP.
- Treating layers as separate programs; they are usually library and kernel modules in one host.
- Ignoring that NAT is a network-layer behavior that breaks naive peer-to-peer designs.
- Blaming application code for Ethernet CRC errors without checking link metrics.
- Memorizing OSI mnemonics without tying them to tcpdump symptoms.""",
        debugging=[
            "Symptom: API works from one datacenter but not another. Check DNS and routing (network/application) before rewriting service code.",
            "Capture a trace with tcpdump or Wireshark and identify the highest layer that shows errors (TLS alert versus TCP RST versus ICMP unreachable).",
            "Verify which component terminates TLS (app, ingress, CDN) to know where certificates and HTTP headers are observed.",
            "Long-term: document per-service layer diagram in the runbook; short-term: split checks into DNS, TCP connect, TLS handshake, HTTP status.",
        ],
        interview_levels=_interview(
            [
                q("beginner", "What problem do network layers solve?", A("Layers let builders swap link technologies without rewriting every application.", "Each layer offers a service contract to the layer above.", "Encapsulation hides details like MAC addresses from HTTP programmers.", "That separation is why the Internet scaled across Ethernet, Wi-Fi, and cellular."), "What problem do layers solve?"),
                q("beginner", "Name the four TCP/IP layers and one protocol in each.", A("Link carries frames (Ethernet).", "Internet routes packets (IPv4/IPv6).", "Transport delivers to ports (TCP/UDP).", "Application carries HTTP, DNS, and TLS-protected data."), "Name TCP/IP layers and protocols"),
                q("beginner", "What is encapsulation?", A("Each layer wraps the upper-layer PDU with its own header.", "A TCP segment is payload inside an IP packet.", "Receivers strip headers bottom-up.", "Malformed encapsulation shows up as checksumming or length errors at a specific layer."), "What is encapsulation?"),
                q("beginner", "Where does HTTP live in the stack?", A("HTTP is an application-layer protocol.", "It assumes a reliable byte stream, usually TCP.", "TLS encrypts HTTP bytes before they enter TCP.", "Proxies may terminate HTTP while TCP continues to another hop."), "Where does HTTP live?"),
                q("beginner", "What is the difference between OSI and TCP/IP models?", A("OSI has seven layers with explicit session and presentation.", "TCP/IP uses four layers aligned to real Internet stacks.", "Both teach the same idea: modular services.", "Interview answers should map concepts to TCP/IP unless asked for OSI numbers."), "OSI versus TCP/IP"),
            ],
            [
                q("intermediate", "Why is TLS not a perfect fit for a single OSI layer?", A("TLS provides encryption and authentication similar to presentation and session functions.", "It runs between HTTP and TCP on the same host.", "Middleboxes may inspect TLS metadata without parsing HTTP.", "Explain behavior (record encryption, handshakes) instead of forcing one OSI number."), "Why TLS spans layers"),
                q("intermediate", "How does an L4 load balancer differ from L7?", A("L4 forwards based on IP and port without parsing HTTP.", "L7 understands URLs, headers, and cookies for routing.", "L7 can terminate TLS and inject headers like X-Forwarded-For.", "Choose L4 for throughput and simplicity; L7 for routing and auth at the edge."), "L4 versus L7 balancers"),
                q("intermediate", "What does the end-to-end principle imply for backends?", A("Intelligence belongs in endpoints, not every router.", "Gateways should not assume the network is reliable or fair.", "Retries, timeouts, and idempotency live in services.", "Network appliances may still optimize, but apps must survive loss and delay."), "End-to-end principle for backends"),
                q("intermediate", "How do you decide if an outage is network or application?", A("Start with synthetic TCP connect and TLS handshake checks.", "Compare edge 5xx with origin health.", "Packet captures show whether failures happen before HTTP bytes.", "Correlate timestamps across layers to avoid fixing the wrong tier."), "Network versus application outage"),
                q("intermediate", "What headers does each layer add on the wire?", A("Ethernet adds MAC addresses.", "IP adds source and destination addresses and TTL.", "TCP adds ports, sequence numbers, and flags.", "TLS adds record headers; HTTP adds method, path, and headers."), "Headers per layer"),
            ],
            [
                q("advanced", "How can layering hurt performance in data centers?", A("Each layer adds parsing and copying in the kernel.", "Techniques like kernel bypass and TLS offload reduce CPU.", "They trade operational complexity for latency.", "Measure before bypassing; correctness and observability may regress."), "Layering performance cost"),
                q("advanced", "Why do tunnels (VPN, QUIC) complicate troubleshooting?", A("They wrap inner packets inside outer headers.", "Firewalls may see only the outer flow.", "Loss on the outer UDP path affects inner TCP unless the tunnel handles it.", "Document which layer your metrics represent."), "Tunnel troubleshooting"),
                q("advanced", "How do sidecars change the logical layer diagram?", A("A proxy sidecar intercepts outbound and inbound sockets.", "mTLS may run between sidecars while app speaks plain HTTP locally.", "The logical hop count increases even on localhost.", "Latency budgets must include extra TLS and serialization."), "Sidecars and layers"),
                q("advanced", "When is it valid to violate strict layering?", A("When standards like TCP offload or HTTP/2 prioritization need cross-layer hints.", "Violations should be explicit and documented.", "Hidden coupling makes upgrades risky.", "Prefer standards-based approaches over ad hoc shortcuts."), "Layer violations"),
                q("advanced", "How does ICMP relate to IP?", A("ICMP messages report delivery problems and support diagnostics like echo request.", "They are network-layer control messages carried inside IP.", "Path MTU discovery uses ICMP to avoid fragmentation.", "Blocking ICMP can break PMTUD and masquerade as TCP hangs."), "ICMP role"),
            ],
            [
                q("scenarios", "Users see HTTP 499 or client disconnects only on mobile networks.", A("Check TLS and HTTP timeouts at the app layer first.", "Also inspect TCP RTT and loss on cellular links.", "Middle boxes may buffer or reset idle flows.", "Compare server logs with client geography and network type."), "Mobile disconnect scenario"),
                q("scenarios", "A new VPC peering link works for ping but not HTTPS.", A("Ping uses ICMP while HTTPS needs TCP 443 and DNS resolution.", "Security groups may allow ICMP but block 443.", "TLS may fail on certificate name mismatch even when TCP connects.", "Walk the stack top-down after confirming routing tables."), "Peering works for ping not HTTPS"),
                q("scenarios", "Microservice A calls B over plain HTTP inside the mesh but mTLS outside.", A("Draw logical layers per hop.", "Inside the mesh, TLS may terminate at the sidecar.", "AuthZ policies might run at L7 on HTTP paths.", "Misconfigured SANs break TLS though TCP succeeds."), "Mesh HTTP versus mTLS"),
                q("scenarios", "After a firewall change, Kafka works but JDBC to RDS fails.", A("Both use TCP but on different ports and security groups.", "RDS may require TLS at the application protocol layer.", "Routing asymmetry can pass SYN but drop return traffic.", "Test each layer independently with nc or openssl s_client."), "Firewall change partial failure"),
                q("scenarios", "Support insists the network is fine because ping works.", A("Ping does not exercise application ports or TLS.", "Run layered checks: DNS, TCP connect, TLS, application RPC.", "Document evidence per layer for the incident.", "Escalate with captures, not opinions."), "Ping is not enough"),
            ],
            [
                q("follow_ups", "How does this connect to sockets (`D03`)?", A("Sockets are the API boundary into transport.", "Application code writes bytes; the kernel segments and routes.", "Understanding layers explains what `connect` and `read` actually do.", "See operating-system networking notes for syscall details."), "Link to sockets"),
                q("follow_ups", "What topic comes next in this domain?", A("IP addressing and CIDR (`D04-T002`) build on the network layer.", "You need CIDR to read cloud VPC diagrams.", "Routing decisions use prefixes, not MACs.", "Subnetting errors look like intermittent TCP timeouts."), "Next topic CIDR"),
                q("follow_ups", "How do CDNs change the layer picture?", A("CDNs terminate TCP and TLS closer to users.", "Origin sees fewer round trips but must trust edge caches.", "Caching is application-layer semantics with network placement.", "See `D04-T021` for edge design."), "CDNs and layers"),
            ],
        ),
        exercise_triplet=[
            (
                "Draw a layered diagram for HTTPS from browser to your API through an ingress controller. Label where TLS terminates and where HTTP is parsed.",
                "Diagram shows at least four layers and marks termination point.",
            ),
            (
                "Logs show TCP SYN retransmits to the database IP but HTTP health checks pass to the app. Which layer likely fails and what is your next test?",
                "You identify network or security-group path to DB port distinct from app HTTP.",
            ),
            (
                "Choose L4 versus L7 load balancing for a gRPC service with TLS passthrough. State one benefit and one operational cost.",
                "Answer mentions port-based routing versus HTTP/2-aware routing and certificate operations.",
            ),
        ],
        solution_bodies=[
            "TLS terminates at the ingress; HTTP is parsed there; TCP may continue separately to pods if TLS is re-encrypted. Label link/network inside the cluster CNI.",
            "SYN retransmits without HTTP involvement point to network ACL or wrong DB port. Test `nc -vz host 5432` from the app subnet; compare with curl to app health URL.",
            "L4 passthrough preserves end-to-end TLS and simplifies ingress CPU but loses path-based routing. L7 can inspect gRPC if TLS terminates at proxy, at the cost of cert management and latency.",
        ],
        revision="- Layers modularize the stack.\n- TCP/IP link, internet, transport, application.\n- TLS wraps HTTP above TCP.\n- Encapsulation on send, decapsulation on receive.\n- Debug top-down with layered checks.",
        related="Understand before: `D03-T001` processes and `D01-T001` data boundaries.\nSupports: `D04-T002` IP addressing, `D04-T009` HTTP versions.\nOften confused with: OSI numbers versus on-wire behavior.",
        completion="- Explain encapsulation with HTTP over TLS over TCP over IP.\n- Place common failures in the correct layer.\n- Compare L4 and L7 proxies with one example each.\n- Sketch a layered path through ingress to a pod.\n- Answer why ping alone does not prove HTTPS health.",
    )


TOPICS_BATCH1 = [topic_001()]
