"""Print all section K blocks for T021-T036. Run: python gen_bulk_k.py > bulk_k.md"""
from d17_k_md import TOPIC_K_ARGS, section_k

for tid in sorted(TOPIC_K_ARGS):
    if tid < "D17-T021":
        continue
    print(f"---{tid}---")
    print(section_k(*TOPIC_K_ARGS[tid]))
    print()
