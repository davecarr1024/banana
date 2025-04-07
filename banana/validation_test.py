from typing import Optional

import pytest
from pytest_subtests import SubTests

from banana.validation import ValueError, validate_letter, validate_word


def test_validate_letter(subtests: SubTests) -> None:
    for letter, expected in list[tuple[str, Optional[str]]](
        [
            ("", None),
            ("1", None),
            ("ab", None),
            ("a", "A"),
        ]
    ):
        with subtests.test(letter=letter, expected=expected):
            if expected is None:
                with pytest.raises(ValueError):
                    validate_letter(letter)
            else:
                assert validate_letter(letter) == expected


def test_validate_word(subtests: SubTests) -> None:
    for word, expected in list[tuple[str, Optional[str]]](
        [
            ("", None),
            ("1", None),
            ("ab1", None),
            ("ab", "AB"),
        ]
    ):
        with subtests.test(word=word, expected=expected):
            if expected is None:
                with pytest.raises(ValueError):
                    validate_word(word)
            else:
                assert validate_word(word) == expected
