import Animation
import sys

from typing import List


def main():
    arguments: List = sys.argv
    if len(arguments) != 2:
        raise NameError("Wrong arguments count. Must be 1 argument")

    try:
        file = open(arguments[1], "rt")
    except Exception:
        raise NameError(f"File: {arguments[1]} unavailable.")

    animation: Animation.Animation = Animation.Animation()
    animation.from_stream(file)

    print(animation.to_str())
    print(f"nodes count: {len(animation.nodes)}, steps count: {len(animation.steps)}")


if __name__ == "__main__":
    main()
