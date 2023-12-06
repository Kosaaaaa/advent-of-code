from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    nums = [_num for _num in re.findall(r'\d+', s)]
    race = [int(''.join([n for n in nums[:int(len(nums) / 2)]])), int(''.join([n for n in nums[int(len(nums) / 2):]]))]

    total = 1

    t, d = race

    interval_1 = (t + ((t ** 2) - (4 * d)) ** 0.5) / 2
    interval_2 = (t - ((t ** 2) - (4 * d)) ** 0.5) / 2

    if interval_1 < interval_2:
        num = int(interval_2) - int(interval_1)
    else:
        num = int(interval_1) - int(interval_2)
    if interval_1 % 1 == 0:
        num -= 1

    total *= num

    return total


INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 71503


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
