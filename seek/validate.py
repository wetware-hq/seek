from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator

_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "frame.schema.json"


@lru_cache(maxsize=1)
def frame_schema() -> dict[str, Any]:
    with _SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _validate_feature_spans(frame: dict[str, Any]) -> None:
    """When seq is non-empty, each feature must have in-bounds 1-based spans."""
    seq = frame.get("seq") or ""
    if not seq:
        return
    n = len(seq)
    for idx, feat in enumerate(frame.get("features") or []):
        if "start" not in feat or "end" not in feat:
            raise jsonschema.ValidationError(
                f"features[{idx}] requires start and end when seq is non-empty"
            )
        start, end = feat["start"], feat["end"]
        if not isinstance(start, int) or not isinstance(end, int):
            raise jsonschema.ValidationError(
                f"features[{idx}].start and features[{idx}].end must be integers"
            )
        if start < 1:
            raise jsonschema.ValidationError(
                f"features[{idx}].start must be >= 1 (1-based coordinates)"
            )
        if end < start:
            raise jsonschema.ValidationError(
                f"features[{idx}].end must be >= start"
            )
        if end > n:
            raise jsonschema.ValidationError(
                f"features[{idx}].end {end} exceeds seq length {n}"
            )


def validate_frame(frame: dict[str, Any]) -> None:
    """Raise jsonschema.ValidationError if frame is invalid."""
    Draft202012Validator(frame_schema()).validate(frame)
    _validate_feature_spans(frame)


def load_frame(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        frame = json.load(fh)
    validate_frame(frame)
    return frame
