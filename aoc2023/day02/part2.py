from __future__ import annotations

import argparse
import os.path
import re
from functools import reduce

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
PATTERN_RE = re.compile(r'Game (\d+): (.*)')


def compute(s: str) -> int:
    lines = s.splitlines()

    games = [
        (int(idx), record.split(';'))
        for idx, record in [
            PATTERN_RE.match(line).groups()  # type: ignore
            for line in lines
        ]
    ]

    bag = {'red': 12, 'green': 13, 'blue': 14}

    power = 0

    for idx, record in games:
        fewest_cubes_bag = {'red': 0, 'green': 0, 'blue': 0}
        for r in record:
            record_bag = {
                color: int(count)
                for count, color in (cube.split() for cube in r.split(','))
            }

            fewest_cubes_bag = {
                color: max(fewest_cubes_bag[color], record_bag.get(color, 0)) for color in bag
            }
        power += reduce(lambda x, y: x * y, fewest_cubes_bag.values())

    return power


INPUT_S = '''\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''
EXPECTED = 2286


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
