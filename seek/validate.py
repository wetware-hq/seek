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


def validate_frame(frame: dict[str, Any]) -> None:
    """Raise jsonschema.ValidationError if frame is invalid."""
    Draft202012Validator(frame_schema()).validate(frame)


def load_frame(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open(encoding="utf-8") as fh:
        frame = json.load(fh)
    validate_frame(frame)
    return frame
