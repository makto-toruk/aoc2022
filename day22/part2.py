from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def split(path: str) -> list[int | str]:

    paths = []
    acc = []
    numeric = True
    for p in path:
        if p.isnumeric() == numeric:
            acc.append(p)
        else:
            t = "".join(acc)
            if t.isnumeric():
                paths.append(int(t))
            else:
                paths.append(t)
            numeric = not numeric
            acc = [p]

    t = "".join(acc)
    paths.append(int(t))

    return paths


ROTATE = {
    "R": {"R": "D", "L": "U"},
    "L": {"R": "U", "L": "D"},
    "U": {"R": "R", "L": "L"},
    "D": {"R": "L", "L": "R"},
}

FACING = {
    "R": 0,
    "L": 2,
    "U": 3,
    "D": 1,
}


def wrap(pos, direction):

    px, py = pos
    xmax = max(x for x, y in dots | walls if py == y)
    xmin = min(x for x, y in dots | walls if py == y)
    ymax = max(y for x, y in dots | walls if px == x)
    ymin = min(y for x, y in dots | walls if px == x)

    if px == xmax and direction == "R":
        if 1 <= py <= 50:  # B -> D .
            assert xmax == 150
            return 100, 151 - py, "L"
        elif 51 <= py <= 100:  # C -> B .
            assert xmax == 100
            return py + 50, 50, "U"
        elif 101 <= py <= 150:  # D -> B .
            assert xmax == 100
            return 150, 151 - py, "L"
        elif 151 <= py <= 200:  # F -> D .
            assert xmax == 50
            return py - 100, 150, "U"
    elif px == xmin and direction == "L":
        if 1 <= py <= 50:  # A -> E .
            assert xmin == 51
            return 1, 151 - py, "R"
        elif 51 <= py <= 100:  # C -> E .
            assert xmin == 51
            return py - 50, 101, "D"
        elif 101 <= py <= 150:  # E -> A .
            assert xmin == 1
            return 51, 151 - py, "R"
        elif 151 <= py <= 200:  # F -> A .
            assert xmin == 1
            return py - 100, 1, "D"
    elif py == ymin and direction == "U":
        if 1 <= px <= 50:  # E -> C .
            assert ymin == 101
            return 51, px + 50, "R"
        elif 51 <= px <= 100:  # A -> F .
            assert ymin == 1
            return 1, px + 100, "R"
        elif 101 <= px <= 150:  # B -> F .
            assert ymin == 1
            return px - 100, 200, "U"
    elif py == ymax and direction == "D":
        if 1 <= px <= 50:  # F -> B .
            assert ymax == 200
            return px + 100, 1, "D"
        elif 51 <= px <= 100:  # D -> F .
            assert ymax == 150
            return 50, px + 100, "L"
        elif 101 <= px <= 150:  # B -> C .
            assert ymax == 50
            return 100, px - 50, "L"


def step(pos: tuple[int, int], direction: str):

    px, py = pos
    xmax = max(x for x, y in dots | walls if py == y)
    xmin = min(x for x, y in dots | walls if py == y)
    ymax = max(y for x, y in dots | walls if px == x)
    ymin = min(y for x, y in dots | walls if px == x)
    match direction:
        case "R":
            if px == xmax:
                wx, wy, wdir = wrap((px, py), direction)
                if (wx, wy) in walls:
                    return (px, py), direction
                else:
                    return (wx, wy), wdir
            elif (px + 1, py) in dots:
                return (px + 1, py), direction
            elif (px + 1, py) in walls:
                return (px, py), direction
        case "L":
            if px == xmin:
                wx, wy, wdir = wrap((px, py), direction)
                if (wx, wy) in walls:
                    return (px, py), direction
                else:
                    return (wx, wy), wdir
            elif (px - 1, py) in dots:
                return (px - 1, py), direction
            elif (px - 1, py) in walls:
                return (px, py), direction
        case "U":
            if py == ymin:
                wx, wy, wdir = wrap((px, py), direction)
                if (wx, wy) in walls:
                    return (px, py), direction
                else:
                    return (wx, wy), wdir
            elif (px, py - 1) in dots:
                return (px, py - 1), direction
            elif (px, py - 1) in walls:
                return (px, py), direction
        case "D":
            if py == ymax:
                wx, wy, wdir = wrap((px, py), direction)
                if (wx, wy) in walls:
                    return (px, py), direction
                else:
                    return (wx, wy), wdir
            elif (px, py + 1) in dots:
                return (px, py + 1), direction
            elif (px, py + 1) in walls:
                return (px, py), direction


def compute(input: str) -> int:

    xs = input.splitlines()
    n = 0

    global dots
    global walls
    dots = set()
    walls = set()
    found_start = False
    for j, ys in enumerate(xs[:-2]):
        for i, y in enumerate(ys):
            if y == ".":
                if not found_start:
                    start = (i + 1, j + 1)
                    found_start = True
                dots.add((i + 1, j + 1))
            elif y == "#":
                walls.add((i + 1, j + 1))

    paths = split(xs[-1])

    direction = "R"
    distance = paths.pop(0)
    p = start
    for _ in range(distance):
        p, direction = step(p, direction)

    prev = direction
    i = 0
    while paths:
        i += 1

        direction = paths.pop(0)
        distance = paths.pop(0)
        direction = ROTATE[prev][direction]
        for _ in range(distance):
            p, direction = step(p, direction)
        prev = direction

    return 1000 * p[1] + 4 * p[0] + FACING[direction]


INPUT_S = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
EXPECTED = 6032


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
