from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PATTERN_RE = re.compile(r'^\D*(\d)(?:.*?(\d))?\D*$')

WORDS_DIGITS_MAP = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

PAT = re.compile(fr'(\d|{"|".join(WORDS_DIGITS_MAP)})')
PAT_REV = re.compile(fr'(\d|{"|".join(s[::-1] for s in WORDS_DIGITS_MAP)})')


def _parse_search(p: re.Pattern[str], s: str) -> str:
    match = p.search(s)
    assert match is not None
    return match[0]


def compute(s: str) -> int:
    lines = s.splitlines()

    result = 0

    for line in lines:
        first = _parse_search(PAT, line)
        last = _parse_search(PAT_REV, line[::-1])[::-1]
        digits = [WORDS_DIGITS_MAP.get(first, first), WORDS_DIGITS_MAP.get(last, last)]
        result += int(digits[0]) * 10 + int(digits[-1])

    return result


INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
EXPECTED = 281


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
