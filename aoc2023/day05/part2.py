from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    seeds = [*map(int, lines[0].split(': ')[1].split())]
    maps = [[[*map(int, n.split())] for n in i.split('\n')[1:]] for i in '\n'.join(lines[2:]).split('\n\n')]

    locations: list[tuple[int, ...]] = []
    for pair in ((seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)):
        remain: deque[tuple[int, ...]] = deque([pair])
        result: deque[tuple[int, ...]] = deque()

        for _map in maps:
            while remain:
                cur = remain.pop()  # cur = x-y
                for dest, src, rng in _map:  # src-(src+rng-1) = a-b
                    if cur[1] < src or src + rng <= cur[0]:  # no overlap, x-y-a-b or a-b-x-y
                        continue
                    elif src <= cur[0] <= cur[1] < src + rng:  # a-x-y-b
                        offset = cur[0] - src
                        result.append((dest + offset, dest + offset + cur[1] - cur[0]))
                        break
                    elif cur[0] < src <= cur[1] < src + rng:  # x-a-y-b
                        offset = cur[1] - src
                        result.append((dest, dest + offset))
                        remain.append((cur[0], src - 1))
                        break
                    elif src <= cur[0] < src + rng <= cur[1]:  # a-x-b-y
                        offset = cur[0] - src
                        result.append((dest + offset, dest + rng - 1))
                        remain.append((src + rng, cur[1]))
                        break
                    elif cur[0] < src <= src + rng <= cur[1]:  # x-a-b-y
                        result.append((dest, dest + rng - 1))
                        remain.append((cur[0], src - 1))
                        remain.append((src + rng, cur[1]))
                        break
                else:  # didn't match any source range
                    result.append(cur)
            remain = deque(result)
            result.clear()
        locations += remain

    return min(i[0] for i in locations)


INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
EXPECTED = 46


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
