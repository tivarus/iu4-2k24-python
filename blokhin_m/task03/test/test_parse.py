import os
import pytest
from smd_handler_classes import SMDParser


@pytest.mark.parametrize(
    argnames='numb_node, numb_frames, fl',
    argvalues=[
        [85, 300, 'a_c4_defuse_crouch.smd'],
        [85, 1, 'a_death_pose_head_SE.smd'],
        [85, 22, 'a_fall.smd'],
        [85, 67, 'a_move_runSE.smd'],
        [85, 91, 'a_move_walkNE.smd']
    ]
)
def test_parse_smd(numb_node: int, numb_frames: int, fl: str) -> None:
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
    fl, directory, nodes, frames = SMDParser.parse(fl, dir_path)

    assert len(nodes) == numb_node and len(frames) == numb_frames
