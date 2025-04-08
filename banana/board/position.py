from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, rhs: Union["direction.Direction", "offset.Offset"]) -> "Position":
        return Position(self.x + rhs.dx, self.y + rhs.dy)

    def __sub__(self, rhs: Union["direction.Direction", "offset.Offset"]) -> "Position":
        return self + (-rhs)


from banana.board import direction, offset  # noqa: E402
