import os
import pytest
from tree import get_tree, print_tree


@pytest.fixture
def create_directory_structure():
    base_dir = 'test_dir'
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir1'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir2'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir2', 'subsubdir'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir3'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir3', 'subsubdir1'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir3', 'subsubdir2'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir3', 'subsubdir2', 'subbbdir1'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir3', 'subsubdir2', 'subbbdir1', 'now_last_for_sure'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'subdir3', 'subsubdir2', 'subbbdir2'), exist_ok=True)
    yield base_dir
    os.system(f'rd /s /q {base_dir}')  # Cleanup after the test


def test_tree_depth_1(create_directory_structure, capsys):
    base_dir = create_directory_structure
    tree = get_tree(base_dir, 1)
    print_tree(tree)
    captured = capsys.readouterr()
    expected_output = (
        "\x1b[34mtest_dir\x1b[0m\n"
        "├── \x1b[34msubdir1\x1b[0m\n"
        "├── \x1b[34msubdir2\x1b[0m\n"
        "│   └── \x1b[34msubsubdir\x1b[0m\n"
        "└── \x1b[34msubdir3\x1b[0m\n"
        "    ├── \x1b[34msubsubdir1\x1b[0m\n"
        "    └── \x1b[34msubsubdir2\x1b[0m\n"
        "Folders: 6, files: 0\n"
    )
    assert captured.out == expected_output


def test_tree_depth_2(create_directory_structure, capsys):
    base_dir = create_directory_structure
    tree = get_tree(base_dir, 2)
    print_tree(tree)
    captured = capsys.readouterr()
    expected_output = (
        "\x1b[34mtest_dir\x1b[0m\n"
        "├── \x1b[34msubdir1\x1b[0m\n"
        "├── \x1b[34msubdir2\x1b[0m\n"
        "│   └── \x1b[34msubsubdir\x1b[0m\n"
        "└── \x1b[34msubdir3\x1b[0m\n"
        "    ├── \x1b[34msubsubdir1\x1b[0m\n"
        "    └── \x1b[34msubsubdir2\x1b[0m\n"
        "        ├── \x1b[34msubbbdir1\x1b[0m\n"
        "        └── \x1b[34msubbbdir2\x1b[0m\n"
        "Folders: 8, files: 0\n"
    )
    assert captured.out == expected_output


def test_tree_depth_3(create_directory_structure, capsys):
    base_dir = create_directory_structure
    tree = get_tree(base_dir, 3)
    print_tree(tree)
    captured = capsys.readouterr()
    expected_output = (
        "\x1b[34mtest_dir\x1b[0m\n"
        "├── \x1b[34msubdir1\x1b[0m\n"
        "├── \x1b[34msubdir2\x1b[0m\n"
        "│   └── \x1b[34msubsubdir\x1b[0m\n"
        "└── \x1b[34msubdir3\x1b[0m\n"
        "    ├── \x1b[34msubsubdir1\x1b[0m\n"
        "    └── \x1b[34msubsubdir2\x1b[0m\n"
        "        ├── \x1b[34msubbbdir1\x1b[0m\n"
        "        │   └── \x1b[34mnow_last_for_sure\x1b[0m\n"
        "        └── \x1b[34msubbbdir2\x1b[0m\n"
        "Folders: 9, files: 0\n"
    )
    assert captured.out == expected_output
