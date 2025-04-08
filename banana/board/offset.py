from dataclasses import dataclass
from typing import Union, overload


@dataclass(frozen=True)
class Offset:
    dx: int
    dy: int

    @overload
    def __add__(self, rhs: "Offset") -> "Offset": ...

    @overload
    def __add__(self, rhs: "position.Position") -> "position.Position": ...

    def __add__(
        self,
        rhs: Union[
            "Offset",
            "position.Position",
        ],
    ) -> Union[
        "Offset",
        "position.Position",
    ]:
        match rhs:
            case Offset():
                return Offset(self.dx + rhs.dx, self.dy + rhs.dy)
            case position.Position():
                return position.Position(self.dx + rhs.x, self.dy + rhs.y)

    def __mul__(self, rhs: int) -> "Offset":
        return Offset(self.dx * rhs, self.dy * rhs)

    def __neg__(self) -> "Offset":
        return Offset(-self.dx, -self.dy)


from banana.board import position  # noqa: E402
