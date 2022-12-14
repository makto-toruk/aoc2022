from __future__ import annotations

import argparse
import os

import numpy as np
import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def matrix_to_string(Y):

    Y = Y.tolist()
    string = ""
    for y in Y:
        for x in y:
            string += x
        string += "\n"

    return string


def draw_line(coords, X):

    for i in range(len(coords) - 1):
        sx, sy = coords[i]
        ex, ey = coords[i + 1]
        if sy == ey:
            m1 = min(sx, ex)
            m2 = max(sx, ex)
            for x in range(m1, m2 + 1):
                X[sy, x] = "#"
        elif sx == ex:
            m1 = min(sy, ey)
            m2 = max(sy, ey)
            for y in range(m1, m2 + 1):
                X[y, sx] = "#"
        else:
            raise ValueError(
                f"not allowed line: ({coords[i]}) -> ({coords[i+1]}"
            )

    return X


def simulate_unit(s, X):

    ymax = X.shape[0]
    y, x = s[0], s[1]

    if y == ymax - 1:
        return X

    if X[y + 1, x] == ".":
        return simulate_unit((y + 1, x), X)
    elif X[y + 1, x - 1] == ".":
        return simulate_unit((y + 1, x - 1), X)
    elif X[y + 1, x + 1] == ".":
        return simulate_unit((y + 1, x + 1), X)
    elif X[y + 1, x] in ["#", "o"]:
        X[y, x] = "o"

    return X


def compute(input: str) -> int:

    xs = input.splitlines()

    X = np.full((1000, 1000), ".")
    for x in xs:
        ps = x.split(" -> ")
        coords = []
        for p in ps:
            t = p.split(",")
            coords.append((int(t[0]), int(t[1])))
        X = draw_line(coords, X)

    # last line
    ys, _ = np.where(X == "#")
    X = X[: max(ys) + 1, :]

    s = (0, 500)
    n = 0
    prev_X = X.copy()
    while 1:
        n += 1
        X = simulate_unit(s, prev_X.copy())
        if np.array_equal(prev_X, X):
            break
        prev_X = X

    return n - 1


INPUT_S = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED = 24


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
