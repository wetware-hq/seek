from __future__ import annotations

from seek.codon_table import back_translate_aa


def _blank_dna_frame(frame_id: str, topo: str = "linear") -> dict:
    return {
        "id": frame_id,
        "kind": "DNA",
        "topo": topo,
        "seq": "",
        "features": [],
        "want": [],
        "forbid": [],
        "phase": "spec",
    }


def fill_peptide_to_dna(
    aa_frame: dict,
    *,
    target_id: str,
    topo: str = "linear",
    include_stop: bool = True,
) -> dict:
    """
    Dumb filler: read amino-acid sequence from an AA frame, write a new DNA frame
    with codon-table-11 back-translation and a single CDS feature spanning the ORF.
    """
    if aa_frame.get("kind") != "AA":
        raise ValueError("fill_peptide_to_dna expects kind AA")
    peptide = aa_frame.get("seq", "")
    dna = back_translate_aa(peptide, include_stop=include_stop)
    end = len(dna)
    out = _blank_dna_frame(target_id, topo=topo)
    out["seq"] = dna
    out["features"] = [
        {
            "type": "CDS",
            "start": 1,
            "end": end,
        }
    ]
    return out
