from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator

_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schema" / "frame.schema.json"


@lru_cache
def _validator() -> Draft202012Validator:
    with _SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)
    return Draft202012Validator(schema)


def validate_frame(frame: dict) -> None:
    """Raise jsonschema.ValidationError if frame violates v0 core schema."""
    errors = sorted(_validator().iter_errors(frame), key=lambda e: e.path)
    if errors:
        raise errors[0]
