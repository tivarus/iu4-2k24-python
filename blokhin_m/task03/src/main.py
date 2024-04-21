import argparse
import os
from smd_handler_classes import SMDParser, SMDModifier


def main() -> None:
    parser = argparse.ArgumentParser(description='Modified smd file')
    parser.add_argument('file', type=str)
    parser.add_argument('-dir', type=str, default=f'{os.getcwd()}')

    args = parser.parse_args()
    SMDModifier.create_new(SMDParser.parse(args.file, args.dir))


if __name__ == '__main__':
    main()
