def assert_no_none(d, path="root"):
    """Recursively assert that there are no None values in dicts/lists."""
    if isinstance(d, dict):
        for k, v in d.items():
            assert v is not None, f"Found None at path: {path}.{k}"
            assert_no_none(v, path=f"{path}.{k}")
    elif isinstance(d, list):
        for idx, item in enumerate(d):
            assert_no_none(item, path=f"{path}[{idx}]")