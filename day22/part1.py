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


def move(pos: tuple[int, int], direction: str, distance: int):

    px, py = pos
    xmax = max(x for x, y in dots | walls if py == y)
    xmin = min(x for x, y in dots | walls if py == y)
    ymax = max(y for x, y in dots | walls if px == x)
    ymin = min(y for x, y in dots | walls if px == x)
    match direction:
        case "R":
            for _ in range(distance):
                if px == xmax:
                    if (xmin, py) in walls:
                        break
                    else:
                        px = xmin
                elif (px + 1, py) in dots:
                    px = px + 1
                elif (px + 1, py) in walls:
                    break
        case "L":
            for _ in range(distance):
                if px == xmin:
                    if (xmax, py) in walls:
                        break
                    else:
                        px = xmax
                elif (px - 1, py) in dots:
                    px = px - 1
                elif (px - 1, py) in walls:
                    break
        case "U":
            for _ in range(distance):
                if py == ymin:
                    if (px, ymax) in walls:
                        break
                    else:
                        py = ymax
                elif (px, py - 1) in dots:
                    py = py - 1
                elif (px, py - 1) in walls:
                    break
        case "D":
            for _ in range(distance):
                if py == ymax:
                    if (px, ymin) in walls:
                        break
                    else:
                        py = ymin
                elif (px, py + 1) in dots:
                    py = py + 1
                elif (px, py + 1) in walls:
                    break

    return (px, py)


def compute(input: str) -> int:

    xs = input.splitlines()

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
    p = move(start, direction, distance)

    prev = direction
    while paths:
        direction = paths.pop(0)
        distance = paths.pop(0)
        direction = ROTATE[prev][direction]
        p = move(p, direction, distance)
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
