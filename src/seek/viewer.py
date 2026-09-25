from __future__ import annotations

import json
import sys
from pathlib import Path

from seek.codon_table import translate_dna

CORE_FIELDS = ("id", "kind", "topo", "seq", "features", "want", "forbid", "phase")


def render_frame(frame: dict) -> str:
    """Human-readable summary of core fields and CDS translations."""
    lines: list[str] = []
    for key in CORE_FIELDS:
        value = frame.get(key, "")
        if key in ("features", "want", "forbid") and isinstance(value, list):
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        else:
            lines.append(f"{key}: {value}")

    seq = frame.get("seq", "")
    for feat in frame.get("features", []):
        if feat.get("type") != "CDS":
            continue
        start = int(feat.get("start", 1))
        end = int(feat.get("end", len(seq)))
        span = seq[start - 1 : end]
        protein = translate_dna(span)
        label = feat.get("ref") or feat.get("label") or "CDS"
        lines.append(f"translation[{label} {start}-{end}]: {protein}")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: python -m seek.viewer <frame.json>", file=sys.stderr)
        return 2
    path = Path(argv[0])
    frame = json.loads(path.read_text(encoding="utf-8"))
    print(render_frame(frame))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
