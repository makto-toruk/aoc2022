from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def get_dirsum(subtree):

    sum = 0
    for _, v in subtree.items():
        if isinstance(v, int):
            sum += v
        else:
            sum += get_dirsum(v)

    return sum


def parse_subtrees(tree):

    for v in tree.values():
        yield v
        if isinstance(v, dict):
            yield from parse_subtrees(v)


def compute(input: str) -> int:

    xs = input.splitlines()

    tree = {"/": {}}
    history = ["/"]
    for x in xs:
        if x.startswith("$ cd"):
            _, y = x.split("$ cd ")
            if y == "/":
                head = "/"
                subtree = tree[head]
                history = ["/"]
                tree_history = [subtree]
            elif y == "..":
                head = history[-2]
                history = history[:-1]
                subtree = tree_history[-2]
                tree_history = tree_history[:-1]
            else:
                if y not in subtree:
                    subtree[y] = {}
                history.append(y)
                tree_history.append(subtree[y])
                head = y
                subtree = subtree[head]
        elif x.startswith("$ ls"):
            continue
        else:
            a, b = x.split(" ")
            if a.isnumeric():
                subtree[b] = int(a)
            else:
                if b not in subtree:
                    subtree[b] = {}

    dir_sum = []
    for x in parse_subtrees(tree):
        if isinstance(x, dict):
            dir_sum.append(get_dirsum(x))

    total = max(dir_sum)
    unused_space = 70000000 - total
    min_unused_space = 30000000
    to_delete = min_unused_space - unused_space

    return min([s for s in dir_sum if s >= to_delete])


INPUT_S = """\
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
"""
EXPECTED = 24933642


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.input) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
