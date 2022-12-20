from __future__ import annotations

import argparse
import copy
import os
from dataclasses import dataclass
from functools import cache, cached_property
from multiprocessing import Pool

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

T = 32

GEODE = "geode"
OBSIDIAN = "obsidian"
CLAY = "clay"
ORE = "ore"


@dataclass(unsafe_hash=True)
class Inventory:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def add(self, other: Inventory, b: Blueprint, t: int) -> Inventory:
        """
        Clip to max resources that can be consumed. Helps reduce caching space.
        """
        rmax = b.max_inventory

        return Inventory(
            ore=min(self.ore + other.ore, rmax.ore * (T - t)),
            clay=min(self.clay + other.clay, rmax.clay * (T - t)),
            obsidian=min(
                self.obsidian + other.obsidian, rmax.obsidian * (T - t)
            ),
            geode=self.geode + other.geode,
        )

    def update_robots(self, action: str) -> Inventory:
        new: Inventory = copy.copy(self)
        if action == GEODE:
            new.geode += 1
        elif action == OBSIDIAN:
            new.obsidian += 1
        elif action == CLAY:
            new.clay += 1
        elif action == ORE:
            new.ore += 1
        else:
            raise ValueError(f"Invalidate update: {action}")

        return new

    def update_resources(self, action: str, b: Blueprint) -> Inventory:
        new: Inventory = copy.copy(self)
        if action == GEODE:
            new.ore -= b.geode.ore
            new.obsidian -= b.geode.obsidian
        elif action == OBSIDIAN:
            new.ore -= b.obsidian.ore
            new.clay -= b.obsidian.clay
        elif action == CLAY:
            new.ore -= b.clay.ore
        elif action == ORE:
            new.ore -= b.ore.ore
        else:
            raise ValueError(f"Invalidate update: {action}")

        return new

    def gteqcost(self, cost: Cost) -> bool:
        if (
            self.ore >= cost.ore
            and self.clay >= cost.clay
            and self.obsidian >= cost.obsidian
        ):
            return True

        return False


@dataclass(unsafe_hash=True)
class Cost:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


@dataclass(unsafe_hash=True)
class Blueprint:
    id: int
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost

    @classmethod
    def from_input(cls, x: str) -> Blueprint:
        t = support.ints(x)
        return cls(
            id=t[0],
            ore=Cost(ore=t[1]),
            clay=Cost(ore=t[2]),
            obsidian=Cost(ore=t[3], clay=t[4]),
            geode=Cost(ore=t[5], obsidian=t[6]),
        )

    @cached_property
    def max_inventory(self) -> Inventory:
        """
        Max resource that can be consumed in any minute
        """
        return Inventory(
            ore=max(
                self.ore.ore,
                self.clay.ore,
                self.obsidian.ore,
                self.geode.ore,
            ),
            clay=max(
                self.ore.clay,
                self.clay.clay,
                self.obsidian.clay,
                self.geode.clay,
            ),
            obsidian=max(
                self.ore.obsidian,
                self.clay.obsidian,
                self.obsidian.obsidian,
                self.geode.obsidian,
            ),
        )

    def is_build_possible(
        self, resources: Inventory, robots: Inventory, robot: str
    ) -> bool:
        """
        No point building more robots than max resouces that can be consumed
        at any minute
        """
        rmax = self.max_inventory

        if robot == GEODE:
            if resources.gteqcost(self.geode):
                return True
        elif robot == OBSIDIAN:
            if resources.gteqcost(self.obsidian) and (
                robots.obsidian < rmax.obsidian
            ):
                return True
        elif robot == CLAY:
            if resources.gteqcost(self.clay) and robots.clay < rmax.clay:
                return True
        elif robot == ORE:
            if resources.gteqcost(self.ore) and robots.ore < rmax.ore:
                return True
        else:
            raise ValueError(f"Invalidate robot: {robot}")

        return False


@cache
def geodes(
    b: Blueprint, t: int, resources: Inventory, robots: Inventory
) -> int:

    if t == T:
        return resources.geode + robots.geode

    # geode
    if b.is_build_possible(resources, robots, GEODE):
        new_robots = robots.update_robots(GEODE)
        new_resources = resources.update_resources(GEODE, b)
        new_resources = new_resources.add(robots, b, t)

        return geodes(b, t + 1, new_resources, new_robots)

    max_possible_obsidian = resources.obsidian
    for _t in range(t, T):
        max_possible_obsidian += robots.obsidian + (_t - t)
    if max_possible_obsidian < b.geode.obsidian:
        return resources.geode + robots.geode * (T - (t - 1))

    gs = []
    # nothing
    new_robots: Inventory = copy.copy(robots)
    new_resources = resources.add(robots, b, t)
    gs.append(geodes(b, t + 1, new_resources, new_robots))

    # obsidian
    if b.is_build_possible(resources, robots, OBSIDIAN):
        new_robots = robots.update_robots(OBSIDIAN)
        new_resources = resources.update_resources(OBSIDIAN, b)
        new_resources = new_resources.add(robots, b, t)
        gs.append(geodes(b, t + 1, new_resources, new_robots))

    # clay
    if b.is_build_possible(resources, robots, CLAY):
        new_robots = robots.update_robots(CLAY)
        new_resources = resources.update_resources(CLAY, b)
        new_resources = new_resources.add(robots, b, t)
        gs.append(geodes(b, t + 1, new_resources, new_robots))

    # ore
    if b.is_build_possible(resources, robots, ORE):
        new_robots = robots.update_robots(ORE)
        new_resources = resources.update_resources(ORE, b)
        new_resources = new_resources.add(robots, b, t)
        gs.append(geodes(b, t + 1, new_resources, new_robots))

    return max(gs)


def compute(input: str) -> int:

    xs = input.splitlines()
    bs = []
    for x in xs:
        b = Blueprint.from_input(x)
        resources = Inventory()
        robots = Inventory(ore=1)
        t = 1
        bs.append((b, t, resources, robots))

    with Pool(processes=8) as pool:
        gs = []
        for b in bs[:3]:
            print(b)
            gs.append(pool.apply_async(geodes, b))

        n = 1
        for i, g in enumerate(gs):
            print(f"blueprint: {i}, display quality: {g.get()}")
            n *= g.get()

    return n


INPUT_S = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
EXPECTED = 62 * 56


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
