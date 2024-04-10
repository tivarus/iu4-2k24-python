import argparse
import os
from generate_smd import generateSmd
from parser import parse_file
from modification import modificateFile
import extras


def main() -> None:
    parser = argparse.ArgumentParser(description='Command for modified smd file')
    my_file = extras.get_filepath("a_move_c4_walkNW.smd")
    # parser.add_argument('file', type=str, default=f"{my_file}",
    #                     help='Name of the smd file to be modified')
    # extras_dir = 'la-la'
    # parser.add_argument('-dir', type=str, default=f'{extras_dir}',
    #                     help='Directory where the file are stored (default: working directory)')
    #
    # args = parser.parse_args()
    generateSmd(modificateFile(parse_file(my_file)))
#modificateFile

if __name__ == '__main__':
    main()
