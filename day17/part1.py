from __future__ import annotations

import argparse
import os
from itertools import cycle

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def show_cave(cs: set[tuple[int, int]]) -> None:
    xmin = min(x for x, _ in cs)
    xmax = max(x for x, _ in cs)
    ymin = min(y for _, y in cs)
    ymax = max(y for _, y in cs)
    s = "\n".join(
        "".join("#" if (x, y) in cs else "." for x in range(xmin, xmax + 1))
        for y in range(ymax, ymin - 1, -1)
    )

    print(s)

    return None


ROCKS = [
    set([(0, 0), (1, 0), (2, 0), (3, 0)]),  # -
    set([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),  # +
    set([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),  # L
    set([(0, 0), (0, 1), (0, 2), (0, 3)]),  # I
    set([(0, 0), (1, 0), (1, 1), (0, 1)]),  # O
]


def blocked(rs: set[tuple[int, int]], cs: set[tuple[int, int]], d: str):

    match d:
        case "<":
            if cs:
                for rx, ry in rs:
                    if (rx - 1, ry) in cs:
                        return True
            for rx, _ in rs:
                if rx == 0:
                    return True

        case ">":
            if cs:
                for rx, ry in rs:
                    if (rx + 1, ry) in cs:
                        return True
            for rx, _ in rs:
                if rx == 6:
                    return True

        case "v":
            if cs:
                for rx, ry in rs:
                    if (rx, ry - 1) in cs:
                        return True
            else:
                for _, ry in rs:
                    if ry == 0:
                        return True

        case _:
            raise ValueError(f"unknown direction: {d}")

    return False


def move(rs: set[tuple[int, int]], d: str):
    # always checks before if it's possible to move
    match d:
        case "<":
            ts = set()
            for rx, ry in rs:
                ts.add((rx - 1, ry))
            rs = ts
        case ">":
            ts = set()
            for rx, ry in rs:
                ts.add((rx + 1, ry))
            rs = ts
        case "v":
            ts = set()
            for rx, ry in rs:
                ts.add((rx, ry - 1))
            rs = ts
        case _:
            raise ValueError(f"unknown direction: {d}")

    return rs


def get_max_height(cs: set):

    if not cs:
        return -1
    else:
        return max(y for _, y in cs)


def simulate(i, cs):

    ymax = get_max_height(cs)
    ts = ROCKS[i % 5]
    rs = set()
    for x, y in ts:
        rs.add((x + 2, y + (ymax + 4)))

    while True:
        _, d = next(jets)
        if not blocked(rs, cs, d):
            rs = move(rs, d)

        if not blocked(rs, cs, "v"):
            rs = move(rs, "v")
        else:
            return cs | rs


def compute(input: str) -> int:

    global jets
    jets = cycle(enumerate([x for x in input.splitlines()[0]]))

    n_rocks = 2022
    cave = set()
    for i in range(n_rocks):
        cave = simulate(i, cave)

    return max([y for _, y in cave]) + 1


INPUT_S = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
EXPECTED = 3068


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
