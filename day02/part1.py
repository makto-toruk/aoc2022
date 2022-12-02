from __future__ import annotations

import argparse
from typing import Sequence

ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"
DECODER = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}
SCORE = {ROCK: 1, PAPER: 2, SCISSORS: 3}


def compute_outcome(elf: str, you: str) -> int:

    if elf == you:
        return 3
    elif (
        (elf == ROCK and you == SCISSORS)
        or (elf == PAPER and you == ROCK)
        or (elf == SCISSORS and you == PAPER)
    ):
        return 0
    else:
        return 6


def compute_score(elf: str, you: str) -> int:

    return compute_outcome(elf, you) + SCORE[you]


def main(argv: Sequence[str] | None = None) -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), required=True)

    args = parser.parse_args(argv)
    rounds = [a.split() for a in args.input.read().splitlines()]

    score = 0
    for round in rounds:
        score += compute_score(DECODER[round[0]], DECODER[round[1]])

    print(score)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
