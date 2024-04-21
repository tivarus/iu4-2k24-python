import pytest
from src.parce import *


@pytest.fixture
def file1():
    smd_data = SmdData()
    smd_data.parse_smd("a_move_walkS.smd")
    smd_data.write_to_file("output.smd")
    return "output.smd"


@pytest.fixture
def file2():
    return "a_move_walkS.smd"


def test_compare_files_from_third_line(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        for _ in range(2):  # Skip first two lines
            next(f2)
        for line1, line2 in zip(f1, f2):
            assert line1 == line2
