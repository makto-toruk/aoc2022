from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> str:

    xs = input.splitlines()

    blocks = []
    instructions = []
    for x in xs:
        if x.startswith("move"):
            instructions.append(x.split(" "))
        elif x.startswith(" 1"):
            grid = [int(i) for i in x.strip().split() if i != ""]
        else:
            blocks.append(x)

    n_stacks = max(grid)
    stacks = [[] for k in range(n_stacks)]
    for block in blocks[::-1]:
        for i, s in enumerate(block):
            if (i - 1) % 4 == 0 and s != " ":
                c = (i - 1) // 4
                stacks[c].append(s)

    for i in instructions:
        n_pops = int(i[1])
        f = stacks[int(i[3]) - 1]
        t = stacks[int(i[5]) - 1]
        gather = []
        for _ in range(n_pops):
            gather.append(f.pop())
        t += gather[::-1]

    n = ""
    for s in stacks:
        n += s.pop()

    return n


INPUT_S = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "MCD"


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: str) -> None:
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
