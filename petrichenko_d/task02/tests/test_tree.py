import os

import pytest

from task02.scripts.find_tree import creating_list_from_directories_and_files


@pytest.mark.parametrize(
    "start_path, max_level, expected",
    [
        [os.getcwd(), 5, (['\x1b[34m+--new1',
                           '\x1b[32m|  \\--kek.py',
                           '\x1b[34m+--new2',
                           '\x1b[32m|  \\--lol.py',
                           '\x1b[32m\\--test_tree.py'],
                          6,
                          10)],
        [os.getcwd(), 10, (['\x1b[34m+--new1',
                            '\x1b[32m|  \\--kek.py',
                            '\x1b[34m+--new2',
                            '\x1b[32m|  \\--lol.py',
                            '\x1b[32m\\--test_tree.py'],
                           6,
                           10)]
    ]
)
def test_kek(start_path: str, max_level: int, expected: list[str]):
    ready = []
    assert creating_list_from_directories_and_files(start_path, max_level, ready) == expected
