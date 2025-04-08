from banana.reasoning.constraints import InSet


def test_filter() -> None:
    assert list(InSet(["ABC"]).filter(["ABC", "DEF"])) == ["ABC"]
