from __future__ import annotations

import argparse
import os

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def adjacent(d):

    x, y, z = d

    f = (x, y, z + 1)
    b = (x, y, z - 1)
    u = (x, y + 1, z)
    d = (x, y - 1, z)
    l = (x - 1, y, z)
    r = (x + 1, y, z)

    return set([f, b, u, d, l, r])


EXITS = {}


def check_exit(d, ds, visited):

    visited.add(d)

    if d in EXITS:
        return EXITS[d]

    us = adjacent(d) - visited - ds
    if not us:
        return False

    xmax = max(x for x, _, _ in ds)
    ymax = max(y for _, y, _ in ds)
    zmax = max(z for _, _, z in ds)
    xmin = min(x for x, _, _ in ds)
    ymin = min(y for _, y, _ in ds)
    zmin = min(z for _, _, z in ds)

    for u in us:
        ux, uy, uz = u
        if (
            (ux < xmin or ux > xmax)
            or (uy < ymin or uy > ymax)
            or (uz < zmin or uz > zmax)
        ):
            return True

        if check_exit(u, ds, visited.copy()):
            EXITS[u] = True
            return True

    EXITS[d] = False

    return False


def count_sides(d, ds):

    x, y, z = d
    f = (x, y, z + 1)
    b = (x, y, z - 1)
    u = (x, y + 1, z)
    d = (x, y - 1, z)
    l = (x - 1, y, z)
    r = (x + 1, y, z)

    n = 0
    for s in [f, b, u, d, l, r]:
        if s not in ds:
            visited = set()
            if check_exit(s, ds, visited):
                n += 1
    return n


def compute(input: str) -> int:

    xs = input.splitlines()

    ds = set()
    for x in xs:
        ds.add(tuple(support.ints(x)))

    n = 0
    for d in ds:
        n += count_sides(d, ds)

    return n


INPUT_S = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
EXPECTED = 58


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
