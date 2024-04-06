import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class Node:
    """
    Class representing a node of the model from a .smd file.

    Attributes:
        name (str): Name of the node.
        index (int): Index of the node.
        parent_index (int): Index of the parent node.
        positions (List[List[float]]): List of node positions for each frame.
        orientations (List[List[float]]): List of node orientations for each frame.
    """
    name: str
    index: int
    parent_index: int
    positions: List[List[float]] = field(default_factory=list)
    orientations: List[List[float]] = field(default_factory=list)

    def print_info(self) -> None:
        """Prints information about the node."""
        print("Node:", self.name)
        print("Index:", self.index)
        print("Parent Index:", self.parent_index)
        print("Positions:", self.positions)
        print("Orientations:", self.orientations)
        print()

    def get_position_at_time(self, frame_index: int) -> List[float]:
        """
        Returns the position of the node at the specified frame index.

        Args:
            frame_index (int): Index of the frame.

        Returns:
            Union[List[float], None]: List of position coordinates if available, None otherwise.
        """
        if 0 <= frame_index < len(self.positions):
            return self.positions[frame_index]
        return None

    def get_orientation_at_time(self, frame_index: int) -> List[float]:
        """
        Returns the orientation of the node at the specified frame index.

        Args:
            frame_index (int): Index of the frame.

        Returns:
            Union[List[float], None]: List of orientation values if available, None otherwise.
        """
        if 0 <= frame_index < len(self.orientations):
            return self.orientations[frame_index]
        return None

    def set_position_at_time(self, frame_index: int, position: List[float]) -> None:
        """
        Replaces the position of the node at the specified frame index with the given position.

        Args:
            frame_index (int): Index of the frame.
            position (List[float]): New position coordinates.

        Raises:
            ValueError: If the length of the position list is not 3.
        """
        if len(position) != 3:
            raise ValueError("Position list must contain exactly 3 values.")
        if 0 <= frame_index < len(self.positions):
            self.positions[frame_index] = position

    def set_orientation_at_time(self, frame_index: int, orientation: List[float]) -> None:
        """
        Replaces the orientation of the node at the specified frame index with the given orientation.

        Args:
            frame_index (int): Index of the frame.
            orientation (List[float]): New orientation values.

        Raises:
            ValueError: If the length of the orientation list is not 3.
        """
        if len(orientation) != 3:
            raise ValueError("Orientation list must contain exactly 3 values.")
        if 0 <= frame_index < len(self.orientations):
            self.orientations[frame_index] = orientation


@dataclass
class SmdData:
    """
    Class representing data from a .smd file.

    Attributes:
        nodes (List[Node]): List of all model nodes.
    """
    nodes: List[Node] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        """Adds a node to the list."""
        self.nodes.append(node)

    def parse_smd(self, filename: str) -> None:
        """
        Parses a .smd file and populates the SmdData object.

        Args:
            filename (str): Name of the .smd file.
        """
        with open(filename, 'r') as file:
            node_flag = False
            for line in file:
                line = line.strip()
                if line.startswith("// Created by"):
                    continue
                elif line.startswith("version"):
                    continue
                elif line.startswith("skeleton"):
                    continue
                elif line.startswith("nodes"):
                    node_flag = True
                    continue
                elif line.startswith("end"):
                    if node_flag is True:
                        node_flag = False
                elif node_flag is True:
                    parts = re.split(r'[\s"]+', line.strip())
                    node_index = int(parts[0])
                    node_name = parts[1]
                    parent_index = int(parts[2])
                    node = Node(node_name, node_index, parent_index)
                    self.add_node(node)
                elif line.startswith("time"):
                    print(line)
                    continue
                elif line:
                    parts = re.split(r'[\s]+', line.strip())
                    for i in range(0, len(parts), 7):
                        node_index = int(parts[i])
                        position = [float(p) for p in parts[i + 1:i + 4]]
                        orientation = [float(p) for p in parts[i + 4:i + 7]]
                        self.nodes[node_index].positions.append(position)
                        self.nodes[node_index].orientations.append(orientation)

    def print_all_nodes_info(self) -> None:
        """Prints information about all nodes."""
        for node in self.nodes:
            node.print_info()

    def write_to_file(self, filename: str) -> None:
        """
        Writes all data to a file.

        Args:
            filename (str): Name of the file to write the data to.
        """
        with open(filename, 'w') as file:
            file.write("nodes\n")
            for node in self.nodes:
                file.write(f"  {node.index} ")
                file.write(f'"{node.name}" ')
                file.write(f"{node.parent_index}\n")
            file.write("end\nskeleton\n")
            for i in range(0, len(self.nodes[0].positions)):
                file.write(f'  time {i}\n')
                for x, node in enumerate(self.nodes):
                    file.write(f"    {x} ")
                    formatted_positions = [
                        f'{pos:.6f}' for pos in node.positions[i]]
                    file.write(f"{' '.join(formatted_positions)} ")
                    formatted_orientations = [
                        f'{ori:.6f}' for ori in node.orientations[i]]
                    file.write(f"{' '.join(formatted_orientations)}\n")
            file.write("end\n")

    @classmethod
    def get_node_by_index(cls, nodes: List[Node], index: int) -> Node:
        """
        Retrieves a Node object with the specified index.

        Args:
            nodes (List[Node]): List of Node objects.
            index (int): Index of the desired Node.

        Returns:
            Node: Node object with the specified index.
        """
        for node in nodes:
            if node.index == index:
                return node
        raise ValueError(f"Node with index {index} not found.")
