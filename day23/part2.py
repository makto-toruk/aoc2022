from __future__ import annotations

import argparse
import os
from collections import Counter

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def print_grid(cs: set[tuple[int, int]]) -> None:
    xmin = min(x for x, _ in cs)
    xmax = max(x for x, _ in cs)
    ymin = min(y for _, y in cs)
    ymax = max(y for _, y in cs)
    s = "\n".join(
        "".join("#" if (x, y) in cs else "." for x in range(xmin, xmax + 1))
        for y in range(ymin, ymax + 1)
    )

    print(s)

    return None


def adjacent(coords):

    a = set()
    x, y = coords
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                a.add((x + i, y + j))

    assert len(a) == 8

    return a


def view(coords, dir):

    x, y = coords
    match dir:
        case "N":
            return {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}
        case "S":
            return {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}
        case "W":
            return {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}
        case "E":
            return {(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}
        case _:
            raise ValueError(f"invalid direction: {dir}")


D = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}


def move(elves, order):

    candidates = {}
    for e in elves:
        xs = adjacent(e)
        ex, ey = e
        if all(x not in elves for x in xs):
            continue
        elif all(x not in elves for x in view(e, order[0])):
            dx, dy = D[order[0]]
            candidates[e] = (ex + dx, ey + dy)
        elif all(x not in elves for x in view(e, order[1])):
            dx, dy = D[order[1]]
            candidates[e] = (ex + dx, ey + dy)
        elif all(x not in elves for x in view(e, order[2])):
            dx, dy = D[order[2]]
            candidates[e] = (ex + dx, ey + dy)
        elif all(x not in elves for x in view(e, order[3])):
            dx, dy = D[order[3]]
            candidates[e] = (ex + dx, ey + dy)

    c = Counter(candidates.values())
    pruned = {}
    for k, v in candidates.items():
        if c[v] == 1:
            pruned[k] = v

    new_elves = set()
    for e in elves:
        if e in pruned:
            new_elves.add(pruned[e])
        else:
            new_elves.add(e)

    return new_elves


def compute(input: str) -> int:

    xs = input.splitlines()

    order = ["N", "S", "W", "E"]

    elves = set()
    for j, ys in enumerate(xs):
        for i, y in enumerate(ys):
            if y == "#":
                elves.add((i, j))  # (x, y)

    old_elves = elves.copy()
    i = 0
    while True:
        i += 1
        elves = move(old_elves, order)
        order.append(order.pop(0))

        if old_elves == elves:
            return i

        # print_grid(elves)
        old_elves = elves.copy()


INPUT_S = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
EXPECTED = 20


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
