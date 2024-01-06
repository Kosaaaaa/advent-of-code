from __future__ import annotations

import argparse
import heapq
import os.path
from typing import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = [
    support.Point(0, 1),  # north
    support.Point(1, 0),  # east
    support.Point(0, -1),  # south
    support.Point(-1, 0),  # west
]


def minimize_heat_loss(graph: dict[support.Point, int], start: support.Point, goal: support.Point) -> int | None:
    def gen_neighbours(node: support.Point, last_dir: support.Point | None, last_count: int) -> Generator[
        tuple[support.Point, int, support.Point], None, None,
    ]:
        for d in DIRS:
            n = node + d
            if n not in graph:
                continue

            if last_dir is not None:
                # No U-turns allowed.
                if last_dir == -d:
                    continue

                # Unstable regular crucible.
                if last_count == 3 and last_dir == d:
                    continue

            yield n, graph[n], d

    horizon = [(0, start, None, 0)]
    seen = set()

    while horizon:
        depth, curr, last_dir, last_count = heapq.heappop(horizon)

        if (curr, last_dir, last_count) in seen:
            continue

        seen.add((curr, last_dir, last_count))

        if curr == goal:
            return depth

        for neighbour, weight, nd in gen_neighbours(curr, last_dir, last_count):
            new_cost = weight + depth
            new_count = 1 if nd != last_dir else last_count + 1
            heapq.heappush(horizon, (new_cost, neighbour, nd, new_count))  # type: ignore

    return None


def compute(s: str) -> int:
    graph = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            graph[support.Point(x, y)] = int(c)

    start = support.Point(0, 0)
    end = support.Point(x, y)

    return minimize_heat_loss(graph, start, end) or 0


INPUT_S = '''\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''
EXPECTED = 102


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
