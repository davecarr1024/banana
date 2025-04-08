from banana.reasoning.constraints import SortWordsByLen


def test_filter() -> None:
    assert list(SortWordsByLen().filter(["a", "ab", "abc"])) == ["a", "ab", "abc"]
    assert list(SortWordsByLen(reverse=True).filter(["a", "ab", "abc"])) == [
        "abc",
        "ab",
        "a",
    ]


def test_repr() -> None:
    assert repr(SortWordsByLen(reverse=True)) == "SortWordsByLen(reverse=True)"
    assert repr(SortWordsByLen(reverse=False)) == "SortWordsByLen(reverse=False)"
