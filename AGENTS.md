# Agent contract

Seek is the object biological frontier intelligence writes when it designs sequence. The frame is the product. English is commentary.

## Law

1. Read `README.md` for the clinical abstract and system card.
2. Every polymer is exactly one frame. Do not invent parallel representations.
3. Required core fields only (no extra required keys at the root):

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

4. `kind` is one of `DNA`, `RNA`, `AA`, or `XNA`.
5. `topo` is `linear` or `circular`.
6. Coordinates are **1-based inclusive** on `seq`.
7. Empty `seq` is legal.
8. `features[].type`, `want[]`, and `forbid[]` are open strings (intent, not ontology).
9. One frame = one polymer. A chromosome is a **parent DNA frame** whose features carry `ref` to child frame ids. Do **not** add `kind: chromosome`.
10. Validate frames against `schema/frame.schema.json` before writing or merging.

## v0 capabilities (this repo)

| Module | Role |
|--------|------|
| `schema/frame.schema.json` | JSON Schema for the eight-field core |
| `seek.filler` | Dumb CDS fill: amino-acid string + NCBI genetic code 11 → `seq` + `CDS` feature |
| `seek.viewer` | Print core fields and translate `CDS` features |
| `seek.validate` | Load and validate a frame dict |

## Out of scope (do not implement here)

- Chat UI, foundation-model wrappers, vendor APIs
- Inhibitory critics (`hits`, phase transitions beyond manual edit)
- Optional parent `write` bag for span ownership

## Order of operations

1. **Frame** (this repository).
2. Critics that bind `seq` / `features` / `want` / `forbid` and write `phase` plus optional `hits`.
3. Optional `write` on parent frames for multi-agent synthetic chromosomes.

## Editing rules for agents

- Prefer editing frame JSON over prose when expressing design.
- When filling sequence, preserve existing features unless the task replaces them.
- After changing `seq`, re-check feature coordinates still lie within `[1, len(seq)]` when `seq` is non-empty.
- Child frames referenced by `features[].ref` should exist as sibling JSON records in the same demo or test set.

## Acceptance (human demo)

A stranger can type a primer into the record in two minutes. A Wetware demo can show one parent frame and one filled child frame with remaining child sequences empty.
