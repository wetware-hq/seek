from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "frame.schema.json"


@lru_cache(maxsize=1)
def frame_schema() -> dict[str, Any]:
    with _SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _validate_feature_spans(frame: dict[str, Any]) -> None:
    """Enforce coordinate rules JSON Schema cannot express against len(seq)."""
    seq = frame.get("seq") or ""
    if not seq:
        return
    seq_len = len(seq)
    for index, feat in enumerate(frame.get("features") or []):
        start = feat.get("start")
        end = feat.get("end")
        if start is None or end is None:
            continue
        if end < start:
            raise ValidationError(
                f"features[{index}]: end ({end}) must be >= start ({start})"
            )
        if end > seq_len:
            raise ValidationError(
                f"features[{index}]: end ({end}) exceeds seq length ({seq_len})"
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
