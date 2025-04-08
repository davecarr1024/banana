from banana.reasoning.constraints import InSet


def test_filter() -> None:
    assert list(InSet(["abc"]).filter(["abc", "def"])) == ["ABC"]


def test_repr() -> None:
    assert repr(InSet(["abc"])) == "InSet(frozenset({'ABC'}))"
