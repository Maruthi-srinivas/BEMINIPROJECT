"""Computer networks cards, D04-T001 through D04-T023."""

from cards import CARDS, core


def add(tid: str, **kwargs: object) -> None:
    CARDS[tid] = core(name=kwargs.get("title", tid), **kwargs)


add(
    "D04-T001",
    title="OSI and TCP/IP models",
    definition="The OSI model is a seven-layer teaching model. The TCP/IP model is the four-layer stack the internet actually runs: link, internet, transport, and application.",
    problem="Without a layered model, every application would have to reimplement framing, routing, retransmission, and naming. Failures would be impossible to assign to a layer.",
    steps="A NIC frames bits on the link | IP routes packets using destination addresses | TCP or UDP multiplexes those packets onto ports | The application protocol, usually HTTP, interprets the byte stream | A response walks the same layers in reverse",
    why="Each layer has a narrow contract with the layer below. You can replace Ethernet with Wi-Fi without rewriting HTTP, because IP hides the link.",
    where="Every request path in a service: the packet capture, the load balancer, the socket, and the HTTP handler are four layers of the same call.",
    analogy="An analogy only: a letter (application) goes in an envelope (transport), into a mail sack addressed to a city (IP), onto a particular truck route (link).",
    example="curl https://example.com crosses DNS, TCP, TLS, and HTTP. ping example.com stops at ICMP over IP and never opens a port.",
    backend="A 502 from a proxy is an application or transport failure. A timeout with no SYN-ACK is a network path problem. The layer tells you which tool to open.",
    avoid="Do not debug an application error by redrawing the seven OSI layers. Use the model to pick a layer, then use that layer's tools.",
    code="def layer_for(symptom: str) -> str:\n    text = symptom.lower()\n    if 'connection refused' in text or 'timeout' in text:\n        return 'transport or path'\n    if text.startswith('http '):\n        return 'application'\n    if 'no route' in text:\n        return 'internet'\n    return 'inspect from the nic upward'\n\n\nif __name__ == '__main__':\n    assert layer_for('connection refused') == 'transport or path'\n    assert layer_for('HTTP 500') == 'application'\n",
    expected="The asserts pass. 'connection refused' maps to transport, 'HTTP 500' maps to application.",
    explain="The function is a triage rule, not a packet decoder. It stops you from treating every failure as an application bug.",
    failure="'connection refused' means a RST or nothing listening. It is not DNS. 'timeout' may be a drop, a firewall, or a saturated server. The same English word hides different layers.",
    symptom="Users say the site is down, but some regions work and the process is healthy.",
    cause="A path, route, or middlebox is failing for one network, while the application process is fine.",
    diagnose="Compare success rate by client network or AZ | Capture whether SYNs get SYN-ACKs | Check routes and security groups before reading application logs",
    mitigation="Shift traffic off the bad path or open the blocked port. Serve a degraded response only if the application itself is the failing layer.",
    prevention="Health checks from more than one network, and alerts on SYN retransmits and connect timeouts, not only on HTTP 500.",
    benefit="You isolate faults to a layer and replace one layer without rewriting the others.",
    cost="The models are simplifications. TLS does not sit neatly in one OSI box, and middleboxes violate layering.",
    choose="Use TCP/IP names when you are operating production, and OSI names only when a textbook or a vendor diagram uses them.",
    load="Under packet loss the transport layer, not the application code, spends time retransmitting. CPU in the service can look idle while clients time out.",
    limits="Layers leak: a firewall can break an application it does not understand | The seven-layer picture is not the implementation | A healthy process does not prove the network path is healthy",
    alts="A flat 'the network is down' story with no layer | Host-only debugging that never looks at the path",
    mistakes="Treating OSI layer numbers as something you configure || People recite seven layers and never open a capture || Name the layer and the tool, then stop ;; Debugging HTTP 500 as a routing problem || The status line was produced by an application that was reached || Read the application log once the TCP handshake succeeded ;; Ignoring middleboxes || Load balancers and NAT rewrite headers and addresses || Draw the boxes that actually terminate the connection ;; Assuming the textbook stack matches the cloud path || Cloud networking adds virtual routers and security groups || Trace the path you deployed, not the diagram in a course",
    confused="OSI versus the TCP/IP stack that is actually implemented",
)

add(
    "D04-T002",
    title="IP addressing, subnetting, CIDR",
    definition="An IPv4 or IPv6 address identifies an interface. CIDR writes a prefix as address plus prefix length. The prefix is the network. The rest is the host.",
    problem="Without prefixes, every router would need a route to every host. Subnets let a router advertise one block instead of thousands of hosts.",
    steps="Write the address and the prefix length | The prefix length says how many leading bits are the network | Hosts with the same prefix are on the same subnet and talk at layer 2 | A packet for a different prefix goes to the gateway | Routing tables match the longest prefix",
    why="Longest-prefix match lets a specific route override a summary route. That is how a VPC route to one subnet beats a default route to the internet.",
    where="VPC subnets, security groups, Kubernetes pod CIDRs, and the address a load balancer listens on.",
    analogy="An analogy only: a street name is the prefix and the house number is the host. Mail for another street goes to the post office, which is the gateway.",
    example="10.0.0.0/24 has 256 addresses. The first and last are reserved in common IPv4 practice for the network and broadcast. Usable hosts are fewer than 256. 10.0.0.0/16 is 65,536 addresses and contains that /24.",
    backend="Put the database subnet in a private CIDR with no internet route. Put the load balancer in a public subnet. Security groups are not a substitute for the route table.",
    avoid="Do not overlap CIDRs you may later peer or connect with a VPN. Overlap makes routing ambiguous.",
    code="def same_subnet(ip: str, other: str, prefix: int) -> bool:\n    def bits(text: str) -> int:\n        value = 0\n        for part in text.split('.'):\n            value = (value << 8) | int(part)\n        return value\n    shift = 32 - prefix\n    return (bits(ip) >> shift) == (bits(other) >> shift)\n\n\nif __name__ == '__main__':\n    assert same_subnet('10.0.0.5', '10.0.0.20', 24)\n    assert not same_subnet('10.0.0.5', '10.0.1.5', 24)\n",
    expected="The asserts pass. /24 groups 10.0.0.5 with 10.0.0.20 and not with 10.0.1.5.",
    explain="Shifting away the host bits compares only the prefix. This is the same test a host uses to decide if a destination is local.",
    failure="A /25 split in the middle of a live /24 will strand hosts that still use the old mask. They will ARP for addresses that are no longer local.",
    symptom="Two instances in the same VPC cannot connect, or traffic to a peered VPC blackholes.",
    cause="The route table lacks a route for the destination CIDR, the security group drops it, or the CIDRs overlap so the local route wins.",
    diagnose="Check the route table for the destination prefix | Compare security groups and network ACLs | Confirm the two CIDRs do not overlap",
    mitigation="Add the missing route or fix the security group. If CIDRs overlap, renumber one side before peering.",
    prevention="Allocate prefixes from an IP plan. Record them. Refuse a peer that overlaps.",
    benefit="One route entry covers a whole subnet, and private address space can be reused in unrelated networks.",
    cost="Planning, renumbering, and the scarcity of public IPv4. IPv6 removes scarcity but not the need for a plan.",
    choose="Use private RFC 1918 space inside a VPC and public addresses only on the edge.",
    load="Addressing does not get slower with QPS. Exhausting a small subnet does stop you from scaling out.",
    limits="IPv4 private space overlaps across companies | Longest prefix match can surprise you when a more specific route is wrong | Broadcast domains that are too large waste and amplify noise",
    alts="Giving every host a public address | One flat network with no subnets",
    mistakes="Counting 256 usable hosts in a /24 || Network and broadcast addresses are not hosts in common IPv4 || Subtract them when sizing ;; Overlapping VPC CIDRs when peering || The local route wins and traffic never leaves || Renumber before you peer ;; Confusing a security group with a route || A route delivers the packet and a security group filters it || Check both ;; Using a default route when a more specific route is wrong || Longest prefix wins even if you did not mean it || Read the whole table, not only the default",
    confused="A subnet mask versus a security-group rule",
)
