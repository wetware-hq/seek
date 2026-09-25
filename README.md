# Seek

Seek is a JSON frame for one informational polymer in molecular biology (`DNA`, `RNA`, `AA`, or `XNA`). Each record holds the primary sequence, annotated `features`, design intent (`want`, `forbid`), and lifecycle `phase`.

| Item | Value |
|------|--------|
| Core | Eight required fields: `id`, `kind`, `topo`, `seq`, `features`, `want`, `forbid`, `phase` |
| Polymers | `kind`: `DNA` · `RNA` · `AA` · `XNA` |
| Topology | `topo`: `linear` · `circular` |
| Coordinates | 1-based inclusive on `seq` when `seq` is nonempty; parent frames with empty `seq` may use `ref` without numeric spans |
| Chromosome | Parent DNA frame; `features[].ref` → child frame ids (no `kind: chromosome`) |
| Schema | [`schema/frame.schema.json`](schema/frame.schema.json) |
| v0 tools | CDS filler (code 11), viewer, tests |

## Core frame

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

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Validate and view a frame:

```bash
python -m seek.viewer examples/primer.json
```

Fill a peptide into DNA (NCBI genetic code 11):

```python
from seek.filler import fill_cds_from_aa
from seek.validate import load_frame

frame = load_frame("examples/peptide_empty.json")
filled = fill_cds_from_aa(frame, "MK")
```

## Examples

| File | Intent |
|------|--------|
| `examples/primer.json` | PCR primer record |
| `examples/peptide_empty.json` | Peptide spec before fill |
| `examples/peptide.json` | Filled DNA CDS after encode |
| `examples/peptide_aa.json` | Amino-acid polymer (`kind: AA`) |
| `examples/grna.json` | gRNA (RNA) |
| `examples/mrna_cassette.json` | DNA cassette for IVT mRNA |
| `examples/chromosome_parent.json` | Parent with child refs |
| `examples/chromosome_child_a.json` | Filled child |
| `examples/chromosome_child_b.json` | Empty child (demo) |

## Roadmap

1. **Frame** (v0, this repo).
2. Inhibitory critics on `seq`, `features`, `want`, `forbid` → `phase` and optional `hits`.
3. Optional `write` bag on parent frames for multi-agent chromosome design.

## License

MIT — see [LICENSE](LICENSE).
