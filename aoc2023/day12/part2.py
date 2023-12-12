from __future__ import annotations

import argparse
import functools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
GROUP_RE = re.compile(r'(#+)\.')


def parse_input(line: str) -> tuple[str, list[int]]:
    spl = line.split(' ')
    row = '?'.join([spl[0]] * 5).strip('.')
    groups = [int(x) for x in spl[1].split(',')] * 5
    return row, groups


def calc_groups(row: str) -> tuple[int, ...]:
    groups = []
    group_len = 0
    prev_char = '.'
    for r in row:
        if r == '#':
            group_len += 1
        elif prev_char == '#':
            groups.append(group_len)
            group_len = 0
        prev_char = r
    if group_len > 0:
        groups.append(group_len)
    return tuple(groups)


@functools.lru_cache(maxsize=100_000)
def arrangements(row: str, groups: tuple[int, ...]) -> int:
    row = row.lstrip('.')
    if '?' not in row:
        expected_groups = calc_groups(row)
        if expected_groups != groups:
            return 0
        return 1

    first_unk_index = row.index('?')
    total = 0
    for opt in ['.', '#']:
        new_row = row[:first_unk_index] + opt + row[first_unk_index + 1:]
        new_row = new_row.lstrip('.')

        # try dropping initial seq of hashes
        if m := GROUP_RE.match(row):
            group_len = len(m.group(1))
            if not groups or groups[0] != group_len:
                continue  # not a valid solution
            total += arrangements(new_row[group_len:], groups[1:])
        else:
            total += arrangements(new_row, groups)

    return total


def compute(s: str) -> int:
    total = 0
    for line in s.splitlines():
        row, groups = parse_input(line)
        total += arrangements(row, tuple(groups))
    return total


INPUT_S = '''\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''
EXPECTED = 525152


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
