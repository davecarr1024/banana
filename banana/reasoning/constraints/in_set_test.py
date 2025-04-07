from banana.reasoning.constraints import InSet


def test_filter() -> None:
    assert list(InSet(["abc"]).filter(["abc", "def"])) == ["abc"]
