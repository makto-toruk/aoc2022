from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def operation(a, operator, b):

    if operator == "+":
        return a + b
    elif operator == "*":
        return a * b
    elif operator == "square":
        return a * a


def compute(input: str) -> int:

    xs = input.splitlines()

    items = []
    operations = []
    tests = []
    for x in xs:
        if x.startswith("Monkey"):
            i = int(x.split()[1][0])
        elif x.startswith("  Starting items: "):
            t = x.replace("  Starting items: ", "")
            items.append([int(j) for j in t.split(",")])
        elif x.startswith("  Operation"):
            t = x.split()[-2:]
            if t[1] == "old":
                operations.append(["square", 0])
            else:
                operations.append([t[0], int(t[1])])
        elif x.startswith("  Test:"):
            tests.append({"divisible": int(x.split()[-1])})
        elif x.startswith("    If true: "):
            tests[i]["true"] = int(x.split()[-1])
        elif x.startswith("    If false: "):
            tests[i]["false"] = int(x.split()[-1])

    n_rounds = 10000
    divisors = 1
    for t in tests:
        divisors *= t["divisible"]

    inspections = [0] * len(items)
    for r in range(n_rounds):
        for i, ys in enumerate(items):
            inspections[i] += len(ys)
            ys = [
                operation(y, operations[i][0], operations[i][1]) % divisors
                for y in ys
            ]
            items[tests[i]["true"]] += [
                y for y in ys if y % tests[i]["divisible"] == 0
            ]
            items[tests[i]["false"]] += [
                y for y in ys if y % tests[i]["divisible"] != 0
            ]
            items[i] = []

    s = sorted(inspections)

    return s[-1] * s[-2]


INPUT_S = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED = 2713310158


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
