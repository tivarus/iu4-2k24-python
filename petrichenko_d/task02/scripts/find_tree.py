import os

import colorama
from colorama import Fore

# work on Windows
colorama.init()


def creating_list_from_directories_and_files(directory, max_depth, ready, current_depth=0):
    if current_depth > max_depth:
        return

    num_dirs = 0
    num_files = 0

    items = sorted(os.listdir(directory))
    for i, item in enumerate(items):
        item_path = os.path.join(directory, item)
        is_last = i == len(items) - 1

        if os.path.isdir(item_path):
            num_dirs += 1
            ready.append(Fore.BLUE + "|  " * current_depth + "+--" + item)
            ready, subdir_num_dirs, subdir_num_files = creating_list_from_directories_and_files(item_path, max_depth,
                                                                                                ready,
                                                                                                current_depth + 1)
            num_dirs += subdir_num_dirs
            num_files += subdir_num_files
        else:
            num_files += 1
            if is_last:
                ready.append(Fore.GREEN + "|  " * current_depth + "\\--" + item)
            else:
                ready.append(Fore.GREEN + "|  " * current_depth + "+--" + item)

    return ready, num_dirs, num_files
