"""NCBI genetic code 11 (bacterial, archaeal, and plant plastid)."""

from __future__ import annotations

# fmt: off
_CODE_11: dict[str, str] = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}
# fmt: on

# One preferred codon per amino acid (excluding stop).
_PREFERRED: dict[str, str] = {
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
    "P": "CCT",
    "Q": "CAA",
    "R": "CGT",
    "S": "TCT",
    "T": "ACT",
    "V": "GTT",
    "W": "TGG",
    "Y": "TAT",
}


def aa_to_dna_code11(amino_acids: str, *, include_stop: bool = False) -> str:
    """Encode an amino-acid string as DNA using code 11 preferred codons."""
    seq: list[str] = []
    for aa in amino_acids.upper():
        if aa == "*":
            if not include_stop:
                raise ValueError("stop codon in peptide without include_stop=True")
            seq.append("TAA")
            continue
        codon = _PREFERRED.get(aa)
        if codon is None:
            raise ValueError(f"unknown amino acid: {aa!r}")
        seq.append(codon)
    return "".join(seq)


def translate_dna_code11(dna: str) -> str:
    """Translate a DNA string in frame 0 using code 11."""
    dna = dna.upper()
    peptides: list[str] = []
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i : i + 3]
        if len(codon) < 3:
            break
        aa = _CODE_11.get(codon, "X")
        if aa == "*":
            break
        peptides.append(aa)
    return "".join(peptides)


_COMPLEMENT = str.maketrans("ACGTacgt", "TGCAtgca")


def reverse_complement(dna: str) -> str:
    return dna.translate(_COMPLEMENT)[::-1]
