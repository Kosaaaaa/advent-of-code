from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def encode(n: int) -> str:
    ret = ''
    while n:
        rem = n % 5
        if rem <= 2:
            ret += str(rem)
        else:
            ret += {3: '=', 4: '-'}[rem]

        n //= 5
        n += rem // 3

    return ret[::-1]


def compute_value(s: str) -> int:
    ret = 0
    for line in s.splitlines():
        n = 0
        for i, c in enumerate(reversed(line)):
            if c.isdigit():
                n += int(c) * (5 ** i)
            elif c == '-':
                n -= 1 * (5 ** i)
            elif c == '=':
                n -= 2 * (5 ** i)
        ret += n
    return ret


def compute(s: str) -> str:
    return encode(compute_value(s))


INPUT_S = '''\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
'''
EXPECTED = '2=-1=0'


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
