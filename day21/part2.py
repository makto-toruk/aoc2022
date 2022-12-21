from __future__ import annotations

import argparse
import os

import pytest
import sympy as sp

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def decode(expr: list[str] | int) -> int | bool:

    if isinstance(expr, (int, sp.Symbol)):
        return expr
    else:
        l, op, r = expr
        return sp.parse_expr(f"(({decode(d[l])}) {op} ({decode(d[r])}))")


def compute(input: str) -> int:

    xs = input.splitlines()

    global d
    d = {}
    for x in xs:
        l, r = x.split(": ")
        rs = r.split()
        if l == "humn":
            d[l] = y = sp.Symbol("y")
        elif len(rs) > 1:
            if l == "root":
                d[l] = [rs[0], "==", rs[2]]
            else:
                d[l] = rs
        else:
            d[l] = int(r)

    l, _, r = d["root"]

    return sp.solve(decode(d[l]) - decode(d[r]), y)[0]


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
EXPECTED = 301


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
