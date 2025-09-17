from typing import Any


def convert_empty_to_none(obj: Any) -> Any:
    """Recursively convert empty strings to None in dataclasses / dicts / lists."""
    if isinstance(obj, dict):
        return {k: convert_empty_to_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_empty_to_none(v) for v in obj]
    elif isinstance(obj, str) and obj == "":
        return None
    elif hasattr(obj, "__dataclass_fields__"):  # handle nested dataclasses
        return obj.__class__(**{
            k: convert_empty_to_none(getattr(obj, k))
            for k in obj.__dataclass_fields__
        })
    else:
        return obj