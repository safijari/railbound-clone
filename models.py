from dataclasses import dataclass
from typing import Dict
from enum import Enum
import random


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


_d = Direction


def rev_add(indict):
    indict.update({v: k for k, v in indict.items()})
    return indict


opposing_d = rev_add({_d.NORTH: _d.SOUTH, _d.EAST: _d.WEST})

num_rows = 30
num_cols = 30


def coord_key(coord):
    return f"{coord[0]}_{coord[1]}"


@dataclass
class Tile:
    x: int
    y: int
    mapping: Dict[Direction, Direction]
    symbol: str

    @classmethod
    def horizontal(cls, x, y):
        return Tile(x, y, rev_add({_d.WEST: _d.EAST}), "═")

    @classmethod
    def vertical(cls, x, y):
        return Tile(x, y, rev_add({_d.NORTH: _d.SOUTH}), "║")

    @classmethod
    def w2s(cls, x, y):
        return Tile(x, y, rev_add({_d.WEST: _d.SOUTH}), "╗")

    @classmethod
    def s2w(cls, x, y):
        return cls.w2s(x, y)

    @classmethod
    def w2n(cls, x, y):
        return Tile(x, y, rev_add({_d.WEST: _d.NORTH}), "╝")

    @classmethod
    def n2w(cls, x, y):
        return cls.w2n(x, y)

    @classmethod
    def e2s(cls, x, y):
        return Tile(x, y, rev_add({_d.EAST: _d.SOUTH}), "╔")

    @classmethod
    def s2e(cls, x, y):
        return cls.e2s(x, y)

    @classmethod
    def e2n(cls, x, y):
        return Tile(x, y, rev_add({_d.EAST: _d.NORTH}), "╚")

    @classmethod
    def n2e(cls, x, y):
        return cls.e2n(x, y)

    def copy(self, x=None, y=None):
        x = x or self.x
        y = y or self.y
        return Tile(x, y, self.mapping, self.symbol)

    @property
    def coord_key(self):
        return coord_key((self.x, self.y))


def print_tiles(tiles):

    coord_map = {t.coord_key: t for t in tiles}

    rows = []
    for j in range(num_rows):
        row = []
        for i in range(num_cols):
            key = coord_key((i, j))
            sym = " "
            if key in coord_map:
                sym = coord_map[key].symbol
            row.append(sym)
        rows.append("".join(row))

    print("\n".join(rows))


def compute_next_coord(tile, entrance):
    exit = tile.mapping[entrance]
    xc = tile.x
    yc = tile.y
    if exit == _d.NORTH:
        yc -= 1
    if exit == _d.SOUTH:
        yc += 1
    if exit == _d.EAST:
        xc += 1
    if exit == _d.WEST:
        xc -= 1
    return (xc, yc)


def generate_random_tracks():
    tiles_by_dir = {
        _d.NORTH: [Tile.vertical(0, 0), Tile.n2e(0, 0), Tile.n2w(0, 0)],
        _d.SOUTH: [Tile.vertical(0, 0), Tile.s2e(0, 0), Tile.s2w(0, 0)],
        _d.WEST: [Tile.horizontal(0, 0), Tile.w2n(0, 0), Tile.w2s(0, 0)],
        _d.EAST: [Tile.horizontal(0, 0), Tile.e2n(0, 0), Tile.e2s(0, 0)],
    }
    tile = Tile.horizontal(10, 10)
    dr = _d.WEST
    tiles = [tile]
    coords = set()
    for i in range(200):
        tile = tiles[-1]
        coord = tile.x, tile.y
        coords.add(tile.coord_key)
        next_coord = compute_next_coord(tile, dr)
        dr = opposing_d[tile.mapping[dr]]

        possible_tiles = [t for t in tiles_by_dir[dr]]
        random.shuffle(possible_tiles)

        for t in possible_tiles:
            contender = t.copy(*next_coord)
            contender_coord = compute_next_coord(contender, dr)
            if (
                coord_key(contender_coord) in coords
                or not (num_cols > contender_coord[0] > 0)
                or not (num_rows > contender_coord[1] > 0)
            ):
                continue
            tiles.append(contender)
            break
        else:
            # print(dr)
            # print(tiles[-1])
            # print(tiles[-2])
            dr = tiles[-2].mapping[opposing_d[tiles[-1].mapping[opposing_d[dr]]]]
            # raise Exception()
            tiles.pop()

    return tiles


def main():
    # tiles = [
    #     Tile.horizontal(0, 0),
    #     Tile.horizontal(1, 0),
    #     Tile.horizontal(2, 0),
    #     Tile.w2s(3, 0),
    #     Tile.vertical(3, 1),
    #     Tile.n2e(3, 2),
    #     Tile.horizontal(4, 2),
    #     Tile.horizontal(5, 2),
    #     Tile.w2n(6, 2),
    #     Tile.s2w(6, 1),
    #     Tile.e2n(5, 1),
    # ]
    tiles = generate_random_tracks()

    print_tiles(tiles)

    coord_mapping = {t.coord_key: t for t in tiles}

    tile = tiles[0]
    entrance = _d.WEST
    coord = (tile.x, tile.y)
    while coord_key(coord) in coord_mapping:
        tile = coord_mapping[coord_key(coord)]
        # print(coord)
        coord = compute_next_coord(tile, entrance)
        entrance = opposing_d[tile.mapping[entrance]]


if __name__ == "__main__":
    main()
