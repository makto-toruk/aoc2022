from __future__ import annotations

import argparse
from typing import Sequence


def insert(item: int, top_three: list[int]) -> list[int]:
    """
    TODO: ideally, I should be using a queue here.
    """

    if item <= top_three[0]:
        top_three = [item] + top_three
    elif item >= top_three[2]:
        top_three = top_three + [item]
    elif item >= top_three[1]:
        top_three = top_three[:2] + [item, top_three[2]]
    elif item > top_three[0]:
        top_three = [top_three[0], item] + top_three[1:]

    return top_three[1:]


def main(argv: Sequence[str] | None = None) -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), required=True)

    args = parser.parse_args(argv)
    inventory = args.input.read().splitlines()
    inventory.append("")

    budget = []
    elf_sum = 0
    top_three = [0, 0, 0]  # [least, intermediate, highest]
    for item in inventory:
        if item == "":
            budget.append(elf_sum)
            top_three = insert(elf_sum, top_three)
            elf_sum = 0
        else:
            elf_sum += int(item)

    print(sum(top_three))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
