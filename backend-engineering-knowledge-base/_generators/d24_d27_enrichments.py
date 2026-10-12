"""Per-topic enrichment keyed by inventory ID (domains 24–27)."""
from __future__ import annotations

# Each value may include: deep, code_extra, mistakes_extra, linux_cmds, interview_focus
ENRICHMENTS: dict[str, dict[str, str]] = {
    "D24-T001": {
        "deep": (
            "The control plane exposes the Kubernetes API through kube-apiserver; etcd holds the desired cluster state; "
            "kube-scheduler assigns pods to nodes; kube-controller-manager runs controllers (Deployment, ReplicaSet, Node). "
            "Every node runs kubelet (pod lifecycle) and a container runtime (containerd/CRI-O). "
            "kubectl and controllers are clients of the API; they never talk to kubelet directly for declarations."
        ),
    },
    "D24-T008": {
        "deep": (
            "Liveness: is the process dead enough to restart? Failing liveness → kubelet kills container. "
            "Readiness: should this pod receive Service traffic? Failing readiness → removed from Endpoints, no restart. "
            "Startup: suppresses liveness until slow initialization finishes. "
            "Never aim liveness at a dependency that can blip (database); use readiness for that."
        ),
    },
    "D24-T009": {
        "deep": (
            "requests.cpu/memory: used by scheduler for placement and by kubelet for guaranteed share. "
            "limits.cpu: throttling when exceeded; limits.memory: OOMKill when exceeded. "
            "HPA compares metrics to requests. Setting limits without requests hides scheduling needs; "
            "requests without limits allow noisy neighbors on memory."
        ),
    },
    "D24-T031": {
        "deep": (
            "Use provider billing exports, cost allocation tags, and rightsizing reports—do not rely on invented benchmark prices. "
            "Optimize idle resources, storage lifecycle, egress, and over-provisioned requests/limits."
        ),
    },
    "D26-T003": {
        "linux_cmds": (
            "```bash\nps aux --sort=-%cpu | head -20\n```\n"
            "Lists processes with USER, PID, %CPU, %MEM, COMMAND—find CPU hogs.\n\n"
            "```bash\nps -eo pid,ppid,cmd --forest\n```\n"
            "Shows parent/child tree for runaway workers.\n\n"
            "```bash\ntop -b -n 1 | head -25\n```\n"
            "Batch snapshot of load averages and top consumers."
        ),
    },
    "D26-T008": {
        "linux_cmds": (
            "```bash\nss -tlnp\n```\n"
            "TCP listeners with PIDs (needs root for process names).\n\n"
            "```bash\nss -tan | awk 'NR==1 || /:8080/'\n```\n"
            "Filter connections involving port 8080.\n\n"
            "```bash\nlsof -iTCP:8080 -sTCP:LISTEN\n```\n"
            "Which process owns the listen socket."
        ),
    },
    "D26-T009": {
        "linux_cmds": (
            "```bash\ndig +short api.example.com A\n```\n"
            "Quick A-record answer from local resolver.\n\n"
            "```bash\ndig api.example.com +trace\n```\n"
            "Delegation chain from root—finds broken NS.\n\n"
            "```bash\nping -c 4 api.example.com\n```\n"
            "ICMP reachability (may be blocked while HTTP works)."
        ),
    },
}
