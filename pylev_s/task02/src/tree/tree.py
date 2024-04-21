import os
from colorama import Fore, Style

PIPE = "│   "
TEE = "├───"
ELBOW = "└───"
BLANK = "    "


def run_tree(path: str, depth: int, output_stream):

    current_depth = 0

    directory_structure = create_tree(path, current_depth, depth)

    print(path, file=output_stream)
    print_tree(directory_structure[1:], "", output_stream)

    directories_count, files_count, links_count = count_entries(directory_structure)
    print(f"\n{directories_count} directories, {files_count} files, {links_count} links", file=output_stream)


def create_tree(path: str, current_depth: int, start_depth: int) -> list[str | list[str] | list[str, list]]:

    result = [path]

    if (start_depth < 0) or (start_depth > 0 and (start_depth - current_depth)):
        try:
            directory_items = sorted(os.listdir(path))
        except (PermissionError, FileNotFoundError):
            result.append([path, "PERMISSION DENIED"])
        else:
            for item in directory_items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    result.append(create_tree(full_path, current_depth + 1, start_depth))
                else:
                    result.append(full_path)
    return result


def count_entries(structure: list) -> tuple[int, int, int]:
    directories, files, links = 0, 0, 0

    for item in structure:
        if isinstance(item, str):
            if os.path.islink(item):
                links += 1
            elif os.path.isdir(item):
                directories += 1
            elif os.path.isfile(item):
                files += 1
        elif isinstance(item, list):
            sub_directories, sub_files, sub_links = count_entries(item)
            directories += sub_directories
            files += sub_files
            links += sub_links

    return directories, files, links


def print_tree(structure: list, prefix: str, output_stream):
    for item in structure:
        if isinstance(item, str):
            print_entry(os.path.basename(item), os.path.join(item, ".."), prefix, item is structure[-1], output_stream)
        elif isinstance(item, list):
            print_entry(os.path.basename(item[0]), os.path.join(item[0], ".."), prefix, item is structure[-1],
                        output_stream)
            print_tree(item[1:], prefix + (PIPE if not (item is structure[-1]) else BLANK), output_stream)


def print_entry(name: str, path_prefix: str, prefix: str, is_last: bool, output_stream):
    full_path = os.path.join(path_prefix, name)

    print(f"{prefix}{ELBOW if is_last else TEE}", end="", file=output_stream)
    print(f"{get_output_color(full_path)}{name}", end="", file=output_stream)

    if os.path.islink(full_path):
        print(f" -> {os.path.realpath(full_path)}", end="", file=output_stream)

    print(Style.RESET_ALL, file=output_stream)


def get_output_color(path: str) -> str:
    if os.path.isdir(path):
        return Fore.BLUE
    elif os.path.islink(path):
        return Fore.CYAN
    elif os.path.isfile(path):
        return Fore.GREEN
    else:
        return Fore.RED
