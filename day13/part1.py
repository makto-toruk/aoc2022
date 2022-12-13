from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def is_lower(l: list | int, r: list | int) -> int:

    if isinstance(l, int) and isinstance(r, int):
        if l > r:
            return -1
        elif l == r:
            return 0
        else:
            return 1

    if isinstance(l, int):
        l = [l]

    if isinstance(r, int):
        r = [r]

    l1 = l.copy()
    r1 = r.copy()
    while l1 and r1:
        x = l1.pop(0)
        y = r1.pop(0)
        z = is_lower(x, y)

        if z != 0:
            return z

    if len(l1) > len(r1):
        return -1
    elif len(r1) > len(l1):
        return 1

    return 0


def compute(input: str) -> int:

    xs = input.splitlines()

    n = 0
    for i in range(0, len(xs), 3):
        l = eval(xs[i])
        r = eval(xs[i + 1])

        if is_lower(l, r) == 1:
            n += i // 3 + 1

    return n


INPUT_S = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
EXPECTED = 13


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
