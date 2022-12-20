from __future__ import annotations

import argparse
import os

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
KEY = 811589153


def find(e: tuple[int, int], ys: list[tuple[int, int]]):
    for i, y in enumerate(ys):
        if y == e:
            return i


def move(
    e: tuple[int, int], ys: list[tuple[int, int]], d: str, p: int
) -> list[tuple[int, int]]:

    # p = find(e, ys)
    l = len(ys)
    zs = [None] * l

    if d == ">":
        if 0 <= p < l - 2:
            zs[:p] = ys[:p]
            zs[p] = ys[p + 1]
            zs[p + 1] = ys[p]
            zs[p + 2 :] = ys[p + 2 :]
        elif p == l - 2:
            zs[0] = ys[l - 2]
            zs[l - 1] = ys[l - 1]
            zs[1 : l - 1] = ys[0 : l - 2]
        elif p == l - 1:
            zs[0] = ys[0]
            zs[1] = ys[l - 1]
            zs[2:] = ys[1 : l - 1]

    elif d == "<":
        if 1 < p <= l - 1:
            zs[p + 1 :] = ys[p + 1 :]
            zs[p] = ys[p - 1]
            zs[p - 1] = ys[p]
            zs[: p - 1] = ys[: p - 1]
        elif p == 1:
            zs[l - 1] = ys[1]
            zs[0] = ys[0]
            zs[1 : l - 1] = ys[2:]
        elif p == 0:
            zs[l - 1] = ys[l - 1]
            zs[l - 2] = ys[0]
            zs[: l - 2] = ys[1 : l - 1]

    return zs


def update(p: int, l: int, d: str):

    if d == ">":
        if 0 <= p < l - 2:
            return p + 1
        elif p == l - 2:
            return 0
        elif p == l - 1:
            return 1

    elif d == "<":
        if 1 < p <= l - 1:
            return p - 1
        elif p == 1:
            return l - 1
        elif p == 0:
            return l - 2


def compute(input: str) -> int:

    xs = [(i, int(x) * KEY) for i, x in enumerate(input.splitlines())]
    ys = xs.copy()
    l = len(xs)
    for _ in range(10):
        for i, x in xs:
            print(i)
            p = find((i, x), ys)
            n = x % (l - 1)
            for _ in range(n):
                ys = move((i, x), ys, ">", p)
                p = update(p, l, ">")

            # print(i)
            # print([y for _, y in ys])

            if x == 0:
                zero = (i, x)

    p = find(zero, ys)

    return ys[(p + 1000) % l][1] + ys[(p + 2000) % l][1] + ys[(p + 3000) % l][1]


INPUT_S = """\
1
2
-3
3
-2
0
4
"""
EXPECTED = 1623178306


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
