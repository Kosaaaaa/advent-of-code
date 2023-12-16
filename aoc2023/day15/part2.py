from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def hash_code(code: str) -> int:
    result = 0

    for c in code:
        result += ord(c)
        result *= 17
        result %= 256

    return result


def compute_boxes(s: str) -> dict[int, list[tuple[str, int]]]:
    boxes: dict[int, list[tuple[str, int]]] = defaultdict(list)

    for step in s.strip().split(','):
        if step[-1] == '-':
            label = step[:-1]
            box = hash_code(label)
            boxes[box] = [lens for lens in boxes[box] if lens[0] != label]
            continue

        focal = int(step[-1])
        label = step[:-2]
        box = hash_code(label)

        for i, (other_label, other_focal) in enumerate(boxes[box]):
            if other_label == label:
                boxes[box][i] = (label, focal)
                break
        else:
            boxes[box].append((label, focal))

    return boxes


def compute(s: str) -> int:
    lenses: dict[str, int] = {}

    for box_num, box in compute_boxes(s).items():
        for slot_num, (label, focal) in enumerate(box, start=1):
            lenses[label] = (box_num + 1) * slot_num * focal

    return sum(lenses.values())


INPUT_S = '''\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''
EXPECTED = 145


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
