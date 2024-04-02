import os
import pytest
from src.smd_parse import SMDParser


@pytest.mark.parametrize(
    argnames="file_path, time",
    argvalues=[
        ["..\\animset_t_anims\\a_move_c4_runS.smd", 27],
        ["..\\animset_t_anims\\a_move_c4_runS.smd", 28],
        ["..\\animset_t_anims\\a_move_c4_runSE.smd", 53],
        ["..\\animset_t_anims\\a_move_c4_runSE.smd", 54],
        ["..\\animset_t_anims\\a_move_c4_runSW.smd", 0],
        ["..\\animset_t_anims\\a_move_c4_runSW.smd", 1]
    ]
)
def test_smd_parse(file_path: str, time: int):

    try:
        parser_1 = SMDParser(file_path)
        # fill in the file with the output
        with open("output.smd", "w"):
            pass
        parser_1.print_nodes("output.smd")
        parser_1.frame_from_smd_file(time)
        parser_1.print_frame("output.smd")
        # read data from temporary file
        parser_2 = SMDParser("output.smd")
        parser_2.frame_from_smd_file(time)

        assert parser_1.nodes == parser_2.nodes

    finally:
        os.remove("output.smd")
