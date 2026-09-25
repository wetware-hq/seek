# Agent contract — Seek

This file is law for agents working in `wetwarehq/seek`. When it conflicts with chat, **this file and `README.md` win**.

## Mission

Implement and maintain the **sequence representation frame** for synthetic DNA and other informational polymers. The frame JSON is the product; natural language is commentary.

## Non-goals (v0)

Do **not** add:

- Chat UI
- Foundation-model or vendor API wrappers
- Inhibitory critic implementations (they come after terminals exist)

Critics will later bind `seq`, `features`, `want`, and `forbid`, and write `phase` plus optional `hits`. Optional `write` bags on parent frames are also later.

## Core frame

Require exactly eight top-level keys (see `schema/frame.schema.json`):

`id`, `kind`, `topo`, `seq`, `features`, `want`, `forbid`, `phase`

### Semantics

- `kind`: `DNA` | `RNA` | `AA` | `XNA`
- `topo`: `linear` | `circular`
- Coordinates on `seq` are **1-based inclusive**
- Empty `seq` is legal
- `features[].type`, `want[]`, `forbid[]`: open strings
- **One frame = one polymer**
- A **chromosome** is a parent **DNA** frame with `features[].ref` pointing at child frame ids. Do **not** add `kind: chromosome`.

## v0 deliverables

1. Keep `README.md` and this file accurate.
2. JSON Schema that requires only the eight fields (`additionalProperties` allowed on the root and on feature objects so spans and refs work).
3. **Filler**: amino-acid string + NCBI genetic code **table 11** → DNA `seq` plus a `CDS` feature.
4. **Viewer**: print the eight core fields and translate `CDS` features.
5. **Tests**: primer, peptide (filler), gRNA, mRNA cassette, parent chromosome with child refs.

## Editing rules

- Prefer minimal diffs; match existing layout and style.
- Do not weaken the eight-field contract without updating schema, README, and tests together.
- Examples in tests should be realistic enough for a Wetware demo: one parent, one filled child, other children empty.

## Commands

```bash
python -m pip install -e ".[dev]"
pytest
python -m seek.viewer path/to/frame.json
```
