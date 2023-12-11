from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

EXPANSION = 1_000_000


def parse_galaxies(s: str, expansion: int = EXPANSION) -> list[tuple[int, int]]:
    lines = s.splitlines()

    empty_columns = [
        all(line[i] == '.' for line in lines)
        for i in range(len(lines[0]))
    ]
    galaxies = []
    x, y = 0, 0

    for line in lines:
        x = 0
        y += expansion if set(line) == {'.'} else 1
        for i, element in enumerate(line):
            x += expansion if empty_columns[i] else 1
            if element == '#':
                galaxies.append((x, y))

    return galaxies


def compute(s: str, expansion: int | None = None) -> int:
    if expansion is not None:
        galaxies = parse_galaxies(s, expansion)
    else:
        galaxies = parse_galaxies(s)

    total = 0
    for i, galaxy1 in enumerate(galaxies):
        for galaxy2 in galaxies[i + 1:]:
            dist = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
            total += dist

    return total


INPUT_S = '''\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''
EXPECTED = 8410


@pytest.mark.parametrize(
    ('input_s', 'expansion', 'expected'),
    (
        (INPUT_S, 100, EXPECTED),
    ),
)
def test(input_s: str, expansion: int, expected: int) -> None:
    assert compute(input_s, expansion) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
