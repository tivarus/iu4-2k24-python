
import pytest
import os
from pathlib import Path
from src.task02 import tree
import shutil


@pytest.fixture
def create_tmp_dir() -> str:

    os.mkdir("./Serebrennikov_A/task02/test/tmp_dir")
    os.mkdir("./Serebrennikov_A/task02/test/tmp_dir/root_dir")
    os.mkdir("./Serebrennikov_A/task02/test/tmp_dir/root_dir/test_dir_1")
    os.mkdir("./Serebrennikov_A/task02/test/tmp_dir/root_dir/test_dir_2")
    open("./Serebrennikov_A/task02/test/tmp_dir/root_dir/test_dir_1/test1.txt", 'x')
    open("./Serebrennikov_A/task02/test/tmp_dir/root_dir/test_dir_2/test2.txt", 'x')
    open("./Serebrennikov_A/task02/test/tmp_dir/root_dir/test_dir_2/test3.txt", 'x')
    open("./Serebrennikov_A/task02/test/tmp_dir/root_dir/test_dir_2/test4.txt", 'x')
    open("./Serebrennikov_A/task02/test/tmp_dir/root_dir/test.txt", 'x')
    return "./Serebrennikov_A/task02/test/tmp_dir"


def remove_tmp_dir(rm_path: str):
    shutil.rmtree(rm_path)


def test_tree(create_tmp_dir) -> None:
    tmp_path = create_tmp_dir
    result = tree(path=Path(tmp_path), depth=3, curr_lvl=1)
    expected_result = [5, 3, [
        "\x1b[37m└── \x1b[34mroot_dir",
        "\x1b[37m    ├── \x1b[32mtest.txt",
        "\x1b[37m    ├── \x1b[34mtest_dir_1",
        "\x1b[37m    │   └── \x1b[32mtest1.txt",
        "\x1b[37m    └── \x1b[34mtest_dir_2",
        "\x1b[37m        ├── \x1b[32mtest2.txt",
        "\x1b[37m        ├── \x1b[32mtest3.txt",
        "\x1b[37m        └── \x1b[32mtest4.txt"
    ]]
    remove_tmp_dir(tmp_path)
    assert result == expected_result
