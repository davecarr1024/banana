from typing import Iterable, Optional, override

from banana.board import Board
from banana.reasoning.constraint_generator import ConstraintGenerator
from banana.reasoning.search import Search


class DFS(Search):
    class Error(Exception): ...

    class SearchError(Error, RuntimeError): ...

    def __init__(
        self,
        words: Iterable[str],
        constraint_generator: ConstraintGenerator,
    ) -> None:
        super().__init__(words)
        self.constraint_generator = constraint_generator

    def _search(self, board: Board, letters: list[str]) -> Optional[Board]:
        if not letters:
            return board

        constraints = self.constraint_generator.generate(board, letters)
        for constraint in constraints:
            for word in constraint.filter(self.words):
                for candidate in constraint.create_candidates(board, word):
                    if not board.can_place_word(candidate):
                        continue
                    candidate_board = board.copy()
                    candidate_board.place_word(candidate)
                    if candidate_board == board:
                        continue
                    if not self._board_is_valid(candidate_board):
                        continue
                    candidate_letters = self._letters_without_word(
                        board, candidate, letters
                    )
                    candidate_solution = self._search(
                        candidate_board,
                        list(candidate_letters),
                    )
                    if candidate_solution is not None:
                        return candidate_solution

    @override
    def search(self, board: Board, letters: Iterable[str]) -> Board:
        if result := self._search(board, list(letters)):
            return result
        raise self.SearchError("No solution found")
