from __future__ import annotations

import argparse
from typing import Sequence


def priority(s: str) -> int:

    if s.islower():
        return ord(s) - 96
    else:
        return ord(s) - 64 + 26


def main(argv: Sequence[str] | None = None) -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), required=True)

    args = parser.parse_args(argv)
    rucksacks = args.input.read().splitlines()

    n = 0
    for r in rucksacks:
        l = len(r)
        left = r[: l // 2]
        right = r[l // 2 :]
        n += priority(list(set(left).intersection(set(right)))[0])

    print(n)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
