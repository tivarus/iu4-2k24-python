import os
from smd_classes import Node, Frame


def create_new_smd(old_smd: tuple[str, str, list[Node], list[Frame]]) -> None:
    """
    Create a new SMD file with modified positions and save it.

    Args:
        old_smd (tuple[str, str, list[Node], list[Frame]]): Tuple containing filename, directory, nodes, and frames.
    """
    filename, directory, nodes, frames = old_smd
    frames = modified_positions(frames)

    new_filename = f'new_{filename}'
    new_directory = os.path.join(directory, 'modified')
    full_filename = os.path.join(new_directory, new_filename)

    check_or_create_directory(new_directory)
    output_smd(full_filename, nodes, frames)


def modified_positions(frames: list[Frame]) -> list[Frame]:
    """
    Modifies the positions of the first PositionNode in each Frame to have x and y coordinates set to 0.0.

    Args:
        frames (list[Frame]): A list of Frame objects to be modified.

    Returns:
        list[Frame]: The modified list of Frame objects.
    """
    for frame in frames:
        pos = frame.positions[0]
        pos.x = 0.0
        pos.y = 0.0
    return frames


def output_smd(filename: str, nodes: list[Node], frames: list[Frame]) -> None:
    """
    Display nodes and frames to an SMD file.

    Args:
        filename (str): The name of the SMD file to be created.
        nodes (list[Node]): List of Node objects.
        frames (list[Frame]): List of Frame objects.
    """
    with open(filename, 'wt', encoding='utf-8') as new_smd:
        new_smd.write('nodes\n')
        for node in nodes:
            node.write_to_file(new_smd)
        new_smd.write('end\nskeleton\n')
        for frame in frames:
            frame.write_to_file(new_smd)
        new_smd.write('end\n')


def check_or_create_directory(dir_name: str) -> None:
    """
    Check if directory exists, create it if not.

    Args:
        dir_name (str): The name of the directory.
    """
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass
