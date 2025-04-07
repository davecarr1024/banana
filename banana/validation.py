class Error(Exception): ...


class ValueError(Error, ValueError): ...


def validate_word(word: str) -> str:
    if not word.isalpha():
        raise ValueError(f"Word must be alpha, not {word!r}")
    return word.upper()


def validate_letter(letter: str) -> str:
    if len(letter) != 1 or not letter.isalpha():
        raise ValueError(f"Letter must be a single alpha character, not {letter!r}")
    return letter.upper()
