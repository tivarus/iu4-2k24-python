import os

# types of branches
INTERMEDIATE_BRANCH = '├── '
CONTINUING_BRANCH = '│   '
LAST_BRANCH = '└── '

# codes of colors
COLOR_RESET = '\033[0m'
COLOR_BOLD = '\033[1m'
COLOR_BLUE = '\033[94m'
COLOR_GREEN = '\033[92m'


def run(directory: str, max_depth: int = None, depth=0, indent='', counts=None):
    if depth == max_depth:
        return
    if not os.path.isdir(directory):
        print("Not a directory")
        return
    if counts is None:
        counts = {'files': 0, 'dirs': 0}

    items = sorted(os.listdir(directory))
    for item in items:
        path = os.path.join(directory, item)
        if item == items[-1]:
            if os.path.isdir(path):
                print(indent + LAST_BRANCH + COLOR_BLUE + item + COLOR_RESET)
                counts['dirs'] += 1
                run(path, max_depth, depth + 1, indent + '    ', counts)
            else:
                print(indent + LAST_BRANCH + COLOR_GREEN + item + COLOR_RESET)
                counts['files'] += 1
        else:
            if os.path.isdir(path):
                print(f"{indent}{INTERMEDIATE_BRANCH}{COLOR_BLUE}{item}{COLOR_RESET}")
                counts['dirs'] += 1
                run(path, max_depth, depth + 1, indent + CONTINUING_BRANCH, counts)
            else:
                print(f"{indent}{INTERMEDIATE_BRANCH}{COLOR_GREEN}{item}{COLOR_RESET}")
                counts['files'] += 1

    if depth == 0:
        print(f"\n{counts['dirs']} directories, {counts['files']} files")
