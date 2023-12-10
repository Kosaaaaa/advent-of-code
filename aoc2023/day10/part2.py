from __future__ import annotations

import argparse
import os.path
from typing import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

EMPTY_FIELD = (False, False, False, False)
FieldT = tuple[bool, bool, bool, bool]
CordsT = tuple[int, int]


def parse_schema(raw_map: dict[CordsT, str]) -> dict[CordsT, FieldT]:
    result = {}

    # transform map to pipe schematic
    for point, value in raw_map.items():
        if value == '|':
            result[point] = (True, False, True, False)
        elif value == '-':
            result[point] = (False, True, False, True)
        elif value == 'L':
            result[point] = (True, True, False, False)
        elif value == 'J':
            result[point] = (True, False, False, True)
        elif value == '7':
            result[point] = (False, False, True, True)
        elif value == 'F':
            result[point] = (False, True, True, False)
        elif value == '.':
            result[point] = EMPTY_FIELD

    return result


def find_starting_point(
        start_point: CordsT,
        schema: dict[CordsT, FieldT],
) -> FieldT:
    return (
        schema.get((start_point[0] - 1, start_point[1]), EMPTY_FIELD)[2],
        schema.get((start_point[0], start_point[1] + 1), EMPTY_FIELD)[3],
        schema.get((start_point[0] + 1, start_point[1]), EMPTY_FIELD)[0],
        schema.get((start_point[0], start_point[1] - 1), EMPTY_FIELD)[1],
    )


def get_neighbors(
        pipe_schematic: dict[CordsT, FieldT], row_index: int,
        column_index: int,
) -> Generator[CordsT, None, None]:
    schema = pipe_schematic[row_index, column_index]

    if schema[0]:
        yield row_index - 1, column_index

    if schema[1]:
        yield row_index, column_index + 1

    if schema[2]:
        yield row_index + 1, column_index

    if schema[3]:
        yield row_index, column_index - 1


def get_neighbors_from_schema(pipe_schematic: dict[CordsT, FieldT], point: CordsT) -> Generator[CordsT, None, None]:
    row, column = point
    if (row // 2, column // 2) not in pipe_schematic:
        return

    schema = pipe_schematic[row // 2, column // 2]

    if row % 2 == 0:
        yield row - 1, column

        if (column % 2 == 0 and not schema[3]) or (column % 2 == 1 and not schema[1]):
            yield row + 1, column
    else:
        if (column % 2 == 0 and not schema[3]) or (column % 2 == 1 and not schema[1]):
            yield row - 1, column

        yield row + 1, column

    if column % 2 == 0:
        yield row, column - 1

        if (row % 2 == 0 and not schema[0]) or (row % 2 == 1 and not schema[2]):
            yield row, column + 1
    else:
        if (row % 2 == 0 and not schema[0]) or (row % 2 == 1 and not schema[2]):
            yield row, column - 1

        yield row, column + 1


def bfs(schema: dict[CordsT, FieldT], start: CordsT) -> dict[CordsT, int]:
    to_check = [start]
    cost_so_far = dict()
    cost_so_far[start] = 0

    while to_check:
        row_index, column_index = to_check.pop()

        for new_point in get_neighbors(schema, row_index, column_index):
            new_cost = cost_so_far[row_index, column_index] + 1

            if new_point not in cost_so_far or new_cost < cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost
                to_check.append(new_point)

    return cost_so_far


def find_outsiders_elements(pipe_schematic: dict[CordsT, FieldT]) -> set[CordsT]:
    to_check = [(0, 0)]
    rescaled_outside = set()

    while to_check:
        point = to_check.pop()
        if point in rescaled_outside:
            continue

        rescaled_outside.add(point)

        for p in get_neighbors_from_schema(pipe_schematic, point):
            to_check.append(p)

    result = set()
    for point in rescaled_outside:
        if point[0] % 2 != 0 or point[1] % 2 != 0:
            continue

        row = (point[0] // 2) * 2
        column = (point[1] // 2) * 2

        if (row, column) in rescaled_outside and \
                (row + 1, column) in rescaled_outside and \
                (row + 1, column + 1) in rescaled_outside and \
                (row, column + 1) in rescaled_outside:
            result.add((row, column))

    return result


def compute(s: str) -> int:
    raw_map = {}

    for row_index, line in enumerate(s.splitlines()):
        for column_index, character in enumerate(line):
            raw_map[row_index, column_index] = character

    pipe_schematic = parse_schema(raw_map)

    starting_position = next(c for c, v in raw_map.items() if v == 'S')
    pipe_schematic[starting_position] = find_starting_point(starting_position, pipe_schematic)
    main_loop_pipes_positions = bfs(pipe_schematic, starting_position).keys()
    clean_schematic_map = {
        key: (value if key in main_loop_pipes_positions else EMPTY_FIELD)
        for key, value in pipe_schematic.items()
    }

    outsiders_elements = find_outsiders_elements(clean_schematic_map)

    return len(pipe_schematic) - len(main_loop_pipes_positions) - len(outsiders_elements)


INPUT_S = '''\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
'''
EXPECTED = 4


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
