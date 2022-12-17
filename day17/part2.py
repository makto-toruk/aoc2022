from __future__ import annotations

import argparse
import os
from itertools import cycle

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


ROCKS = [
    set([(0, 0), (1, 0), (2, 0), (3, 0)]),  # -
    set([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),  # +
    set([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),  # L
    set([(0, 0), (0, 1), (0, 2), (0, 3)]),  # I
    set([(0, 0), (1, 0), (1, 1), (0, 1)]),  # O
]
N_ROCKS = 1_000_000_000_000
SKYLINES = {}


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


def get_skyline(cs) -> set[tuple[str, str]]:

    ymax = get_max_height(cs)
    ss = set()
    for i in range(6):

        yis = [y for x, y in cs if x == i]
        if yis:
            yi = ymax - max(yis)
        else:
            yi = -1
        ss.add((i, yi))

    return ss


def simulate(i, cs, add):

    ymax = get_max_height(cs)
    ts = ROCKS[i % 5]
    rs = set()
    for x, y in ts:
        rs.add((x + 2, y + (ymax + 4)))

    while True:
        j, d = next(jets)
        skyline = get_skyline(cs)
        if (i % 5, j, frozenset(skyline)) in SKYLINES:
            i_prev, height_prev = SKYLINES[(i % 5, j, frozenset(skyline))]
            period = i - i_prev
            height_curr = get_max_height(cs)
            height_diff = height_curr - height_prev
            n_period = (N_ROCKS - i) // period
            i += n_period * period
            add += n_period * height_diff

        else:
            SKYLINES[(i % 5, j, frozenset(skyline))] = (
                i,
                get_max_height(cs),
            )

        if not blocked(rs, cs, d):
            rs = move(rs, d)

        if not blocked(rs, cs, "v"):
            rs = move(rs, "v")
        else:
            return (i, cs | rs, add)


def compute(input: str) -> int:

    global jets
    jets = cycle(enumerate([x for x in input.splitlines()[0]]))

    i = 0
    cs = set()
    add = 0

    while i < N_ROCKS:
        i, cs, add = simulate(i, cs, add)
        i += 1

    return add + get_max_height(cs) + 1


INPUT_S = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
EXPECTED = 1514285714288


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
