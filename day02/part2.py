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
}
RESULT_DECODER = {"X": "lose", "Y": "draw", "Z": "win"}
SCORE = {ROCK: 1, PAPER: 2, SCISSORS: 3}


def compute_action(elf: str, result: str) -> int:

    if result == "lose":
        losing_actions = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}
        return losing_actions[elf]
    elif result == "draw":
        return elf
    elif result == "win":
        winning_actions = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}
        return winning_actions[elf]


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


def compute_score(elf: str, result: str) -> int:

    you = compute_action(elf, result)
    return compute_outcome(elf, you) + SCORE[you]


def main(argv: Sequence[str] | None = None) -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), required=True)

    args = parser.parse_args(argv)
    rounds = [a.split() for a in args.input.read().splitlines()]

    score = 0
    for round in rounds:
        score += compute_score(DECODER[round[0]], RESULT_DECODER[round[1]])

    print(score)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
