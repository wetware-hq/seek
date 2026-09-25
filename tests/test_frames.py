from __future__ import annotations

import json
from pathlib import Path

import pytest

from seek.filler import fill_peptide_to_dna
from seek.schema import validate_frame
from seek.viewer import render_frame
from seek.codon_table import translate_dna

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def _load(name: str) -> dict:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def test_primer_frame_validates():
    frame = _load("primer.json")
    validate_frame(frame)
    assert frame["kind"] == "DNA"
    assert len(frame["seq"]) == 20


def test_peptide_filler_writes_dna_and_cds():
    aa = _load("peptide_aa.json")
    validate_frame(aa)
    dna = fill_peptide_to_dna(aa, target_id="frm_peptide_dna")
    validate_frame(dna)
    assert dna["kind"] == "DNA"
    cds = next(f for f in dna["features"] if f["type"] == "CDS")
    assert cds["start"] == 1
    assert cds["end"] == len(dna["seq"])
    assert translate_dna(dna["seq"]) == "MK"


def test_grna_frame_validates():
    frame = _load("grna.json")
    validate_frame(frame)
    assert frame["kind"] == "RNA"
    assert any(f["type"] == "gRNA_spacer" for f in frame["features"])


def test_mrna_cassette_validates():
    frame = _load("mrna_cassette.json")
    validate_frame(frame)
    assert frame["topo"] == "linear"
    assert frame["kind"] == "RNA"
    types = {f["type"] for f in frame["features"]}
    assert "five_prime_UTR" in types
    assert "CDS" in types
    assert "three_prime_UTR" in types


def test_chromosome_parent_with_child_refs():
    parent = _load("chromosome_parent.json")
    child_a = _load("chromosome_child_a.json")
    child_b = _load("chromosome_child_b.json")
    for frame in (parent, child_a, child_b):
        validate_frame(frame)
    refs = {f["ref"] for f in parent["features"] if "ref" in f}
    assert refs == {"frm_child_a", "frm_child_b"}
    assert child_a["seq"] != ""
    assert child_b["seq"] == ""


def test_viewer_renders_cds_translation():
    dna = fill_peptide_to_dna(_load("peptide_aa.json"), target_id="frm_x")
    text = render_frame(dna)
    assert "kind: DNA" in text
    assert "translation[CDS" in text
    assert "MK" in text


def test_schema_rejects_missing_core_field():
    bad = _load("primer.json").copy()
    del bad["phase"]
    with pytest.raises(Exception):
        validate_frame(bad)
