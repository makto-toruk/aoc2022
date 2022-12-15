from __future__ import annotations

import argparse
import os
import re

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def lmap(func, *iterables):
    return list(map(func, *iterables))


def ints(s):
    return lmap(int, re.findall(r"-?\d+", s))


def dist(a, b):

    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def get_coverage_y(s, b, y):

    d = dist(s, b)

    sx, sy = s
    dy = abs(sy - y)

    covered = set()
    for dx in range(-d + dy, d - dy + 1):
        assert dist(s, (sx + dx, y)) <= d
        covered.add((sx + dx, y))

    return covered


def compute(input: str, y: int) -> int:

    xs = input.splitlines()

    sensors = []
    beacons = []
    for x in xs:
        t = ints(x)
        sensors.append((t[0], t[1]))
        beacons.append((t[2], t[3]))

    covered = set()
    for s, b in zip(sensors, beacons):
        for c in get_coverage_y(s, b, y):
            covered.add(c)

    for b in beacons:
        if b in covered:
            covered.remove(b)

    return len(covered)


INPUT_S = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
EXPECTED = 26


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 10) == expected


def main() -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.input) as f:
        print(compute(f.read(), 2_000_000))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
