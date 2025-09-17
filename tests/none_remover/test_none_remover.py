from src.utils import remove_none 
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Inner:
    a: Optional[str]
    b: Optional[int]


@dataclass
class Outer:
    x: Optional[str]
    y: Optional[Inner]
    z: List[Optional[str]]
    w: Dict[str, Optional[str]]


class TestRemoveNone:

    def test_basic_dict(self):
        data = {"a": 1, "b": None, "c": 2}
        expected = {"a": 1, "c": 2}
        assert remove_none(data) == expected

    def test_nested_dict(self):
        data = {"a": {"b": None, "c": 3}, "d": None}
        expected = {"a": {"c": 3}}
        assert remove_none(data) == expected

    def test_list_inside_dict(self):
        data = {"a": [1, None, 2], "b": None}
        expected = {"a": [1, 2]}
        assert remove_none(data) == expected

    def test_nested_list(self):
        data = [1, None, {"a": None, "b": 2}, [None, 3]]
        expected = [1, {"b": 2}, [3]]
        assert remove_none(data) == expected

    def test_dataclass_conversion(self):
        inner = Inner(a=None, b=5)
        outer = Outer(x=None, y=inner, z=[None, "ok"], w={"key": None})
        outer_dict: Dict[str, Any] = {
            "x": outer.x,
            "y": {"a": outer.y.a, "b": outer.y.b},
            "z": outer.z,
            "w": outer.w
        }
        result = remove_none(outer_dict)
        assert result["y"]["b"] == 5
        assert "a" not in result["y"]
        assert result["z"] == ["ok"]
        assert result["w"] == {}

    def test_preserve_non_none_values(self):
        data = {"a": 0, "b": False, "c": "", "d": "text"}
        assert remove_none(data) == data