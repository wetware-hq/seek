"""NCBI genetic code table 11 (bacterial, archaeal and plant plastid)."""

from __future__ import annotations

# Codon -> amino acid (one-letter). Stop codons map to None.
TABLE_11: dict[str, str | None] = {
    "TTT": "F",
    "TTC": "F",
    "TTA": "L",
    "TTG": "L",
    "TCT": "S",
    "TCC": "S",
    "TCA": "S",
    "TCG": "S",
    "TAT": "Y",
    "TAC": "Y",
    "TAA": None,
    "TAG": None,
    "TGT": "C",
    "TGC": "C",
    "TGA": "W",
    "TGG": "W",
    "CTT": "L",
    "CTC": "L",
    "CTA": "L",
    "CTG": "L",
    "CCT": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "CAT": "H",
    "CAC": "H",
    "CAA": "Q",
    "CAG": "Q",
    "CGT": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "ATT": "I",
    "ATC": "I",
    "ATA": "I",
    "ATG": "M",
    "ACT": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "AAT": "N",
    "AAC": "N",
    "AAA": "K",
    "AAG": "K",
    "AGT": "S",
    "AGC": "S",
    "AGA": "R",
    "AGG": "R",
    "GTT": "V",
    "GTC": "V",
    "GTA": "V",
    "GTG": "V",
    "GCT": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "GAT": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "GGT": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
}

# Preferred codon per amino acid for naive back-translation (table 11).
_PREFERRED_CODON: dict[str, str] = {
    "A": "GCT",
    "C": "TGT",
    "D": "GAT",
    "E": "GAA",
    "F": "TTC",
    "G": "GGT",
    "H": "CAT",
    "I": "ATT",
    "K": "AAA",
    "L": "CTG",
    "M": "ATG",
    "N": "AAT",
    "P": "CCG",
    "Q": "CAG",
    "R": "CGT",
    "S": "TCT",
    "T": "ACT",
    "V": "GTG",
    "W": "TGG",
    "Y": "TAC",
}

STOP_CODON = "TAA"


def translate_dna(dna: str) -> str:
    """Translate DNA using table 11; stops omitted from output."""
    dna = dna.upper().replace("U", "T")
    protein: list[str] = []
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i : i + 3]
        if len(codon) < 3:
            break
        aa = TABLE_11.get(codon)
        if aa is None:
            break
        protein.append(aa)
    return "".join(protein)


def back_translate_aa(aa: str, include_stop: bool = True) -> str:
    """Naive AA -> DNA using preferred table-11 codons."""
    codons: list[str] = []
    for letter in aa.upper():
        if letter == "*":
            codons.append(STOP_CODON)
            continue
        codon = _PREFERRED_CODON.get(letter)
        if codon is None:
            raise ValueError(f"Unknown amino acid: {letter}")
        codons.append(codon)
    if include_stop and (not aa.endswith("*")):
        codons.append(STOP_CODON)
    return "".join(codons)
