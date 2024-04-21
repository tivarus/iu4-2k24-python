import os
from enum import Enum
from colorama import Fore, Style
import sys

class Symbol(Enum):
    TAB: str = '    '
    OUTER: str = '│   '
    INNER: str = '├── '
    LAST: str = '└── '


class Dir:
    name: str
    subdirs: list[str]
    lvl: int
    self_last: bool
    is_base: bool

    def __init__(self):
        self.next = None  # for tracking parent dirs
        self.subdirs = []
        self.name = ''
        self.lvl = 0
        self.self_last = False


def dir_is_last(dir_it: str, dir_list: list[str]) -> bool:
    if dir_list[-1] == dir_it:
        return True
    else:
        return False


def get_subdirs(parent_dir: Dir, depth: int) -> list[Dir]:
    dirs_this_lvl: list[Dir] = []

    if os.path.isdir(parent_dir.name):
        dir_content = os.listdir(parent_dir.name)
        for d in dir_content:
            full_path = f'{parent_dir.name}\\{d}'
            parent_dir.subdirs.append(full_path)
    else:
        parent_dir.subdirs = []

    if len(parent_dir.subdirs) != 0:
        for dir_it in parent_dir.subdirs:
            subdir: Dir = Dir()
            subdir.name = dir_it
            subdir.lvl = parent_dir.lvl - 1
            subdir.self_last = dir_is_last(dir_it, parent_dir.subdirs)
            subdir.is_base = False
            if subdir.lvl != depth:  # because we don't need and indent for 0 lvl
                subdir.next = parent_dir

            dirs_this_lvl.append(subdir)

            if subdir.lvl == 0:
                if subdir.self_last:
                    return dirs_this_lvl
            else:
                dirs_this_lvl.extend(get_subdirs(subdir, depth))

    return dirs_this_lvl


def get_tree(base_dir_name: str, depth: int) -> list[Dir]:
    base_dir = Dir()
    base_dir.name = base_dir_name
    base_dir.lvl = depth + 1
    base_dir.self_last = False
    base_dir.is_base = True

    tree: list[Dir] = [base_dir]
    tree.extend(get_subdirs(base_dir, depth))

    return tree


def get_output_color(path: str) -> str:
    if os.path.isdir(path):
        return Fore.BLUE
    elif os.path.isfile(path):
        return Fore.GREEN
    else:
        return Fore.RED


def print_tree(tree: list[Dir]) -> None:
    for dir_it in tree:
        line: str = os.path.basename(dir_it.name)
        line = f'{get_output_color(dir_it.name)}{line}'
        if not dir_it.is_base:
            if dir_it.self_last:
                line = f'{Symbol.LAST.value}{line}'
            else:
                line = f'{Symbol.INNER.value}{line}'

            parent_dir = dir_it.next
            while parent_dir:
                if parent_dir.self_last:
                    line = f'{Symbol.TAB.value}{line}'
                else:
                    line = f'{Symbol.OUTER.value}{line}'
                parent_dir = parent_dir.next
        print(f'{line}{Style.RESET_ALL}')


def main():
    depth = int(sys.argv[1])
    base_folder = f'{os.getcwd()}{sys.argv[2]}'
    my_tree = get_tree(base_folder, depth)
    print_tree(my_tree)


if __name__ == "__main__":
    main()