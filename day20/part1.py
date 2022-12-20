from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:

    xs = [(i, int(x)) for i, x in enumerate(input.splitlines())]
    ys = xs.copy()
    l = len(xs)
    for i, x in xs:
        print(i)
        p = ys.index((i, x))
        n = x % (l - 1)  # moving backwards has an equivalent
        ys.pop(p)
        # l - 1 moved right will land in index 1
        # l - 2 moved right will land in index 0

        if x == 0:
            zero = (i, x)

    p = ys.index(zero)

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
EXPECTED = 3


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
