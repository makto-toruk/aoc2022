from __future__ import annotations

import argparse
import os

import numpy as np
import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def matrix_to_string(Y):

    string = ""
    for y in Y:
        for x in y:
            string += x
        string += "\n"

    return string


def update(cycle, X, XS):

    x = (cycle) % 40
    y = (cycle) // 40

    if x in [X - 1, X, X + 1]:
        XS[y, x] = "#"

    return XS


def compute(input: str) -> str:

    xs = input.splitlines()

    X = 1
    XS = np.array([["."] * 40] * 6)
    X = 1
    cycle = 0
    XS = update(cycle, X, XS)
    for x in xs:
        if x == "noop":
            cycle += 1
            XS = update(cycle, X, XS)
        else:
            mag = int(x.split()[1])
            cycle += 1
            XS = update(cycle, X, XS)

            cycle += 1
            X += mag
            XS = update(cycle, X, XS)

    return matrix_to_string(XS)


INPUT_S = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
EXPECTED = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: str) -> None:
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
