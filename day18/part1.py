from __future__ import annotations

import argparse
import os

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


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
EXPECTED = 64


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
