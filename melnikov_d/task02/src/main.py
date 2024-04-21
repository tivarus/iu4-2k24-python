import sys
from tree import print_tree


def main():
    if len(sys.argv) != 3:
        print("invalid count args")
        sys.exit(1)
    depth = int(sys.argv[1])
    path = sys.argv[2]
    print_tree(path, depth)


if __name__ == '__main__':
    main()
