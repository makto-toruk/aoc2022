from __future__ import annotations

import argparse
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int | None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType("r"), required=True)

    args = parser.parse_args(argv)
    inventory = args.input.read().splitlines()
    inventory.append("")

    elf_sum = 0
    max_calories = 0
    for item in inventory:
        if item == "":
            if elf_sum > max_calories:
                max_calories = elf_sum
            elf_sum = 0
        else:
            elf_sum += int(item)

    print(max_calories)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
