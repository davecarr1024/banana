from collections import Counter
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
        max_depth: int = 0,
        # Heuristic weight for the number of remaining letters.
        # Negative values encourage using more letters.
        remaining_letters_weight: float = -2,
        # Heuristic weight for the size of the board.
        # Positive values encourage larger boards.
        board_size_weight: float = 1,
        # Heuristic weight for the average word length.
        # Positive values encourage longer words.
        average_word_length_weight: float = 1,
        # Heuristic weight for the number of constraints.
        # Negative values encourage more constrained search path (like MCV).
        constraints_weight: float = -1,
        # Heuristic weight for the rarity of letters.
        # Positive values encourage using rarer letters.
        letter_rarity_weight: float = 1.5,
    ) -> None:
        super().__init__(words)
        self.constraint_generator = constraint_generator
        self.beam_size = beam_size
        self.max_depth = max_depth
        counts = Counter("".join(words))
        self.letter_density = {
            letter: count / counts.total() for letter, count in counts.items()
        }
        self.inverse_letter_density = {
            letter: 1 - (count / counts.total()) for letter, count in counts.items()
        }
        self.remaining_letters_weight = remaining_letters_weight
        self.board_size_weight = board_size_weight
        self.average_word_length_weight = average_word_length_weight
        self.constraints_weight = constraints_weight
        self.letter_rarity_weight = letter_rarity_weight

    @override
    def __str__(self) -> str:
        return (
            f"BeamSearch\n"
            f"  beam_size={self.beam_size}\n"
            f"  max_depth={self.max_depth}\n"
            f"  remaining_letters_weight={self.remaining_letters_weight}\n"
            f"  board_size_weight={self.board_size_weight}\n"
            f"  average_word_length_weight={self.average_word_length_weight}\n"
            f"  constraints_weight={self.constraints_weight}\n"
            f"  letter_rarity_weight={self.letter_rarity_weight}\n"
        )

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
                    if node.board == candidate_board:
                        continue
                    if not self._board_is_valid(candidate_board):
                        continue
                    candidate_letters = self._letters_without_word(
                        node.board,
                        candidate,
                        node.letters,
                    )
                    yield self._node(candidate_board, list(candidate_letters))

    def _score(self, node: _Node) -> float:
        words = list(node.board.get_words())
        average_word_length = sum(map(len, words)) / len(words) if words else 0
        letters = [tile.value for tile in node.board]
        average_letter_rarity = (
            sum(self.inverse_letter_density.get(letter, 0) for letter in letters)
            / len(letters)
            if letters
            else 0
        )
        min_pos, max_pos = node.board.bounds()
        board_area = (max_pos.x - min_pos.x + 1) * (max_pos.y - min_pos.y + 1)
        board_density = len(node.board) / board_area
        return (
            self.remaining_letters_weight * len(node.letters)
            + self.board_size_weight * board_density
            + self.average_word_length_weight * average_word_length
            + self.constraints_weight * len(node.constraints)
            + self.letter_rarity_weight * average_letter_rarity
        )

    @override
    def search(self, board: Board, letters: Iterable[str]) -> Board:
        letters = list(letters)
        beam = [self._node(board, letters)]
        depth = 1
        while beam and (self.max_depth <= 0 or depth <= self.max_depth):
            beam = sorted(
                beam,
                key=lambda node: self._score(node),
                reverse=True,
            )[: self.beam_size]
            for node in beam:
                if not node.letters:
                    return node.board
            beam = [
                expanded_node for node in beam for expanded_node in self._expand(node)
            ]
            depth += 1
        raise self.SearchError("Search failed to find a solution.")
