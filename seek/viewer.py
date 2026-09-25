from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from seek.codon_table import reverse_complement, translate_dna_code11
from seek.validate import load_frame, validate_frame


def _slice_seq(seq: str, start: int, end: int, strand: str) -> str:
    if start < 1 or end < start:
        raise ValueError(f"invalid coordinates: {start}-{end}")
    segment = seq[start - 1 : end]
    if strand == "-":
        segment = reverse_complement(segment)
    elif strand != "+":
        raise ValueError(f"invalid strand: {strand!r}")
    return segment


def translate_cds_features(frame: dict[str, Any]) -> list[tuple[dict[str, Any], str]]:
    """Return (feature, peptide) for each CDS feature."""
    seq = frame.get("seq") or ""
    if not seq:
        return []
    results: list[tuple[dict[str, Any], str]] = []
    for feat in frame.get("features") or []:
        if feat.get("type") != "CDS":
            continue
        start = feat.get("start")
        end = feat.get("end")
        strand = feat.get("strand", "+")
        if start is None or end is None:
            results.append((feat, "<missing coordinates>"))
            continue
        if end > len(seq):
            results.append((feat, "<coordinates beyond seq>"))
            continue
        segment = _slice_seq(seq, start, end, strand)
        results.append((feat, translate_dna_code11(segment)))
    return results


def format_frame(frame: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"id:    {frame['id']}")
    lines.append(f"kind:  {frame['kind']}")
    lines.append(f"topo:  {frame['topo']}")
    lines.append(f"phase: {frame['phase']}")
    seq = frame.get("seq") or ""
    lines.append(f"seq:   ({len(seq)} bp) {seq if len(seq) <= 80 else seq[:77] + '...'}")
    want = frame.get("want") or []
    forbid = frame.get("forbid") or []
    lines.append(f"want:  {want if want else '[]'}")
    lines.append(f"forbid:{forbid if forbid else '[]'}")
    features = frame.get("features") or []
    lines.append(f"features ({len(features)}):")
    for i, feat in enumerate(features):
        ref = f" ref={feat['ref']}" if feat.get("ref") else ""
        coords = ""
        if feat.get("start") is not None and feat.get("end") is not None:
            strand = feat.get("strand", "+")
            coords = f" {feat['start']}-{feat['end']} ({strand})"
        lines.append(f"  [{i}] {feat.get('type', '?')}{coords}{ref}")

    translations = translate_cds_features(frame)
    if translations:
        lines.append("CDS translation (code 11):")
        for feat, pep in translations:
            label = feat.get("type", "CDS")
            lines.append(f"  {label} {feat.get('start')}-{feat.get('end')}: {pep}")
    return "\n".join(lines)


def view_frame(frame: dict[str, Any]) -> str:
    validate_frame(frame)
    return format_frame(frame)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print Seek frame core fields and CDS translations.")
    parser.add_argument("path", type=Path, help="Path to frame JSON")
    parser.add_argument("--json", action="store_true", help="Print raw JSON instead of summary")
    args = parser.parse_args(argv)
    frame = load_frame(args.path)
    if args.json:
        json.dump(frame, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(format_frame(frame))
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
