from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

DP = {}


@dataclass
class Valve:
    i: int
    rate: int
    connects: list[str]
    # open: bool = False


def step(curr: str, t: int, valves: dict[str, Valve], opened: tuple[int]):

    if t == 30:
        return 0

    if (curr, t, opened) in DP:
        return DP[(curr, t, opened)]

    pressure = 0
    for v in valves.values():
        if opened[v.i]:
            pressure += v.rate

    # move
    move = []
    for node in valves[curr].connects:
        move.append(step(node, t + 1, valves, opened))
    move = max(move)

    # open
    open = 0
    if not opened[valves[curr].i] and valves[curr].rate > 0:
        new_opened = list(opened)
        new_opened[valves[curr].i] = 1
        open = step(curr, t + 1, valves, tuple(new_opened))

    pressure += max(open, move)
    DP[(curr, t, opened)] = pressure

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

    # input = INPUT_S
    xs = input.splitlines()

    valves = {}
    for i, x in enumerate(xs):
        name, rate, connects = parse(x)
        valves[name] = Valve(i=i, rate=rate, connects=connects)

    print(valves)

    curr = "AA"
    t = 0
    opened = tuple([0] * len(valves))
    max_pressure = step(curr, t, valves, opened)

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
