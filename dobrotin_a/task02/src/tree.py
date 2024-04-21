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
    is_base: bool
    dir_content: list[str]
    is_last: bool = False
    par_dir: Self = None

    def __init__(self, name: str, lvl: int, is_base: bool, dir_content: list[str], par_dir: Self = None):
        self.name = name
        self.lvl = lvl
        self.is_base = is_base
        self.dir_content = dir_content
        self.par_dir = par_dir
        if par_dir is None:
            self.is_last = False
        else:
            self.is_last = self.par_dir.dir_content[-1] == self.name


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
            subdir: Dir = Dir(name=dir_it, lvl=(parent_dir.lvl - 1), is_base=False, dir_content=[], par_dir=parent_dir)

            dirs_this_lvl.append(subdir)

            if subdir.lvl == 0:
                if subdir.is_last:
                    return dirs_this_lvl
            else:
                dirs_this_lvl.extend(get_subdirs(subdir, depth))

    return dirs_this_lvl


def get_tree(base_dir_name: str, depth: int) -> list[Dir]:
    base_dir = Dir(name=base_dir_name, lvl=(depth + 1), is_base=True, dir_content=[])

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
    dir_cnt: int = 0
    files_cnt: int = 0
    for dir_it in tree:
        line: str = os.path.basename(dir_it.name)
        line = f'{get_output_color(dir_it.name)}{line}'
        if not dir_it.is_base:
            if os.path.isdir(dir_it.name):
                dir_cnt += 1
            else:
                files_cnt += 1

            if dir_it.is_last:
                line = f'{Symbol.LAST.value}{line}'
            else:
                line = f'{Symbol.INNER.value}{line}'

            parent_dir = dir_it.par_dir
            while parent_dir:
                if parent_dir.is_base:
                    line = line
                elif parent_dir.is_last:
                    line = f'{Symbol.TAB.value}{line}'
                else:
                    line = f'{Symbol.OUTER.value}{line}'
                parent_dir = parent_dir.par_dir
        print(f'{line}{Style.RESET_ALL}')
    print(f'Folders: {dir_cnt}, files: {files_cnt}')


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
