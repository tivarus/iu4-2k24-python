import os
from smd_classes import Node, Frame


def parse_file(filename: str, directory: str = os.getcwd()) -> tuple[str, str, list[Node], list[Frame]]:
    """
    Parse an SMD file and return its components.

    Args:
        filename (str): The name of the SMD file.
        directory (str, optional): The directory where the file is located. Defaults to the current working directory.

    Returns:
        tuple[str, str, list[Node], list[Frame]]: A tuple containing filename, directory, nodes, and frames.
    """
    nodes = []
    frames = []
    full_filename = os.path.join(directory, filename)
    try:
        nodes, frames = read_smd(full_filename)
        return filename, directory, nodes, frames
    except FileNotFoundError:
        return filename, directory, nodes, frames


def read_smd(filename: str) -> tuple[list[Node], list[Frame]]:
    """
    Read an SMD file and extract nodes and frames.

    Args:
        filename (str): The name of the SMD file.

    Returns:
        tuple[list[Node], list[Frame]]: A tuple containing read out nodes and frames.
    """
    nodes = []
    frames = []
    with open(filename, 'rt') as file_smd:
        current_section = None
        for line in file_smd:
            line = line.strip()
            if line.startswith('nodes'):
                current_section = 'nodes'
            elif line.startswith('skeleton'):
                current_section = 'skeleton'
            elif line.startswith('end'):
                current_section = None

            elif current_section == 'nodes':
                nodes.append(Node.from_line(line))

            elif current_section == 'skeleton':
                if line.startswith('time'):
                    frame_id = int(line.split()[1])
                    positions = []
                else:
                    positions.append(line)
                    if len(positions) == len(nodes):
                        frames.append(Frame.from_lines(frame_id, positions))

    return nodes, frames
