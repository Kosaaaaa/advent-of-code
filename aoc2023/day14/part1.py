from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move(beams: set[tuple[int, int]], grid: set[tuple[int, int]], dr: int, dc: int, height: int, width: int) -> set[
    tuple[int, int]
]:
    new_grid = set(beams)

    order = sorted(grid, key=lambda rc: rc[::-1])

    for r, c in order:
        new_r, new_c = r + dr, c + dc
        while 0 <= new_r < height and 0 <= new_c < width and (new_r, new_c) not in new_grid:
            new_r += dr
            new_c += dc

        x = (new_r - dr, new_c - dc)
        assert x not in new_grid
        new_grid.add(x)

    return new_grid - beams


def compute(s: str) -> int:
    raw_grid = s.splitlines()
    H, W = len(raw_grid), len(raw_grid[0])

    beams = set()
    grid = set()
    for r, row in enumerate(raw_grid):
        for c, char in enumerate(row):
            if char == '#':
                beams.add((r, c))
            elif char == 'O':
                grid.add((r, c))

    return sum(map(lambda rc: H - rc[0], move(beams, grid, -1, 0, height=H, width=W)))


INPUT_S = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''
EXPECTED = 136


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
