from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

decoder = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}
score = {"R": 1, "P": 2, "S": 3}
lose = {"R": "S", "P": "R", "S": "P"}


def compute_outcome(elf: str, you: str) -> int:

    if elf == you:
        return 3
    elif you == lose[elf]:
        return 0
    else:
        return 6


def compute(input: str) -> int:

    rounds = [a.split() for a in input.splitlines()]

    n = 0
    for round in rounds:
        elf = decoder[round[0]]
        you = decoder[round[1]]
        n += compute_outcome(elf, you) + score[you]

    return n


INPUT_S = """\
A Y
B X
C Z
"""
EXPECTED = 15


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
