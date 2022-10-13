from dataclasses import dataclass
from typing import Dict
from enum import Enum


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


@dataclass
class Tile:
    x: int
    y: int
    mapping: Dict[Direction, Direction]
