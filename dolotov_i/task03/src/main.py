from lib import smd_parse
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('value', type=str, help='Name of file')
    args = parser.parse_args()

    # filename = 'a_move_grenade_walkE.smd'
    filename = args.value
    smd_parse(filename)


if __name__ == '__main__':
    main()
