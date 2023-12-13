from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def transpose(grid: list[str]) -> list[str]:
    return list(map(''.join, zip(*grid)))


def count_differences(a: list[str], b: list[str]) -> int:
    diff = 0
    for linea, lineb in zip(a, b):
        diff += sum(chara != charb for chara, charb in zip(linea, lineb))
        if diff > 1:
            break

    return diff


def find_reflections(grid: list[str]) -> int:
    height = len(grid)
    imperfect = 0

    for size in range(1, height // 2 + 1):
        a = grid[:size]
        b = grid[2 * size - 1:size - 1:-1]
        diff = count_differences(a, b)

        if diff == 1:
            imperfect = size

        if imperfect:
            break

        a = grid[height - 2 * size:height - size]
        b = grid[height - 1:height - size - 1:-1]
        diff = count_differences(a, b)

        if diff == 1:
            imperfect = height - size

        if imperfect:
            break

    return imperfect


def compute(s: str) -> int:
    total = 0

    grids = s.split('\n\n')

    for line in map(str.splitlines, grids):
        imperfect = find_reflections(line)
        total += 100 * imperfect

        imperfect = find_reflections(transpose(line))
        total += imperfect

    return total


INPUT_S = '''\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''
EXPECTED = 400


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
