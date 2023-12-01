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


def parse_words_digits(s: str) -> str:
    found_substrings = [(w, [m.start() for m in re.finditer(w, s)]) for w
                        in WORDS_DIGITS_MAP.keys() if re.search(w, s)]

    for word, _ in sorted(found_substrings, key=lambda _x: _x[1][0]):
        s = s.replace(word, WORDS_DIGITS_MAP[word])

    return s


def compute(s: str) -> int:
    lines = s.splitlines()

    result = 0

    for line in lines:
        if match := PATTERN_RE.search(parse_words_digits(line)):
            first, last = match.groups()

            if last is None:
                last = first

            result += int(f'{first}{last}')

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
        ('two1nine', '219'),
        ('eightwothree', '8wo3'),
        ('abcone2threexyz', 'abc123xyz'),
        ('xtwone3four', 'x2ne34'),
        ('4nineeightseven2', '49872'),
        ('zoneight234', 'z1ight234'),
        ('onezvbhrblrkzcrsevensix96jnpxjone', '1zvbhrblrkzcr7696jnpxj1'),
        ('nineight', '9ight'),
        ('1nineight', '19ight'),
    ),
)
def test_parse_words_digits(input_s: str, expected: str) -> None:
    assert parse_words_digits(input_s) == expected


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
