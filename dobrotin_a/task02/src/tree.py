import os
from enum import Enum
from colorama import Fore, Style
import sys
from typing import Self
from dataclasses import dataclass, field


@dataclass
class Symbol(Enum):
    TAB: str = '    '
    OUTER: str = '│   '
    INNER: str = '├── '
    LAST: str = '└── '


@dataclass
class Dir:
    name: str
    lvl: int
    self_last: bool
    is_base: bool
    dir_content: list[str]
    next: Self = None


def dir_is_last(dir_it: str, dir_cont: list[str]) -> bool:
    return dir_cont[-1] == dir_it


def get_subdirs(parent_dir: Dir, depth: int) -> list[Dir]:
    dirs_this_lvl: list[Dir] = []

    if os.path.isdir(parent_dir.name):
        dir_content = os.listdir(parent_dir.name)
        for d in dir_content:
            full_path = os.path.join(parent_dir.name, d)
            parent_dir.dir_content.append(full_path)
    else:
        parent_dir.dir_content = []

    if len(parent_dir.dir_content) != 0:
        for dir_it in parent_dir.dir_content:
            subdir: Dir = Dir(name=dir_it, lvl=(parent_dir.lvl - 1),
                              self_last=dir_is_last(dir_it, parent_dir.dir_content), is_base=False, dir_content=[])
            if subdir.lvl != depth:  # because we don't need and indent for 'depth' (base) lvl
                subdir.next = parent_dir

            dirs_this_lvl.append(subdir)

            if subdir.lvl == 0:
                if subdir.self_last:
                    return dirs_this_lvl
            else:
                dirs_this_lvl.extend(get_subdirs(subdir, depth))

    return dirs_this_lvl


def get_tree(base_dir_name: str, depth: int) -> list[Dir]:
    base_dir = Dir(name=base_dir_name, lvl=(depth + 1), self_last=False, is_base=True, dir_content=[])

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
    if len(sys.argv) > 1:
        depth = int(sys.argv[1])
    else:
        depth = 0

    if len(sys.argv) > 2:
        base_folder = f'{os.getcwd()}{sys.argv[2]}'
    else:
        base_folder = f'{os.getcwd()}'

    my_tree = get_tree(base_folder, depth)
    print_tree(my_tree)


if __name__ == "__main__":
    main()