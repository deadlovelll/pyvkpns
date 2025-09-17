from typing import Any


def remove_none(d: Any) -> Any:
    """Recursively remove None values from dicts/lists."""
    if isinstance(d, dict):
        return {k: remove_none(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [remove_none(v) for v in d if v is not None]
    else:
        return d