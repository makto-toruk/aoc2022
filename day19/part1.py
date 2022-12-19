from __future__ import annotations

import argparse
import copy
import os
from dataclasses import dataclass
from functools import cache
from multiprocessing import Pool

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

T = 24


@dataclass(unsafe_hash=True)
class Inventory:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


@dataclass(unsafe_hash=True)
class Cost:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


@dataclass(unsafe_hash=True)
class Blueprint:
    id: int
    ore_robot: Cost
    clay_robot: Cost
    obsidian_robot: Cost
    geode_robot: Cost


@cache
def geodes(
    b: Blueprint, t: int, resources: Inventory, robots: Inventory
) -> int:

    if t == T:
        return resources.geode + robots.geode

    max_ore = max(
        b.ore_robot.ore,
        b.clay_robot.ore,
        b.obsidian_robot.ore,
        b.geode_robot.ore,
    )
    max_clay = max(
        b.ore_robot.clay,
        b.clay_robot.clay,
        b.obsidian_robot.clay,
        b.geode_robot.clay,
    )
    max_obsidian = max(
        b.ore_robot.obsidian,
        b.clay_robot.obsidian,
        b.obsidian_robot.obsidian,
        b.geode_robot.obsidian,
    )

    # geode
    if (
        resources.ore >= b.geode_robot.ore
        and resources.obsidian >= b.geode_robot.obsidian
    ):
        new_robots: Inventory = copy.copy(robots)
        new_resources: Inventory = copy.copy(resources)
        new_robots.geode += 1
        new_resources.ore -= b.geode_robot.ore
        new_resources.obsidian -= b.geode_robot.obsidian

        new_resources.ore = min(
            new_resources.ore + robots.ore, (T - t) * max_ore
        )
        new_resources.clay = min(
            new_resources.clay + robots.clay, (T - t) * max_clay
        )
        new_resources.obsidian = min(
            new_resources.obsidian + robots.obsidian, (T - t) * max_obsidian
        )
        new_resources.geode += robots.geode

        return geodes(b, t + 1, new_resources, new_robots)

    max_possible_obsidian = resources.obsidian
    for _t in range(t, T):
        max_possible_obsidian += robots.obsidian + (_t - t)
    if max_possible_obsidian < b.geode_robot.obsidian:
        return robots.geode * (T - (t - 1))

    gs = []
    # nothing
    new_robots: Inventory = copy.copy(robots)
    new_resources: Inventory = copy.copy(resources)

    new_resources.ore = min(new_resources.ore + robots.ore, (T - t) * max_ore)
    new_resources.clay = min(
        new_resources.clay + robots.clay, (T - t) * max_clay
    )
    new_resources.obsidian = min(
        new_resources.obsidian + robots.obsidian, (T - t) * max_obsidian
    )
    new_resources.geode += robots.geode

    gs.append(geodes(b, t + 1, new_resources, new_robots))

    # clay
    if robots.clay < max_clay and resources.ore >= b.clay_robot.ore:
        new_robots: Inventory = copy.copy(robots)
        new_resources: Inventory = copy.copy(resources)
        new_robots.clay += 1
        new_resources.ore -= b.clay_robot.ore

        new_resources.ore = min(
            new_resources.ore + robots.ore, (T - t) * max_ore
        )
        new_resources.clay = min(
            new_resources.clay + robots.clay, (T - t) * max_clay
        )
        new_resources.obsidian = min(
            new_resources.obsidian + robots.obsidian, (T - t) * max_obsidian
        )
        new_resources.geode += robots.geode

        gs.append(geodes(b, t + 1, new_resources, new_robots))

    # ore
    if robots.ore < max_ore and resources.ore >= b.ore_robot.ore:
        new_robots: Inventory = copy.copy(robots)
        new_resources: Inventory = copy.copy(resources)
        new_robots.ore += 1
        new_resources.ore -= b.ore_robot.ore

        new_resources.ore = min(
            new_resources.ore + robots.ore, (T - t) * max_ore
        )
        new_resources.clay = min(
            new_resources.clay + robots.clay, (T - t) * max_clay
        )
        new_resources.obsidian = min(
            new_resources.obsidian + robots.obsidian, (T - t) * max_obsidian
        )
        new_resources.geode += robots.geode

        gs.append(geodes(b, t + 1, new_resources, new_robots))

    if robots.obsidian < max_obsidian and (
        resources.ore >= b.obsidian_robot.ore
        and resources.clay >= b.obsidian_robot.clay
    ):
        new_robots: Inventory = copy.copy(robots)
        new_resources: Inventory = copy.copy(resources)
        new_robots.obsidian += 1
        new_resources.ore -= b.obsidian_robot.ore
        new_resources.clay -= b.obsidian_robot.clay

        new_resources.ore = min(
            new_resources.ore + robots.ore, (T - t) * max_ore
        )
        new_resources.clay = min(
            new_resources.clay + robots.clay, (T - t) * max_clay
        )
        new_resources.obsidian = min(
            new_resources.obsidian + robots.obsidian, (T - t) * max_obsidian
        )
        new_resources.geode += robots.geode

        gs.append(geodes(b, t + 1, new_resources, new_robots))

    return max(gs)


def compute(input: str) -> int:

    xs = input.splitlines()
    bs = []
    for x in xs:
        t = support.ints(x)
        b = Blueprint(
            id=t[0],
            ore_robot=Cost(ore=t[1]),
            clay_robot=Cost(ore=t[2]),
            obsidian_robot=Cost(ore=t[3], clay=t[4]),
            geode_robot=Cost(ore=t[5], obsidian=t[6]),
        )
        resources = Inventory()
        robots = Inventory(ore=1)
        t = 1
        bs.append((b, t, resources, robots))

    with Pool(processes=8) as pool:
        gs = []
        for b in bs:
            print(b)
            gs.append(pool.apply_async(geodes, b))

        n = 0
        for i, g in enumerate(gs):
            print(f"blueprint: {i}, display quality: {g.get()}")
            n += (i + 1) * g.get()

    return n


INPUT_S = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
EXPECTED = 33


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
