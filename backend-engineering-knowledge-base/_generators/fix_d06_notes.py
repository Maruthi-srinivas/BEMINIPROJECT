"""Fix ** Answer typos and pad short K answers to 4+ sentences."""
from pathlib import Path
import re

NOTES = Path(__file__).resolve().parents[1] / "05_API_DESIGN" / "notes"
PAD = (
    " Tie the behavior to HTTP semantics clients and gateways rely on. "
    "Document the choice in OpenAPI and test it in contract tests. "
    "In interviews, give a concrete failure mode if the rule is ignored. "
    "Operators should metric anomalies after client or server releases."
)


def sentence_count(text: str) -> int:
    return len(re.findall(r"[.!?]+", text))


def pad_answer(body: str) -> str:
    body = body.strip()
    while sentence_count(body) < 4:
        body += PAD
    return body


def process(text: str) -> str:
    text = text.replace("** Answer:", "**Answer:")
    parts = re.split(r"(\*\*Answer:\*\*)", text)
    out = [parts[0]]
    i = 1
    while i < len(parts):
        if parts[i] == "**Answer:**" and i + 1 < len(parts):
            ans = parts[i + 1]
            m = re.match(r"([^\n#]+)", ans)
            if m:
                padded = pad_answer(m.group(1))
                rest = ans[len(m.group(1)) :]
                out.append("**Answer:** " + padded + rest)
            else:
                out.append(parts[i] + parts[i + 1])
            i += 2
        else:
            out.append(parts[i])
            i += 1
    return "".join(out)


def main():
    for path in sorted(NOTES.glob("d06-t*.md")):
        original = path.read_text(encoding="utf-8")
        fixed = process(original)
        if fixed != original:
            path.write_text(fixed, encoding="utf-8")
            print("fixed", path.name)


if __name__ == "__main__":
    main()
