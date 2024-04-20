import pytest

from typing import List

from src.task02.task02 import (
    generate_indentations,
    generate_union_list,
    get_path,
    get_reqursion_number,
)


@pytest.mark.parametrize(
    "lines,expected",
    [
        [[], ""],
        [[True, True, False, True], "│   │       │   "],
        [[False, True, False, True, True], "    │       │   │   "],
        [[True, True, True, True], "│   │   │   │   "],
        [[False], "    "],
        [[False, False, False, False], "                "],
    ],
)
def test_generate_indentations(lines: List[bool], expected: str):
    assert generate_indentations(lines) == expected


@pytest.mark.parametrize(
    "dirnames,filenames,expected",
    [
        [[], [], []],
        [
            [],
            ["f1", "f5", "f0", "f9"],
            [["f0", False], ["f1", False], ["f5", False], ["f9", False]],
        ],
        [
            ["d4", "d2", "d8", "d0"],
            [],
            [["d0", True], ["d2", True], ["d4", True], ["d8", True]],
        ],
        [
            ["ab_d", "ef_d", "ig_d", "op_d"],
            ["cd_f", "gh_f", "kl_f"],
            [
                ["ab_d", True],
                ["cd_f", False],
                ["ef_d", True],
                ["gh_f", False],
                ["ig_d", True],
                ["kl_f", False],
                ["op_d", True],
            ],
        ],
    ],
)
def test_generate_union_list(
    dirnames: List[str], filenames: List[str], expected: List[List]
):  # List[[str, bool]]
    assert generate_union_list(dirnames, filenames) == expected


@pytest.mark.parametrize(
    "arguments,expected",
    [
        [[], ""],
        [["progname"], ""],
        [["progname", "1"], ""],
        [["progname", "1", "path"], "path"],
        [["abc", "def", "ghi", "jkl"], "ghi"],
    ],
)
def test_get_path(arguments: List[str], expected: str):
    assert get_path(arguments) == expected


@pytest.mark.parametrize(
    "arguments,expected",
    [
        [[], 0],
        [["progname"], 0],
        [["progname", "34"], 34],
        [["progname", "1", "path"], 1],
        [["progname", "path", "1"], 0],
        [["abcd", "109", "path", "arg1", "arg2"], 109],
        [["efgh", "-1000", "pth", "ar1", "ar56"], 0],
        [["efgh", "1.23", "sdf", "sadas"], 0],
        [["efgh", "1.23e3", "sdf", "sadas"], 0],
    ],
)
def test_get_reqursion_number(arguments: List[str], expected: int):
    assert get_reqursion_number(arguments) == expected
