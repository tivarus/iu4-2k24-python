import argparse
import os

from task02.scripts.find_tree import creating_list_from_directories_and_files


def print_tree(start_path: str, max_level: int, ready: list):
    ans, number_of_directories, number_of_files = creating_list_from_directories_and_files(start_path, max_level, ready)
    for f in ans:
        print(f)
    print(f"{number_of_directories} directories, {number_of_files} files")


def main():
    parser = argparse.ArgumentParser(description='parse flags')
    parser.add_argument('-d', '--dir', default=os.getcwd(), type=str, help='starting directory')
    parser.add_argument('-n', '--nest', default=1000, type=int, help='nesting')
    args = parser.parse_args()
    ready = []

    print_tree(args.dir, args.nest, ready)


if __name__ == '__main__':
    main()
