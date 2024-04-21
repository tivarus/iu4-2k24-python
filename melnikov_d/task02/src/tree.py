import os
from colorama import Fore, Style


def get_directory_content(path: str, depth: int) -> list:
    content = []

    if depth < 0:
        return content
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            content.append([item, get_directory_content(item_path, depth - 1)])
        else:
            content.append(item)
    return content


def get_tree(path: str, depth: int) -> list:
    return [os.path.basename(path), get_directory_content(path, depth)]


def print_tree(path: str, depth: int = 0) -> None:
    tree = get_tree(path, depth)

    print(tree)

    _print_tree(tree)


def _print_tree(tree: list, depth: int = 0) -> None:
    name, content = tree
    print(Fore.CYAN + Style.BRIGHT + '    ' * depth + '|-- ' + name)
    for item in content:
        if isinstance(item, list):
            _print_tree(item, depth + 1)
        else:
            print(Fore.RED + Style.BRIGHT + '    ' * (depth + 1) + '|-- ' + Fore.RED + item)
