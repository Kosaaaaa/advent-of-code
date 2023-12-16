from __future__ import annotations

import argparse
import os.path
from typing import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

N = support.Point(0, 1)
E = support.Point(1, 0)
S = support.Point(0, -1)
W = support.Point(-1, 0)


def simulate_light(grid: dict[support.Point, str], start: support.Point, initial_d: support.Point) -> int:
    photons = [(start, initial_d)]
    seen = set()
    while photons:
        photon, d = photons.pop()

        if photon not in grid:
            continue

        if (photon, d) in seen:
            continue

        seen.add((photon, d))

        if grid[photon] == '.':
            photons.append((photon + d, d))
        elif grid[photon] == '/':
            # ~d takes N <-> E and S <-> W
            photons.append((photon + ~d, ~d))
        elif grid[photon] == '\\':
            # -~d takes N <-> W and S <-> E
            photons.append((photon + -~d, -~d))
        elif grid[photon] == '|':
            if d in (N, S):
                photons.append((photon + d, d))
            else:
                photons.append((photon + N, N))
                photons.append((photon + S, S))
        elif grid[photon] == '-':
            if d in (E, W):
                photons.append((photon + d, d))
            else:
                photons.append((photon + E, E))
                photons.append((photon + W, W))

    return len({p for p, d in seen})


def part_2_starts(grid: dict[support.Point, str]) -> Generator[tuple[support.Point, support.Point], None, None]:
    max_x = int(max(p.x for p in grid))
    max_y = int(max(p.y for p in grid))

    for x in range(max_x):
        yield support.Point(x, 0), N
        yield support.Point(x, max_y - 1), S

    for y in range(max_y):
        yield support.Point(0, y), E
        yield support.Point(max_x - 1, y), W


def compute(s: str) -> int:
    # Parse problem input.
    grid = {}

    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[support.Point(x, y)] = c

    return max(simulate_light(grid, p, d) for p, d in part_2_starts(grid))


INPUT_S = '\n'.join((
    r'.|...\....',
    r'|.-.\.....',
    r'.....|-...',
    r'........|.',
    r'..........',
    r'.........\\',
    r'..../.\\..',
    r'.-.-/..|..',
    r'.|....-|.\\',
    r'..//.|....',
))
EXPECTED = 51


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
