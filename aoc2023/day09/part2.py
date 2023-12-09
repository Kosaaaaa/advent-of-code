from __future__ import annotations

import argparse
import os.path
from functools import reduce
from typing import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def extrapolate(v: list[int]) -> int:
    derivatives = [v]
    while any(derivatives[-1]):
        derivatives.append(
            [
                y - x
                for x, y in zip(derivatives[-1], derivatives[-1][1:])
            ],
        )

    return reduce(lambda first, d: d[0] - first, reversed(derivatives), 0)


def compute(s: str) -> int:
    def f() -> Generator[int, None, None]:
        for line in s.splitlines():
            yield extrapolate([int(x) for x in line.split()])

    return sum(f())


INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
EXPECTED = 2


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
