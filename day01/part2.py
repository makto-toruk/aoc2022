from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


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


def compute(input: str) -> int:
    inventory = input.splitlines()
    inventory.append("")

    elf_sum = 0
    top_three = [0, 0, 0]  # [least, intermediate, highest]
    for item in inventory:
        if item == "":
            top_three = insert(elf_sum, top_three)
            elf_sum = 0
        else:
            elf_sum += int(item)

    return sum(top_three)


INPUT_S = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
EXPECTED = 45000


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
