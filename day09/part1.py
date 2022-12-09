from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def in_vicinity(h, t):

    x1, y1 = h
    x2, y2 = t

    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
        return True
    else:
        return False


def move(h, t):

    x1, y1 = h
    x2, y2 = t

    if abs(x1 - x2) == 2 and abs(y1 - y2) == 1:
        return ((x1 + x2) // 2, y1)
    elif abs(x1 - x2) == 1 and abs(y1 - y2) == 2:
        return (x1, (y1 + y2) // 2)
    else:
        return ((x1 + x2) // 2, (y1 + y2) // 2)


def compute(input: str) -> int:

    xs = input.splitlines()

    h = (0, 0)
    t = (0, 0)
    history = set([t])
    for x in xs:
        dir, mag = x.split()
        mag = int(mag)

        if dir == "R":
            xstep, ystep = 1, 0
        elif dir == "L":
            xstep, ystep = -1, 0
        elif dir == "U":
            xstep, ystep = 0, 1
        elif dir == "D":
            xstep, ystep = 0, -1

        for _ in range(mag):
            h = (h[0] + xstep, h[1] + ystep)
            if not in_vicinity(h, t):
                t = move(h, t)
                history.add(t)

    return len(history)


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


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
