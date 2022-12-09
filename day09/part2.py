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
    T = [(0, 0)] * 9
    history = set([(0, 0)])
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
            for j, t in enumerate(T):
                if j == 0:
                    if not in_vicinity(h, t):
                        T[0] = move(h, t)
                else:
                    if not in_vicinity(T[j - 1], T[j]):
                        T[j] = move(T[j - 1], T[j])

                history.add(T[-1])

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
EXPECTED = 1
INPUT_S2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED2 = 36


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
    ),
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
