from banana.reasoning.constraints import SortWordsByLen


def test_filter() -> None:
    assert list(SortWordsByLen().filter(["a", "ab", "abc"])) == ["a", "ab", "abc"]
    assert list(SortWordsByLen(reverse=True).filter(["a", "ab", "abc"])) == [
        "abc",
        "ab",
        "a",
    ]
