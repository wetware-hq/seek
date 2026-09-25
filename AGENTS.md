# Agent contract

Seek frames are the canonical JSON records for designed sequence in this repository. Prefer editing frame JSON over prose when expressing design.

## Frame rules

1. See `README.md` for the field spec, schema link, and v0 tooling.
2. One polymer → one frame. Do not maintain parallel sequence representations.
3. Required root fields (no other required keys):

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
6. `phase` is one of `spec`, `filled`, `kill`, or `tube`. Use `spec` while `seq` is empty; use `filled` once `seq` is written.
7. Coordinates are **1-based inclusive** on `seq` when `seq` is non-empty. On an empty parent frame, omit feature `start`/`end` and use `ref` only.
8. Empty `seq` is legal.
9. Each `features[]` entry must include `type` (string). When `seq` is non-empty, each feature must include `start` and `end` within `[1, len(seq)]`.
10. `features[].type`, `want[]`, and `forbid[]` are open strings (intent, not ontology).
11. A chromosome is a **parent DNA frame** whose features carry `ref` to child frame ids. Do **not** add `kind: chromosome`.
12. Validate against `schema/frame.schema.json` before writing or merging.

## v0 capabilities (this repo)

| Module | Role |
|--------|------|
| `schema/frame.schema.json` | JSON Schema for the eight-field core |
| `seek.filler` | CDS fill: amino-acid string + NCBI genetic code 11 → `seq` + `CDS` feature |
| `seek.viewer` | Print core fields and translate `CDS` features |
| `seek.validate` | Load and validate a frame dict |

## Out of scope

- Chat UI, foundation-model wrappers, vendor APIs
- Inhibitory critics (`hits`, automated phase transitions)
- Optional parent `write` bag for span ownership

## Roadmap order

1. **Frame** (this repository).
2. Critics that bind `seq` / `features` / `want` / `forbid` and write `phase` plus optional `hits`.
3. Optional `write` on parent frames for multi-agent chromosome design.

## Editing conventions

- When filling sequence, preserve existing features unless the task replaces them.
- After changing `seq`, ensure feature coordinates lie within `[1, len(seq)]` when `seq` is non-empty.
- Child frames referenced by `features[].ref` should exist as sibling JSON records in the same demo or test set.

## Demo checkpoints

- Primer example: a user can enter a short primer into `examples/primer.json` and validate it with `seek.viewer`.
- Chromosome example: parent frame plus one filled child (`chromosome_child_a`) and one empty child (`chromosome_child_b`).
