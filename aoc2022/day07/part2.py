from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

TOTAL = 70000000
NEED = 30000000


def dir_size(files: dict[str, int], dirname: str) -> int:
    sz = 0
    for k, v in files.items():
        if k.startswith(f'{dirname}/'):
            sz += v

    return sz


def compute(s: str) -> int:
    files = {}
    dirs = {'/'}

    pwd = '/'
    in_ls = False
    for line in s.splitlines()[1:]:
        if in_ls and line.startswith('$'):
            in_ls = False
        elif in_ls and line.startswith('dir '):
            _, dirname = line.split(' ', 1)
            dirs.add(os.path.join(pwd, dirname))
            continue
        elif in_ls:
            sz, filename = line.split(' ', 1)
            files[os.path.join(pwd, filename)] = int(sz)
            continue

        if line == '$ ls':
            in_ls = True
        elif line == '$ cd ..':
            pwd = os.path.dirname(pwd) or '/'
        elif line.startswith('$ cd'):
            pwd = os.path.join(pwd, line.split(' ', 2)[-1])
        else:
            raise AssertionError(line)

    root = sum(files.values())
    sizes = [root] + [dir_size(files, dirname) for dirname in dirs]
    sizes.sort()

    need_to_delete = NEED - (TOTAL - root)
    sizes = [size for size in sizes if size >= need_to_delete]
    sizes.sort()
    return sizes[0]


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642


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
