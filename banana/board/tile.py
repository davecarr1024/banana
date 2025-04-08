from dataclasses import dataclass

from banana.board.position import Position


@dataclass(frozen=True)
class Tile:
    value: str
    position: Position
