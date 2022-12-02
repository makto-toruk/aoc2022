from __future__ import annotations

import argparse
from typing import Sequence

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


def main(argv: Sequence[str] | None = None) -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), required=True)

    args = parser.parse_args(argv)
    rounds = [a.split() for a in args.input.read().splitlines()]

    n = 0
    for round in rounds:
        elf = decoder[round[0]]
        you = decoder[round[1]]
        n += compute_outcome(elf, you) + score[you]

    print(n)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
