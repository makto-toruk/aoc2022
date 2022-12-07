from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class Object:
    def __init__(self, name: str, parent: Dir, size: int) -> None:
        self.name = name
        self.parent = parent
        self.size = size


class Dir:
    def __init__(
        self,
        name: str,
        parent: Dir | None,
        children: set[Dir | Object] = set(),
        size: int = 0,
    ) -> None:
        self.name = name
        self.parent = parent
        self.children = children
        self.size = size

    def add_size(self, size):
        self.size += size

    def __str__(self) -> str:
        cs = None
        if len(self.children) > 0:
            cs = [c.name for c in self.children]
        s = f"""
        name: {self.name}
        parent: {self.parent.name if self.parent else None}
        children: {cs}
        size: {self.size}
        """
        return s


def parse_directories(dir):

    for c in dir.children:
        if isinstance(c, Dir):
            yield c.size
            yield from parse_directories(c)


def compute(input: str) -> int:

    xs = input.splitlines()

    home = Dir("/", None)
    for x in xs:
        if x.startswith("$ cd"):
            _, y = x.split("$ cd ")
            if y == "/":
                pwd = home
            elif y == "..":
                pwd = pwd.parent
            else:
                for c in pwd.children:
                    if c.name == y:
                        pwd = c
                        continue
        elif x.startswith("$ ls"):
            continue
        elif x.startswith("dir"):
            c = x.split(" ")[1]
            pwd.children.add(Dir(c, pwd, set()))
        else:
            size, name = x.split(" ")
            if size.isnumeric():
                size = int(size)
                pwd.children.add(Object(name, pwd, size))

                pwd.add_size(size)
                cwd = pwd
                while cwd.parent:
                    cwd.parent.add_size(size)
                    cwd = cwd.parent
            else:
                raise ValueError(f"{x}: not valid")

    sizes = list(parse_directories(home)) + [home.size]

    unused = 70000000 - home.size
    required = 30000000
    to_delete = required - unused

    return min([s for s in sizes if s >= to_delete])


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
