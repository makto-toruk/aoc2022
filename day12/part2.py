from __future__ import annotations

import argparse
import os

import numpy as np
import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

ROUTES = {}


def get_adjacent(i, j, X):

    imax, jmax = X.shape
    adjacent = []
    if i > 0:
        adjacent.append((i - 1, j))
    if i < imax - 1:
        adjacent.append((i + 1, j))
    if j > 0:
        adjacent.append((i, j - 1))
    if j < jmax - 1:
        adjacent.append((i, j + 1))

    return adjacent


def cord(s):

    if s == "E":
        return ord("z")
    elif s == "S":
        return ord("a")
    else:
        return ord(s)


def min_length(X, s):

    dist = {s: 0}
    curr = s
    visited = set()

    while X[curr] != "E":
        visited.add(curr)
        ps = get_adjacent(curr[0], curr[1], X)
        d = dist[curr]

        for p in ps:
            if cord(X[p]) <= cord(X[curr]) + 1:
                distance = 1 + d
                if p not in dist:
                    dist[p] = distance
                else:
                    temp = dist[p]
                    if temp > distance:
                        dist[p] = distance

        candidates = {n: dist[n] for n in dist if n not in visited}

        if not candidates:
            return 1_000_000_000

        curr = min(candidates, key=lambda k: candidates[k])

    return dist[curr]


def compute(input: str) -> int:

    xs = input.splitlines()

    X = []
    for x in xs:
        X.append([c for c in x])

    X = np.array(X)
    S = []
    i_s, j_s = np.where((X == "a") | (X == "S"))
    for i, j in zip(i_s, j_s):
        S.append((i, j))

    paths = [min_length(X, p) for p in S]

    return min(paths)


INPUT_S = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 29


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
