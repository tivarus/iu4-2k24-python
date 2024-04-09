import os
import sys

from enum import Enum
from typing import List
from typing import Tuple

class inden(Enum):
    EMPTY = "    "
    END = "└── "
    INTERVAL = "├── "
    VERTICAL = "│   "

class fselids(Enum):
    PATH = 0
    TYPE = 1

class arg(Enum):
    PATH = 2
    RECURSION = 1

class path_types(Enum):
    FILE = 0
    DIRRECTORY = 1

class Scan_ids(Enum):
    DIRRECTORIES_COUNT = 1
    FILES_COUNT = 2
    RESULT = 0

class ter_styles(Enum):
    RED = "\033[31m"
    PURPLE = "\033[35m"
    RESSET = "\033[36m"

def gener_inden(lines: List[bool]) -> str:
    result: str = ""

    for element in lines:
        result = f"{result}{inden.VERTICAL.value if element else inden.EMPTY.value}"

    return result

def gener_u_l(
    dirnames: List[str], filenames: List[str]
) -> List[List]:  # List[[str, bool]]
    result_list: List[List] = []  # List[[str, bool]]

    for dirname in dirnames:
        result_list.append([dirname, path_types.DIRRECTORY.value])
    for filename in filenames:
        result_list.append([filename, path_types.FILE.value])

    result_list.sort(
        key=lambda arr: arr[fselids.PATH.value], reverse=False
    )  # by name

    return result_list

def get_p(arguments: List[str]) -> str:
    try:
        return arguments[arg.PATH.value]
    except Exception:
        return ""

def get_r_n(arguments: List[str]) -> int:
    try:
        result = int(arguments[arg.RECURSION.value])
        if result < 0:
            return 0
        return result
    except Exception:
        return 0

def set_style(input: str, style: str) -> str:
    return f"{style}{input}{ter_styles.RESSET.value}"

def scan_dir(
    scan_dir_path: str, curr_req: int, lines: List[bool]
) -> Tuple[str, int, int]:  # Tuple[paths, dirs_count, files_count]
    result: str = ""

    indentation = gener_inden(lines)

    union_list: List[List] = []  # List[[str, bool]]

    directories_count: int = 0
    files_count: int = 0

    for dirpaths, dirnames, filenames in os.walk(scan_dir_path):
        union_list = gener_u_l(dirnames=dirnames, filenames=filenames)
        dirs_count = len(dirnames)

        directories_count = len(dirnames)
        files_count = len(filenames)
        break

    dirrectory_iterator: int = 0
    element_iterator: int = 0
    for element in union_list:
        element_iterator += 1

        name: str = element[fselids.PATH.value]
        name = set_style(
            element[fselids.PATH.value],
            ter_styles.RED.value
            if element[fselids.TYPE.value] == path_types.DIRRECTORY.value
            else ter_styles.PURPLE.value,
        )

        if element[fselids.TYPE.value] == path_types.DIRRECTORY.value:
            dirrectory_iterator += 1

        complete_indentation: str = (
            f"{indentation}{inden.END.value}"
            if element_iterator == len(union_list)
            else f"{indentation}{inden.INTERVAL.value}"
        )

        result = f"{result}{complete_indentation}{name}\n\r"

        if curr_req > 1:
            lines.append(dirrectory_iterator < dirs_count)

            subdirrectory_scan_result: str = scan_dir(
                f"{scan_dir_path}/{element[fselids.PATH.value]}",
                curr_req - 1,
                lines,
            )
            directories_count += subdirrectory_scan_result[
                Scan_ids.DIRRECTORIES_COUNT.value
            ]
            files_count += subdirrectory_scan_result[Scan_ids.FILES_COUNT.value]
            result = f"{result}{subdirrectory_scan_result[Scan_ids.RESULT.value]}"

            lines.pop()

    return result, directories_count, files_count

def main():
    check_path: str = get_p(sys.argv)
    reqursion: int = get_r_n(sys.argv)

    if reqursion == 0:
        print("ERROR::List of arguments is wrong.")
        exit()

    lines: List[bool] = []

    print(check_path)

    scan_dirrectory_result: Tuple[str, int, int] = scan_dir(
        check_path, reqursion, lines
    )
    print(scan_dirrectory_result[Scan_ids.RESULT.value])
    print(
        f"{scan_dirrectory_result[Scan_ids.DIRRECTORIES_COUNT.value]} directories",
        end=", ",
    )
    print(f"{scan_dirrectory_result[Scan_ids.FILES_COUNT.value]} files")


if __name__ == "__main__":
    main()