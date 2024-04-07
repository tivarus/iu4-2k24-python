from tree import tree
from argparse import ArgumentParser


def parse_arg():
    parser = ArgumentParser(description="Build tree of filesystem")

    parser.add_argument("path", type=str, help="start directory")
    parser.add_argument("-d", "--depth", dest="depth", default=None, type=int,
                        help="tree display depth [default: %(default)s]")
    return parser.parse_args()


def main():
    arg = parse_arg()
    tree.run(arg.path, arg.depth)


if __name__ == "__main__":
    main()
