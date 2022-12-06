from __future__ import annotations

import argparse
import os

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:

    xs = input.splitlines()[0]

    l = []
    n = 0
    for x in xs:
        l = l[-3:] + [x]
        n += 1
        if len(set(l)) == 4:
            return n


INPUT_1 = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""
EXPECTED_1 = 7
INPUT_2 = """\
bvwbjplbgvbhsrlpgdmjqwftvncz
"""
EXPECTED_2 = 5
INPUT_3 = """\
nppdvjthqldpwncqszvftbrmjlhg
"""
EXPECTED_3 = 6
INPUT_4 = """\
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
"""
EXPECTED_4 = 10
INPUT_5 = """\
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""
EXPECTED_5 = 11


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_1, EXPECTED_1),
        (INPUT_2, EXPECTED_2),
        (INPUT_3, EXPECTED_3),
        (INPUT_4, EXPECTED_4),
        (INPUT_5, EXPECTED_5),
    ),
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
