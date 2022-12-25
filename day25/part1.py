from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

numerals = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
encoders = {v: k for k, v in numerals.items()}


def decode(xs):

    k = len(xs)
    n = 0
    for i, x in enumerate(xs):
        n += numerals[x] * (5 ** (k - 1 - i))

    return n


def encode(n):

    s = ""
    ls = {}
    i = 0
    while n > 0:
        t = n % 5
        ls[i] = t
        n = n // 5
        i += 1

    digits = max(ls.keys())

    for i in range(digits):
        l = ls[i]
        if l <= 2:
            continue
        else:
            ls[i] = l - 5
            if (i + 1) in ls:
                ls[i + 1] += 1
            else:
                ls[i + 1] = 1

    ps = [0] * (max(ls.keys()) + 1)
    for i, l in ls.items():
        ps[i] = l

    for p in ps:
        s = encoders[p] + s

    return s


def compute(input: str) -> str:

    xs = input.splitlines()

    n = 0
    for x in xs:
        n += decode(x)

    assert decode("2=") == 8
    assert decode("20") == 10
    assert decode("2=-01") == 976
    assert decode("1121-1110-1=0") == 314159265

    return encode(n)


INPUT_S = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""
EXPECTED = "2=-1=0"


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
