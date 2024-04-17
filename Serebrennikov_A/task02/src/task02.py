import argparse
import os
import sys
from pathlib import Path
from enum import Enum
from colorama import Fore


class Symbols(Enum):
    """Class with symbols for tree printing"""
    S = '    '
    B = '│   '
    T = '├── '
    L = '└── '


def sortByAlphabet(inputStr: str) -> str:
    return str(inputStr).casefold()


def tree(path: Path, depth: int, curr_lvl: int, init_symb: str = '', result: list = [None], files: int = 0, dirs: int = 0) -> list:
    path_list = list(path.glob('*'))
    path_list.sort(key=sortByAlphabet)
    symbols = [Symbols.T.value] * (len(path_list) - 1) + [Symbols.L.value]

    for symbol, path in zip(symbols, path_list):
        if path.is_dir():
            dirs += 1
            result.append(
                f'{Fore.WHITE}{init_symb}{symbol}{Fore.BLUE}{path.name}')
            if curr_lvl < depth or depth == 0:
                init_symb_next = init_symb + \
                    (Symbols.B.value if (symbol == Symbols.T.value) else Symbols.S.value)
                count = tree(path, depth, curr_lvl+1, init_symb_next, result)
                files += count[0]
                dirs += count[1]
        else:
            files += 1
            result.append(
                f'{Fore.WHITE}{init_symb}{symbol}{Fore.GREEN}{path.name}')

    if curr_lvl == 1:
        result = list(filter(None, result))
        print('\n'.join(result))
        print(f'{dirs} directories, {files} files')

    return [files, dirs, result]


def main():
    parser = argparse.ArgumentParser(description='Dir path for tree')
    parser.add_argument('-L', '--Length', default='0', help='Tree depth')
    parser.add_argument('RootDir', nargs='?', default='.', help='Tree path')
    args = parser.parse_args()
    if (os.path.exists(args.RootDir) == False):
        print("No such file or directory")
        sys.exit(-1)

    tree(Path(args.RootDir), int(args.Length), 1)


if __name__ == "__main__":
    main()
