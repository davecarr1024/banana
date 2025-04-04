from dataclasses import dataclass

from banana.board.position import Position


@dataclass(frozen=True)
class Direction:
    dx: int
    dy: int

    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __post_init__(self) -> None:
        if self.dx * self.dx + self.dy * self.dy != 1:
            raise self.ValueError(f"Invalid direction: {self}")

    def __radd__(self, position: Position) -> Position:
        return self.__add__(position)

    def __add__(self, position: Position) -> Position:
        return Position(position.x + self.dx, position.y + self.dy)

    def __rsub__(self, position: Position) -> Position:
        return self.__neg__().__add__(position)

    def __neg__(self) -> "Direction":
        return Direction(-self.dx, -self.dy)

    def orthogonal(self) -> "Direction":
        return Direction(self.dy, self.dx)


ACROSS = Direction(1, 0)
DOWN = Direction(0, 1)
