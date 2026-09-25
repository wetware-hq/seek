# Seek

A sequence representation frame for synthetic DNA and, more generally, any informational polymer in molecular biology.

Seek is the object that biological frontier intelligence writes when it designs sequence. **The frame is the product.** English is commentary. This repository ships the frame first; inhibitory critics come after the terminals exist.

Synthetic DNA is a physical scaffold that design models act on. One frame = one polymer. A chromosome is a parent DNA frame whose `features` carry `ref` pointers to child frames—not a separate `kind`.

## Core record (v0)

Every frame carries exactly these eight fields:

```json
{
  "id": "frm_001",
  "kind": "DNA",
  "topo": "linear",
  "seq": "",
  "features": [],
  "want": [],
  "forbid": [],
  "phase": "spec"
}
```

| Field | Meaning |
| --- | --- |
| `id` | Stable frame identifier (e.g. `frm_001`). |
| `kind` | `DNA` \| `RNA` \| `AA` \| `XNA` |
| `topo` | `linear` \| `circular` |
| `seq` | Polymer sequence; empty string is legal. |
| `features` | Annotated spans on `seq`; coordinates are **1-based inclusive**. |
| `want` | Open-string design intents (critics bind later). |
| `forbid` | Open-string prohibitions (critics bind later). |
| `phase` | Lifecycle label; v0 frames typically start at `spec`. |

`features[].type` and entries in `want` / `forbid` are open strings. Optional feature keys such as `start`, `end`, and `ref` (child frame id) are used in examples and tests.

## System card

| Layer | v0 | Later |
| --- | --- | --- |
| Frame + schema | ✓ | |
| Filler (AA → DNA + CDS, table 11) | ✓ | |
| Viewer (core fields + CDS translation) | ✓ | |
| Inhibitory critics on `seq` / `features` / `want` / `forbid` | | ✓ |
| Optional `write` bag on parent frames | | ✓ |
| Chat UI, FM wrappers, vendor APIs | — | out of scope |

**Order of operations:** (1) Frame — this repo. (2) Critics that write `phase` and optional `hits`. (3) Optional span-ownership `write` on synthetic chromosomes.

## Quick start

```bash
python -m pip install -e ".[dev]"
pytest
python -m seek.viewer examples/peptide.json
```

Fill a peptide frame (amino-acid `seq` on an `AA` frame) into DNA:

```python
from seek.filler import fill_peptide_to_dna

frame = {"id": "frm_pep", "kind": "AA", "topo": "linear", "seq": "MK", ...}
dna = fill_peptide_to_dna(frame, target_id="frm_dna")
```

JSON Schema: [`schema/frame.schema.json`](schema/frame.schema.json).

Agent contract: [`AGENTS.md`](AGENTS.md).

## Acceptance (v0)

A stranger can type a primer into the record in two minutes. A Wetware demo can show one parent frame and one filled child frame with remaining child sequences empty.

## License

MIT — see [LICENSE](LICENSE).
