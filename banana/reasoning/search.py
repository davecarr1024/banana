from abc import ABC, abstractmethod
from typing import Iterable

from banana.board import Board


class Search(ABC):
    @abstractmethod
    def search(self, board: Board, letters: Iterable[str]) -> Board: ...
