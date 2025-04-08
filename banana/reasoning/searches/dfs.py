from collections import Counter
from typing import Iterable, Optional, override

from banana.board import Board, Word
from banana.reasoning.constraint_generator import ConstraintGenerator
from banana.reasoning.search import Search
from banana.validation import validate_letter


class DFS(Search):
    class Error(Exception): ...

    class SearchError(Error, RuntimeError): ...

    def __init__(self, constraint_generator: ConstraintGenerator) -> None:
        self.constraint_generator = constraint_generator

    def _search(self, board: Board, letters: Iterable[str]) -> Optional[Board]:
        def letters_without_candidate(candidate: Word) -> Iterable[str]:
            letters_consumed = board.get_letters_consumed(candidate)
            new_counter = Counter(letters) - Counter(letters_consumed)
            return new_counter.elements()

        if not letters:
            return board

        constraints = self.constraint_generator.generate(board, letters)
        for constraint in constraints:
            for word in constraint.filter(letters):
                for candidate in constraint.create_candidates(board, word):
                    candidate_board = board.copy()
                    candidate_board.place_word(candidate)
                    candidate_letters = letters_without_candidate(candidate)
                    candidate_solution = self._search(
                        candidate_board, candidate_letters
                    )
                    if candidate_solution is not None:
                        return candidate_solution

    @override
    def search(self, board: Board, letters: Iterable[str]) -> Board:
        if result := self._search(board, list(map(validate_letter, letters))):
            return result
        raise self.SearchError("No solution found")
