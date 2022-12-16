from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from functools import cache

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Valve:
    i: int
    rate: int
    connects: list[str]


# easier than storing a DP dict (and seems much faster)
@cache
def DP(curr: str, t: int, opened: tuple[int]):

    if t == 0:
        return 0

    pressure = 0
    # move
    move = []
    for node in valves[curr].connects:
        move.append(DP(node, t - 1, opened))
    move = max(move)

    # open
    open = 0
    if not opened[valves[curr].i] and valves[curr].rate > 0:
        new_opened = list(opened)
        new_opened[valves[curr].i] = 1
        open = (t - 1) * valves[curr].rate + DP(
            curr, t - 1, tuple(new_opened)
        )

    pressure += max(open, move)

    return pressure


def parse(x):
    name = x.split()[1]
    rate = support.ints(x)[0]
    connects = (
        x.split("; ")[1]
        .replace("tunnels lead to valves ", "")
        .replace("tunnel leads to valve ", "")
        .split(", ")
    )

    return name, rate, connects


def compute(input: str) -> int:

    xs = input.splitlines()

    global valves
    valves = {}
    for i, x in enumerate(xs):
        name, rate, connects = parse(x)
        valves[name] = Valve(i=i, rate=rate, connects=connects)

    curr = "AA"
    t = 30
    opened = tuple([0] * len(valves))
    max_pressure = DP(curr, t, opened)

    return max_pressure


INPUT_S = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
EXPECTED = 1651


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
