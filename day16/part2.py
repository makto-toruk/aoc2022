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


def step(
    player1: str,
    player2: str,
    t: int,
    valves: dict[str, Valve],
    opened: tuple[int],
):

    if t == 26:
        return 0

    player1, player2 = min(player1, player2), max(player1, player2)

    if (player1, player2, t, opened) in DP:
        return DP[(player1, player2, t, opened)]

    pressure = 0
    for v in valves.values():
        if opened[v.i]:
            pressure += v.rate

    if all(opened[v.i] for v in valves.values() if v.rate > 0):
        pressure += step(player1, player2, t + 1, valves, opened)

    else:
        # move, move
        move_move = []
        for node_1 in valves[player1].connects:
            for node_2 in valves[player2].connects:
                move_move.append(step(node_1, node_2, t + 1, valves, opened))

        move_move = max(move_move)

        # move, open
        move_open = 0
        for node_1 in valves[player1].connects:
            if not opened[valves[player2].i] and valves[player2].rate > 0:
                new_opened = list(opened)
                new_opened[valves[player2].i] = 1
                move_open = max(
                    move_open,
                    step(node_1, player2, t + 1, valves, tuple(new_opened)),
                )

        # open, move
        open_move = 0
        for node_2 in valves[player2].connects:
            if not opened[valves[player1].i] and valves[player1].rate > 0:
                new_opened = list(opened)
                new_opened[valves[player1].i] = 1
                open_move = max(
                    open_move,
                    step(player1, node_2, t + 1, valves, tuple(new_opened)),
                )

        # open, open
        open = 0
        if not opened[valves[player1].i] and valves[player1].rate > 0:
            if not opened[valves[player2].i] and valves[player2].rate > 0:
                new_opened = list(opened)
                new_opened[valves[player1].i] = 1
                new_opened[valves[player2].i] = 1
                open = step(player1, player2, t + 1, valves, tuple(new_opened))

        pressure += max(move_move, move_open, open_move, open)

    DP[(player1, player2, t, opened)] = pressure

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

    valves = {}
    for i, x in enumerate(xs):
        name, rate, connects = parse(x)
        valves[name] = Valve(i=i, rate=rate, connects=connects)

    print(valves)

    t = 0
    opened = tuple([0] * len(valves))
    max_pressure = step("AA", "AA", t, valves, opened)

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
EXPECTED = 1707


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
