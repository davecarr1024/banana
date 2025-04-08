from abc import ABC, abstractmethod
from typing import Iterable

from banana.board import Board
from banana.validation import validate_word


class Search(ABC):
    def __init__(self, words: Iterable[str]) -> None:
        self.words = frozenset(map(validate_word, words))

    def _board_is_valid(self, board: Board) -> bool:
        return {word.value for word in board.get_words()}.issubset(self.words)

    @abstractmethod
    def search(self, board: Board, letters: Iterable[str]) -> Board: ...
