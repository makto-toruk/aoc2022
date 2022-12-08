from __future__ import annotations

import argparse
import os

import numpy as np
import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def is_visible(i, j, X):

    imax, jmax = X.shape
    h = X[i, j]
    if i == 0 or j == 0 or i == imax - 1 or j == jmax - 1:
        return True
    else:
        if (
            (np.max(X[:i, j]) < h)
            or (np.max(X[i + 1 :, j]) < h)
            or (np.max(X[i, :j]) < h)
            or (np.max(X[i, j + 1 :]) < h)
        ):
            return True


def compute(input: str) -> int:

    xs = input.splitlines()

    X = []
    for x in xs:
        X.append([int(i) for i in x])
    X = np.array(X)

    n = 0
    imax, jmax = X.shape
    for i in range(imax):
        for j in range(jmax):
            if is_visible(i, j, X):
                n += 1

    return n


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


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
