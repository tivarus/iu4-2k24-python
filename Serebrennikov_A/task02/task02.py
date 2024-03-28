import argparse
import os
import sys

def pritn_tree():
    print("Tree:")


def main():

    parser = argparse.ArgumentParser(description = 'Dir path for tree')
    parser.add_argument('-L', '--Length', default = '0', help = 'Tree depth')
    parser.add_argument('RootDir', nargs = '?', default = '.', help = 'Tree path')
    args = parser.parse_args()

    if (os.path.exists(args.RootDir) == False):
        print("No such file or directory")
        sys.exit(-1)
    else:
        pritn_tree()

    #print(args)

if __name__ == "__main__":
    main()