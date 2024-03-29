import os
import sys
import pytest
# from src.smd_parse import generate_tree
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
def test_generate_tree(file_path: str, time: int):

    original_stdout = sys.stdout
    try:
        parser_1 = SMDParser(file_path)
        # redirect cout to a file output.smd
        with open("output.smd", "w") as test_output:
            sys.stdout = test_output
            # fill in the file with the output of get_smd_info()
            parser_1.print_nodes()
            print("end")
            parser_1.frame_from_smd_file(time)
            print()
            parser_1.print_frame()
            print("end")
        sys.stdout = original_stdout
        # read data from temporary file
        parser_2 = SMDParser("output.smd")
        parser_2.frame_from_smd_file(time)

        assert parser_1.nodes == parser_2.nodes

    finally:
        os.remove("output.smd")
