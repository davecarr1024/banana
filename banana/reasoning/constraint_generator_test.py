from banana.reasoning import ConstraintGenerator


def test_filter_can_build() -> None:
    c = ConstraintGenerator.filter_can_build(
        ["AB", "BC", "AD"],
        "ABC",
    )
    assert list(c.filter(["AB", "BC", "AD"])) == ["AB", "BC"]
