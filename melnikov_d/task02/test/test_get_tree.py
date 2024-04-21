import pytest

from task02.src.tree import get_tree


@pytest.mark.parametrize(
    "path, depth, expected",
    [["../test_dir", 3, ['test_dir',
                            [['abc',
                                [['gd2', ['fsdl']],
                            'sds',
                            ['sad',
                                [['ret', ['123']]]],
                            'dds', 'fas']],
                            '1f',
                            ['gnf', []],
                            'asf']]]]
)
def test_get_tree(path: str, depth: int, expected: list):
    assert get_tree(path, depth) == expected
    pass
