from dataclasses import dataclass
from typing import Iterable, override

from banana.board import Board
from banana.reasoning.constraint import Constraint
from banana.reasoning.constraint_generator import ConstraintGenerator
from banana.reasoning.search import Search


@dataclass(frozen=True)
class _Node:
    board: Board
    letters: list[str]
    constraints: list[Constraint]


class BeamSearch(Search):
    class Error(Exception): ...

    class SearchError(Error, RuntimeError): ...

    def __init__(
        self,
        words: Iterable[str],
        constraint_generator: ConstraintGenerator,
        beam_size: int = 100,
        max_depth: int = 10,
    ) -> None:
        super().__init__(words)
        self.constraint_generator = constraint_generator
        self.beam_size = beam_size
        self.max_depth = max_depth

    def _node(
        self,
        board: Board,
        letters: list[str],
    ) -> _Node:
        return _Node(
            board,
            letters,
            list(self.constraint_generator.generate(board, letters)),
        )

    def _expand(self, node: _Node) -> Iterable[_Node]:
        for constraint in node.constraints:
            for word in constraint.filter(self.words):
                for candidate in constraint.create_candidates(
                    node.board,
                    word,
                ):
                    if not node.board.can_place_word(candidate):
                        continue
                    candidate_board = node.board.copy()
                    candidate_board.place_word(candidate)
                    if not self._board_is_valid(candidate_board):
                        continue
                    candidate_letters = self._letters_without_word(
                        node.board,
                        candidate,
                        node.letters,
                    )
                    yield self._node(candidate_board, list(candidate_letters))

    def _score(self, node: _Node) -> float:
        return -len(node.letters)

    @override
    def search(self, board: Board, letters: Iterable[str]) -> Board:
        letters = list(letters)
        beam = [self._node(board, letters)]
        depth = 1
        while beam and depth <= self.max_depth:
            beam = sorted(
                beam,
                key=self._score,
                reverse=True,
            )[: self.beam_size]
            print(f"beam search depth {depth} beam size {len(beam)}")
            for node in beam:
                if not node.letters:
                    return node.board
            beam = [
                expanded_node for node in beam for expanded_node in self._expand(node)
            ]
            print(f"expanded beam size {len(beam)}")
            depth += 1
        raise self.SearchError("Search failed to find a solution.")
