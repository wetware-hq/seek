from __future__ import annotations

import copy
from typing import Any

from seek.codon_table import aa_to_dna_code11


def fill_cds_from_aa(
    frame: dict[str, Any],
    amino_acids: str,
    *,
    start: int = 1,
    strand: str = "+",
    replace_features: bool = False,
) -> dict[str, Any]:
    """
    Dumb filler: write DNA ``seq`` and a ``CDS`` feature from an AA string (NCBI code 11).

    Returns a new frame dict; does not mutate the input.
    """
    if frame.get("kind") != "DNA":
        raise ValueError("fill_cds_from_aa requires kind DNA")
    if start < 1:
        raise ValueError("start must be >= 1 (1-based coordinates)")
    if strand not in ("+", "-"):
        raise ValueError("strand must be '+' or '-'")

    out = copy.deepcopy(frame)
    dna = aa_to_dna_code11(amino_acids)
    out["seq"] = dna
    end = start + len(dna) - 1

    cds = {
        "type": "CDS",
        "start": start,
        "end": end,
        "strand": strand,
    }
    if replace_features:
        out["features"] = [cds]
    else:
        features = list(out.get("features") or [])
        features.append(cds)
        out["features"] = features
    return out
