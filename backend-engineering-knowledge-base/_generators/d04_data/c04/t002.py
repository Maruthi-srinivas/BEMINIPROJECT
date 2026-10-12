from ..topic_builder import TopicSpec
from ..topic_factory import A

SPEC = TopicSpec(
    id="D04-T002",
    name="IP addressing, subnetting, CIDR",
    subdomain="IP addressing, subnetting, CIDR",
    slug="d04-t002-ip-addressing-subnetting-cidr",
    deps=["D04-T001", "D01-T001", "D01-T002", "D03-T001", "D03-T002"],
    elevator="IP addresses identify interfaces on a network; CIDR notation expresses prefix length so routers know which bits are network versus host.",
    principles=[
        "IPv4 addresses are 32-bit integers usually written in dotted decimal. The subnet mask or prefix length tells devices which portion identifies the network.",
        "Private ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are not routed on the public Internet; NAT maps them to public addresses.",
        "IPv6 uses 128-bit addresses and typically allocates /64 subnets to links, reducing NAT dependence but changing address planning.",
        "Longest-prefix match selects the most specific route when multiple entries overlap.",
    ],
    internals=[
        "When a host sends to another IP, it compares destination to local subnets. On-link traffic uses ARP; off-link traffic goes to the default gateway.",
        "Cloud VPCs attach route tables to subnets; security groups filter by IP and port at the hypervisor.",
        "CIDR aggregation reduces routing table size by summarizing contiguous blocks.",
        "Mis-sized subnets exhaust IPs or force painful migrations; plan for load balancers and managed services that consume addresses.",
    ],
    mermaid="""flowchart LR
  host[AppHost_10_0_1_5]
  gw[DefaultGateway_10_0_1_1]
  internet[PublicInternet]
  host -->|off_subnet| gw
  gw --> internet""",
    examples=[
        "A /24 provides 256 addresses, but usable hosts are fewer once network, gateway, and broadcast/reserved addresses are accounted for depending on platform.",
        "Backend pods in Kubernetes receive cluster IPs distinct from node IPs; service CIDR planning prevents overlap with VPC CIDR.",
        "Do not hard-code public IPs in config; use DNS names and let addressing change.",
    ],
    code_file="examples/d04_t002_cidr.py",
    code="""import ipaddress

def hosts_in_prefix(cidr: str) -> int:
    net = ipaddress.ip_network(cidr, strict=False)
    return net.num_addresses


if __name__ == "__main__":
    print(hosts_in_prefix("10.0.1.0/24"))""",
    practical=[
        "Document every environment VPC CIDR and peerings to avoid overlapping ranges that break VPN and mesh routing.",
        "Health checks from load balancers need free IPs in target subnets.",
        "Observability: log source IP after trusting only validated X-Forwarded-For from known proxies.",
    ],
    tradeoff_rows=[
        ("Large /16 per VPC", "Room to grow", "Wastes address space", "Early cloud adoption", "Tight IP conservation"),
        ("Many small subnets", "Isolation", "Complex routing", "Tiered security zones", "Tiny dev accounts"),
        ("IPv6 only", "Huge address space", "Legacy IPv4 clients", "Greenfield mobile", "B2B with IPv4-only partners"),
        ("NAT gateway", "Outbound IPv4 from private subnets", "Cost and SNAT port limits", "Private workloads", "Need inbound static IPs without LB"),
    ],
    mistakes=[
        "Overlapping CIDR between peered VPCs breaks routing silently for some flows.",
        "Forgetting broadcast/reserved addresses when sizing subnets.",
        "Treating RFC1918 addresses as globally unique across merged networks.",
        "Using /32 rules everywhere instead of security groups tied to groups.",
        "Confusing network address with any host address in the block.",
    ],
    debugging=[
        "Symptom: TCP hangs to a private IP from the wrong subnet—verify route tables and peering accepter routes.",
        "Use `ip route` or cloud console effective routes to see next hop.",
        "Traceroute shows where packets stop; compare with security group rules on that hop.",
        "Long-term: IPAM spreadsheet; short-term: fix asymmetric routing or missing return path.",
    ],
    beginner=[
        ("What is CIDR?", A("CIDR writes an IP prefix with a slash length like /24.", "The length counts network bits from the left.", "It replaces old classful A/B/C assumptions.", "Routers longest-prefix-match on these blocks."), "What is CIDR?"),
        ("What is a private IP?", A("Private ranges are reserved for local networks.", "They are not globally routable on the public Internet.", "NAT translates them for outbound traffic.", "Backends in VPCs almost always use private addresses."), "Private IP ranges"),
        ("What is a default gateway?", A("It is the router IP used for off-subnet destinations.", "Hosts compare destination to subnet mask to decide on-link versus gateway.", "Wrong gateway causes blackholes or asymmetric paths.", "In cloud, the gateway is the VPC router for the subnet."), "Default gateway"),
        ("How many hosts in a /24?", A("A /24 has 256 total addresses in the block.", "Cloud platforms reserve some for network, gateway, and DNS.", "Plan fewer usable addresses than 254.", "Size subnets with growth and load balancers in mind."), "Hosts in /24"),
        ("Why do we subnet?", A("Subnets segment broadcast domains and apply policy.", "Security groups and ACLs attach per subnet.", "Routing summarizes traffic between segments.", "Microservices use many small subnets for blast radius."), "Why subnet"),
    ],
    intermediate=[
        ("Explain longest-prefix match.", A("Routers choose the route with the most specific matching prefix.", "A /24 beats a /16 when both match.", "This enables aggregation and exceptions.", "Misconfigured summaries send traffic the wrong way."), "Longest-prefix match"),
        ("How does SNAT affect outbound connections?", A("NAT gateways map many private IPs to fewer public IPs.", "Ephemeral source ports multiplex flows.", "Exhausting ports causes connection failures under heavy load.", "Monitor SNAT port allocation on cloud NAT appliances."), "SNAT behavior"),
        ("IPv4 versus IPv6 for backends?", A("IPv6 removes NAT for many designs with global addresses.", "Dual-stack adds complexity but aids transition.", "Libraries and firewalls must allow both.", "DNS A and AAAA records must stay consistent."), "IPv4 vs IPv6"),
        ("What is IPAM?", A("IP address management tracks allocations across clouds.", "It prevents overlaps during mergers and peerings.", "Automation pulls from IPAM for Terraform.", "Without IPAM, teams rediscover conflicts during incidents."), "IPAM"),
        ("How do security groups relate to IPs?", A("They filter L4 traffic to ENIs or instances.", "Rules reference CIDR blocks or other groups.", "They are stateful for allowed flows in AWS.", "Misrules look like network flakiness but are policy."), "Security groups"),
    ],
    advanced=[
        ("Why can overlapping VPN CIDR break only some services?", A("Longest match may route overlapping ranges inconsistently per host.", "Some peers attract traffic that never reaches the intended subnet.", "TCP may SYN to a wrong endpoint that RSTs.", "Fix by renumbering or summarizing with null routes."), "VPN overlap"),
        ("Explain anycast VIP.", A("Same IP announced from multiple sites via BGP.", "Clients reach the nearest PoP.", "TCP connections stay on one site for the flow lifetime.", "Health checks must withdraw routes on failure."), "Anycast VIP"),
        ("How does /32 host routing work?", A("Some systems install host routes for individual IPs.", "Kubernetes or BGP can advertise /32s.", "Tables grow; lookup cost rises.", "Use aggregation where possible."), "/32 host routes"),
        ("Path MTU and IP?", A("PMTUD discovers the smallest MTU on a path using ICMP.", "Blocking ICMP breaks discovery and causes blackhole MTU issues.", "TCP MSS clamping on VPNs prevents fragmentation.", "Tune MTU on overlays like IPSec."), "PMTUD"),
        ("Dual-stack pitfalls?", A("Happy Eyeballs may prefer IPv6 or IPv4 per OS.", "Firewalls might allow one family only.", "Logs must record address family.", "Test both paths in CI."), "Dual-stack pitfalls"),
    ],
    scenarios=[
        ("New microservice cannot reach RDS in same VPC.", A("Verify security group sources include the service subnet CIDR or group.", "Confirm RDS subnet route table has local VPC route.", "DNS may point to wrong interface.", "Test with telnet/openssl from the same task ENI."), "RDS connectivity"),
        ("Peering added but one direction fails.", A("Peering is non-transitive and needs routes on both sides.", "Return traffic may lack a route to the source subnet.", "NACLs can block replies.", "Draw source and destination subnet paths separately."), "Peering one-way"),
        ("Kubernetes pods cannot reach external SaaS.", A("Check NAT gateway and route 0.0.0.0/0.", "Egress proxy may require different subnet.", "DNS must resolve publicly.", "Corporate firewall may block new CIDR egress."), "Pod egress"),
        ("Latency spikes after shrinking subnet.", A("SNAT port exhaustion causes SYN delays or failures.", "More instances share fewer mapped ports.", "Spread across NAT gateways or widen pools.", "Watch cloud NAT metrics."), "SNAT exhaustion"),
        ("Terraform apply warns CIDR overlap.", A("Stop before apply; overlapping VPC CIDR cannot peer cleanly.", "Pick unused RFC1918 block from IPAM.", "Migrating live CIDR is painful.", "Renumber dev first to validate."), "Terraform overlap"),
    ],
    follow_ups=[
        ("Link to ARP?", A("On-link IPv4 delivery needs MAC addresses from ARP.", "Off-link traffic goes to gateway MAC.", "See `D04-T003`.", "IP alone does not deliver frames."), "ARP link"),
        ("Link to TCP?", A("TCP endpoints are IP plus port.", "Routing must work before SYN.", "See `D04-T004`.", "Firewalls filter on both."), "TCP link"),
        ("Cloud networking docs?", A("Each provider documents implicit routers and reserved IPs.", "Read platform limits per subnet.", "Align with `D04-T019` load balancers.", "Design reviews should include CIDR diagram."), "Cloud docs"),
    ],
    exercises=[
        ("Given 10.0.0.0/16, carve three /24 subnets for app, data, and public tiers without overlap. List network addresses.", "Three distinct /24 network IDs inside the /16."),
        ("A service in 10.0.1.0/24 cannot reach 10.0.2.50; routes are local. What two non-application checks run first?", "Security group/NACL and host firewall on port."),
        ("Choose /20 versus /24 for a GKE subnet with 200 nodes and many services. Justify.", "Mentions IP consumption and alias ranges."),
    ],
    solutions=[
        "Example: 10.0.1.0/24 app, 10.0.2.0/24 data, 10.0.3.0/24 public—all contained in 10.0.0.0/16.",
        "Verify L4 rules allow egress/ingress on the service port; confirm RDS SG inbound includes app SG or CIDR.",
        "A /20 provides more pod/service IPs if secondary ranges are used; /24 may be tight—document max pods per node impact.",
    ],
    revision_items=[
        "CIDR prefix length defines network bits.",
        "Private addresses need NAT for public Internet.",
        "Longest-prefix match picks routes.",
        "Plan subnets for gateways and LB consumption.",
        "Avoid overlapping peered CIDR.",
    ],
    related="Understand before: `D04-T001` layers.\nSupports: `D04-T003` ARP, `D04-T020` NAT/firewalls.\nOften confused with: MAC addresses versus IP.",
    completion=[
        "Compute whether two IPs share a /24.",
        "Explain why peering needs routes both ways.",
        "Size a subnet given instance count and reserves.",
        "Debug asymmetric routing symptoms.",
        "Contrast private IP with elastic public IP.",
    ],
)
