from banana.reasoning import ConstraintGenerator


def test_filter_can_build() -> None:
    c = ConstraintGenerator.filter_can_build(
        ["ab", "bc", "ad"],
        "abc",
    )
    assert list(c.filter(["ab", "bc", "ad"])) == ["AB", "BC"]
