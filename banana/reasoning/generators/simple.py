from typing import Iterable, override

from banana.board import Board
from banana.reasoning.constraint import Constraint
from banana.reasoning.constraint_generator import ConstraintGenerator
from banana.reasoning.constraints import Start


class Simple(ConstraintGenerator):
    @override
    def generate(self, board: Board) -> Iterable[Constraint]:
        if len(board) == 0:
            return [Start()]
        raise NotImplementedError()
