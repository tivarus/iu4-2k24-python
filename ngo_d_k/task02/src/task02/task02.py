import os
import sys

from enum import Enum
from typing import List
from typing import Tuple

class Indentations(Enum):
    EMPTY = "    "
    END = "└── "
    INTERVAL = "├── "
    VERTICAL = "│   "

class FS_Elements_List_IDs(Enum):
    PATH = 0
    TYPE = 1

class Arguments_IDs(Enum):
    PATH = 2
    RECURSION = 1

class Paths_Types(Enum):
    FILE = 0
    DIRRECTORY = 1

class Scan_Result_IDs(Enum):
    DIRRECTORIES_COUNT = 1
    FILES_COUNT = 2
    RESULT = 0

class Terminal_Styles(Enum):
    RED = "\033[31m"
    PURPLE = "\033[35m"
    RESSET = "\033[36m"

def generate_indentations(lines: List[bool]) -> str:
    result: str = ""

    for element in lines:
        result = f"{result}{Indentations.VERTICAL.value if element else Indentations.EMPTY.value}"

    return result

def generate_union_list(
    dirnames: List[str], filenames: List[str]
) -> List[List]: 
    result_list: List[List] = []  

    for dirname in dirnames:
        result_list.append([dirname, Paths_Types.DIRRECTORY.value])
    for filename in filenames:
        result_list.append([filename, Paths_Types.FILE.value])

    result_list.sort(
        key=lambda arr: arr[FS_Elements_List_IDs.PATH.value], reverse=False
    )  # by name

    return result_list

def get_path(Arguments_IDsuments: List[str]) -> str:
    try:
        return Arguments_IDsuments[Arguments_IDs.PATH.value]
    except Exception:
        return ""

def get_reqursion_number(arguments: List[str]) -> int:
    try:
        result = int(arguments[Arguments_IDs.RECURSION.value])
        if result < 0:
            return 0
        return result
    except Exception:
        return 0

def set_style(input: str, style: str) -> str:
    return f"{style}{input}{Terminal_Styles.RESSET.value}"

def scan_dirrectory(
    scan_dir_path: str, curr_req: int, lines: List[bool]
) -> Tuple[str, int, int]:  # Tuple[paths, dirs_count, files_count]
    result: str = ""

    Indentationstation = generate_indentations(lines)

    union_list: List[List] = []  

    directories_count: int = 0
    files_count: int = 0

    try:
        dirpaths, dirnames, filenames = next(os.walk(scan_dir_path))
        union_list = generate_union_list(dirnames=dirnames, filenames=filenames)
        dirs_count = len(dirnames)

        directories_count = len(dirnames)
        files_count = len(filenames)
    except StopIteration:
        return result, 0, 0

    dirrectory_iterator: int = 0
    element_iterator: int = 0
    for element in union_list:
        element_iterator += 1

        name: str = element[FS_Elements_List_IDs.PATH.value]
        name = set_style(
            element[FS_Elements_List_IDs.PATH.value],
            Terminal_Styles.RED.value
            if element[FS_Elements_List_IDs.TYPE.value] == Paths_Types.DIRRECTORY.value
            else Terminal_Styles.PURPLE.value,
        )

        if element[FS_Elements_List_IDs.TYPE.value] == Paths_Types.DIRRECTORY.value:
            dirrectory_iterator += 1

        complete_Indentationstation: str = (
            f"{Indentationstation}{Indentations.END.value}"
            if element_iterator == len(union_list)
            else f"{Indentationstation}{Indentations.INTERVAL.value}"
        )

        result = f"{result}{complete_Indentationstation}{name}\n\r"

        if curr_req > 1:
            lines.append(dirrectory_iterator < dirs_count)

            subdirrectory_scan_result: str = scan_dirrectory(
                f"{scan_dir_path}/{element[FS_Elements_List_IDs.PATH.value]}",
                curr_req - 1,
                lines,
            )
            directories_count += subdirrectory_scan_result[
                Scan_Result_IDs.DIRRECTORIES_COUNT.value
            ]
            files_count += subdirrectory_scan_result[Scan_Result_IDs.FILES_COUNT.value]
            result = f"{result}{subdirrectory_scan_result[Scan_Result_IDs.RESULT.value]}"

            lines.pop()

    return result, directories_count, files_count

def main():
    check_path: str = get_path(sys.argv)
    reqursion: int = get_reqursion_number(sys.argv)

    if reqursion == 0:
        print("ERROR::List of arguments is wrong.")
        exit()

    lines: List[bool] = []

    print(check_path)

    scan_dirrectory_result: Tuple[str, int, int] = scan_dirrectory(
        check_path, reqursion, lines
    )
    print(scan_dirrectory_result[Scan_Result_IDs.RESULT.value])
    print(
        f"{scan_dirrectory_result[Scan_Result_IDs.DIRRECTORIES_COUNT.value]} directories",
        end=", ",
    )
    print(f"{scan_dirrectory_result[Scan_Result_IDs.FILES_COUNT.value]} files")


if __name__ == "__main__":
    main()
