from dataclasses import dataclass
from typing import List, Optional, Dict
from pyvkpns.utils import convert_empty_to_none  


@dataclass
class Inner:
    a: str
    b: int
    c: Optional[str] = None


@dataclass
class Outer:
    x: str
    y: Inner
    z: List[str]
    w: Dict[str, str]


class TestConvertEmptyToNone:

    def test_empty_string_to_none(self):
        assert convert_empty_to_none("") is None
        assert convert_empty_to_none("non-empty") == "non-empty"

    def test_dict_conversion(self):
        data = {"a": "", "b": "text", "c": {"d": "", "e": 1}}
        expected = {"a": None, "b": "text", "c": {"d": None, "e": 1}}
        assert convert_empty_to_none(data) == expected

    def test_list_conversion(self):
        data = ["", "foo", ["", "bar"]]
        expected = [None, "foo", [None, "bar"]]
        assert convert_empty_to_none(data) == expected

    def test_dataclass_conversion(self):
        inner = Inner(a="", b=5, c="")
        outer = Outer(x="", y=inner, z=["", "ok"], w={"key": ""})
        result = convert_empty_to_none(outer)

        assert result.x is None
        assert result.y.a is None
        assert result.y.b == 5
        assert result.y.c is None
        assert result.z == [None, "ok"]
        assert result.w == {"key": None}

    def test_preserve_other_types(self):
        assert convert_empty_to_none(123) == 123
        assert convert_empty_to_none(0.5) == 0.5
        assert convert_empty_to_none(True) is True
        obj = object()
        assert convert_empty_to_none(obj) is obj

    def test_nested_mix(self):
        data = {
            "list": ["", {"a": ""}],
            "dataclass": Outer(x="", y=Inner(a="", b=1), z=[], w={})
        }
        result = convert_empty_to_none(data)
        assert result["list"] == [None, {"a": None}]
        assert result["dataclass"].x is None
        assert result["dataclass"].y.a is None
        assert result["dataclass"].y.b == 1