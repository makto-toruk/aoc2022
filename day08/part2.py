from __future__ import annotations

import argparse
import os

import numpy as np
import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def scenic_score(i, j, X):

    h = X[i, j]
    imax, jmax = X.shape
    if i == 0 or j == 0 or i == imax - 1 or j == jmax - 1:
        return 0
    else:
        left = X[:i, j][::-1]
        right = X[i + 1 :, j]
        up = X[i, :j][::-1]
        down = X[i, j + 1 :]
        dirs = [left, right, up, down]

        score = 1
        for dir in dirs:
            s = 0
            for t in dir:
                s += 1
                if t >= h:
                    break
            score *= s

    return score


def compute(input: str) -> int:

    xs = input.splitlines()

    X = []
    for x in xs:
        X.append([int(i) for i in x])
    X = np.array(X)

    imax, jmax = X.shape
    scores = []
    for i in range(imax):
        for j in range(jmax):
            scores.append(scenic_score(i, j, X))

    return max(scores)


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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
