from typing import Iterable, override

from banana.board import ACROSS, Board, Position, Word
from banana.reasoning.constraint import Constraint


class Start(Constraint):
    @override
    def __repr__(self) -> str:
        return "Start()"

    @override
    def create_candidates(self, board: Board, word: str) -> Iterable[Word]:
        return [
            Word.from_str(
                word,
                Position(0, 0),
                ACROSS,
            )
        ]
