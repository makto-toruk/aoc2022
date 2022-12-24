from __future__ import annotations

import argparse
import os
from collections import deque
from functools import cache
from math import lcm

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


BLIZZARDS = []


def print_blizzards(blizzards) -> None:

    xmin = 0
    ymin = 0

    def out(pos):
        n = 0
        for b in blizzards.values():
            if pos in b:
                n += 1

        if n > 1:
            return str(n)
        else:
            if pos in blizzards["r"]:
                return ">"
            elif pos in blizzards["l"]:
                return "<"
            elif pos in blizzards["u"]:
                return "^"
            elif pos in blizzards["d"]:
                return "v"

        px, py = pos
        if px == 0 or px == xmax or py == 0 or py == ymax:
            return "#"
        return "."

    s = "\n".join(
        "".join(out((x, y)) for x in range(xmin, xmax + 1))
        for y in range(ymin, ymax + 1)
    )

    print(s)

    return None


def adjacent(pos):
    px, py = pos

    a = set()
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
        a.add((px + dx, py + dy))

    return a


def update(blizzards):

    new = {"r": set(), "l": set(), "u": set(), "d": set()}
    for x, y in blizzards["r"]:
        if x + 1 == xmax:
            new["r"].add((1, y))
        else:
            new["r"].add((x + 1, y))
    for x, y in blizzards["l"]:
        if x - 1 == 0:
            new["l"].add((xmax - 1, y))
        else:
            new["l"].add((x - 1, y))
    for x, y in blizzards["u"]:
        if y - 1 == 0:
            new["u"].add((x, ymax - 1))
        else:
            new["u"].add((x, y - 1))
    for x, y in blizzards["d"]:
        if y + 1 == ymax:
            new["d"].add((x, 1))
        else:
            new["d"].add((x, y + 1))

    return new


def bfs(t, start, goal):

    queue = deque([(start, t)])
    PREV = set()
    PREV.add((start, (t % period)))

    while queue:
        pos, t = queue.popleft()
        bs = BLIZZARDS[(t + 1) % period]
        ps = adjacent(pos)
        for p in ps:
            if p == goal:
                return t + 1
            if any(p in b for b in bs.values()):
                continue
            px, py = p
            if not ((1 <= px < xmax) and (1 <= py < ymax)) and p != start:
                continue
            if (p, (t + 1) % period) in PREV:
                continue
            else:
                PREV.add((p, (t + 1) % period))
                queue.append((p, t + 1))

    raise Exception("no path found")


def compute(input: str) -> int:

    xs = input.splitlines()

    ws = set()
    blizzards = {"r": set(), "l": set(), "u": set(), "d": set()}
    for j, ys in enumerate(xs):
        for i, y in enumerate(ys):
            match y:
                case "#":
                    ws.add((i, j))
                case ">":
                    blizzards["r"].add((i, j))
                case "<":
                    blizzards["l"].add((i, j))
                case "^":
                    blizzards["u"].add((i, j))
                case "v":
                    blizzards["d"].add((i, j))
                case _:
                    assert y == "."

    global xmax
    global ymax
    xmax = max(x for x, _ in ws)
    ymax = max(y for _, y in ws)

    # periodic blizzards
    global period
    period = lcm(xmax - 1, ymax - 1)
    temp = blizzards.copy()
    for _ in range(period):
        BLIZZARDS.append(temp)
        temp = update(temp)
        # print_blizzards(blizzards)

    assert blizzards == temp

    finish = (xmax - 1, ymax)
    start = (1, 0)

    t0 = bfs(0, start, finish)
    print(t0)
    t1 = bfs(t0, finish, start)
    print(t1)
    return bfs(t1, start, finish)


INPUT_S = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
EXPECTED = 54


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
