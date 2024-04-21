import pytest
from src.Task03.animation_parser_alternative import *


def test_node_parse():
    filename = "P:\\Pyton\\T3\\animset_t_anims\\a_move_c4_walkNE.smd"
    parsed_nodes = parse_nodes(filename)
    assert len(parsed_nodes) == 85



def test_frame_parse():
    filename = "a_move_c4_walkNE.smd"
    parsed_animation = parse_animation(filename)
    assert len(parsed_animation) == 91


def test_nodes_in_frames():
    filename = "a_move_c4_walkNE.smd"
    parsed_nodes = parse_nodes(filename)
    parsed_animation = parse_animation(filename)
    assert len(parsed_nodes) == len(parsed_animation[0].bones)
