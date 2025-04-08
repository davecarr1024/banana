from abc import ABC, abstractmethod
from collections import Counter
from typing import Iterable

from banana.board import Board, Word


class Search(ABC):
    def __init__(self, words: Iterable[str]) -> None:
        self.words = frozenset(words)

    def _board_is_valid(self, board: Board) -> bool:
        return {word.value for word in board.get_words()}.issubset(self.words)

    def _letters_without_word(
        self,
        board: Board,
        word: Word,
        letters: Iterable[str],
    ) -> Iterable[str]:
        letters_consumed = board.get_letters_consumed(word)
        return (Counter(letters) - Counter(letters_consumed)).elements()

    @abstractmethod
    def search(self, board: Board, letters: Iterable[str]) -> Board: ...
