from typing import Iterable, override

from banana.board import Board, Direction, Position, Word
from banana.reasoning.constraint import Constraint
from banana.reasoning.constraint_generator import ConstraintGenerator
from banana.reasoning.constraints import And, Contains, Start
from banana.validation import validate_letter, validate_word


class _Anchor(Constraint):
    def __init__(self, position: Position, direction: Direction) -> None:
        self.position = position
        self.direction = direction

    @override
    def __repr__(self) -> str:
        return f"Anchor({self.position}, {self.direction})"

    @override
    def create_candidates(self, board: Board, word: str) -> Iterable[Word]:
        for i in range(len(word)):
            word_ = Word.from_str(
                word, self.position - self.direction * i, self.direction
            )
            if board.can_place_word(word_):
                yield word_


class SimpleConstraintGenerator(ConstraintGenerator):
    def __init__(self, words: Iterable[str]) -> None:
        self.words = frozenset(map(validate_word, words))

    @override
    def __repr__(self) -> str:
        return f"SimpleConstraintGenerator({self.words})"

    @override
    def generate(self, board: Board, letters: Iterable[str]) -> Iterable[Constraint]:
        can_build_filter = self.filter_can_build(
            self.words,
            map(validate_letter, letters),
        )
        if len(board) == 0:
            yield And(
                [
                    can_build_filter,
                    Start(),
                ]
            )
        else:
            for word in board.get_words():
                direction = word.direction.orthogonal()
                for tile in word:
                    print(
                        f"generating constraints for tile {tile} in word {word}"
                        f" in direction {direction}"
                    )
                    if board.tile(tile.position + direction) is not None:
                        print(f"tile {tile} has a tile to the right")
                        continue
                    if board.tile(tile.position - direction) is not None:
                        print(f"tile {tile} has a tile to the left")
                        continue
                    yield And(
                        [
                            can_build_filter,
                            Contains([tile.value]),
                            _Anchor(tile.position, direction),
                        ]
                    )
