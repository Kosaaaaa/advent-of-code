from __future__ import annotations

import argparse
import os.path
from math import lcm

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    network = {}

    lines = s.splitlines()

    for line in lines[2:]:
        node, connections = line.split(' = ')
        left, right = connections.strip('()').split(', ')
        network[node] = (left, right)

    instructions = lines[0]

    starts = [node for node in network if node.endswith('A')]
    count = len(starts)
    nodes = list(starts)
    steps = 0
    loops: list[int] = []
    journey = {node: [(node, 0)] for node in nodes}

    while len(loops) < count:
        idx = steps % len(instructions)
        steps += 1
        LR = 0 if instructions[idx] == 'L' else 1
        nodes = [network[node][LR] for node in nodes]
        for start, current in zip(starts, nodes):
            if (current, idx) in journey[start]:
                loops.append(steps - journey[start].index((current, idx)))
                nodes.remove(current)
                starts.remove(start)
            journey[start].append((current, idx))

    return lcm(*loops)


INPUT_S = '''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''
EXPECTED = 6


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
