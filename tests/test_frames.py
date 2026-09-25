from __future__ import annotations

from pathlib import Path

import pytest

from seek.filler import fill_cds_from_aa
from seek.validate import load_frame, validate_frame
from seek.viewer import format_frame, translate_cds_features

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def test_primer_frame_validates_and_viewer():
    frame = load_frame(EXAMPLES / "primer.json")
    assert frame["kind"] == "DNA"
    assert frame["features"][0]["type"] == "primer"
    text = format_frame(frame)
    assert "frm_primer_fwd" in text
    assert "primer" in text


def test_peptide_filler_writes_seq_and_cds():
    frame = load_frame(EXAMPLES / "peptide_empty.json")
    filled = fill_cds_from_aa(frame, "MK")
    validate_frame(filled)
    assert filled["seq"] == "ATGAAA"
    assert len(filled["features"]) == 1
    cds = filled["features"][0]
    assert cds["type"] == "CDS"
    assert cds["start"] == 1
    assert cds["end"] == 6
    translations = translate_cds_features(filled)
    assert translations[0][1] == "MK"


def test_grna_rna_frame():
    frame = load_frame(EXAMPLES / "grna.json")
    assert frame["kind"] == "RNA"
    assert frame["features"][0]["type"] == "gRNA"
    assert len(frame["seq"]) == 20


def test_mrna_cassette_cds_translation():
    frame = load_frame(EXAMPLES / "mrna_cassette.json")
    cds_feats = [f for f in frame["features"] if f["type"] == "CDS"]
    assert len(cds_feats) == 1
    translations = translate_cds_features(frame)
    assert len(translations) == 1
    _, pep = translations[0]
    assert pep == "MASKV"


def test_chromosome_parent_child_refs():
    parent = load_frame(EXAMPLES / "chromosome_parent.json")
    child_a = load_frame(EXAMPLES / "chromosome_child_a.json")
    child_b = load_frame(EXAMPLES / "chromosome_child_b.json")

    refs = {f["ref"] for f in parent["features"] if f.get("ref")}
    assert refs == {"frm_chr_child_a", "frm_chr_child_b"}
    assert parent["topo"] == "circular"
    assert child_a["seq"] != ""
    assert child_b["seq"] == ""
    assert child_a["phase"] == "draft"
    assert child_b["phase"] == "spec"


def test_schema_rejects_extra_root_keys():
    frame = load_frame(EXAMPLES / "primer.json")
    bad = {**frame, "extra": True}
    with pytest.raises(Exception):
        validate_frame(bad)
