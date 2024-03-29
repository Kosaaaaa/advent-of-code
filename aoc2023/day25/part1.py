from __future__ import annotations

import argparse
import operator
import os.path
from functools import reduce

import networkx
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # Parse problem input.
    graph = networkx.Graph()

    for line in s.splitlines():
        src, rest = line.strip().split(': ')
        graph.add_node(src)
        for dest in rest.split():
            graph.add_edge(src, dest)

    # Solve part 1.
    for a, b in networkx.minimum_edge_cut(graph):
        graph.remove_edge(a, b)

    return reduce(operator.mul, (len(c) for c in networkx.connected_components(graph)), 1)


INPUT_S = '''\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
'''
EXPECTED = 54


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
