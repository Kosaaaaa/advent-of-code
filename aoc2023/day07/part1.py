from __future__ import annotations

import argparse
import os.path
from collections import Counter

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    hands: list[tuple[str, int]] = [
        (parts[0], int(parts[1]))
        for line in s.splitlines()
        if (parts := line.split()) and len(parts) == 2
    ]

    labels = dict(zip('23456789TJQKA', range(13)))

    def calc(hand: tuple[str, int]) -> tuple[list[int], list[int]]:
        return sorted(Counter(hand[0]).values(), reverse=True), [labels[c] for c in hand[0]]

    return sum(bid * (i + 1) for i, (_, bid) in enumerate(sorted(hands, key=calc)))


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 6440


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
