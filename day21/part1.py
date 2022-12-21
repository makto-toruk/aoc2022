from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def decode(expr: list[str] | int) -> int:

    if isinstance(expr, int):
        return expr
    else:
        l, op, r = expr
        return eval(f"{decode(d[l])} {op} {decode(d[r])}")


def compute(input: str) -> int:

    xs = input.splitlines()
    n = 0

    global d
    d = {}
    for x in xs:
        l, r = x.split(": ")
        if len(r.split()) > 1:
            d[l] = r.split()
        else:
            d[l] = int(r)

    return int(decode(d["root"]))


INPUT_S = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
EXPECTED = 152


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
