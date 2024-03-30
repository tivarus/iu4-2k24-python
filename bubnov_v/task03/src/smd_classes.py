from dataclasses import dataclass


@dataclass
class PositionNode:
    """
    Represents a position node with its coordinates and rotation.

    Attributes:
        node_id (int): The ID of the node.
        x (float): The x-coordinate of the node.
        y (float): The y-coordinate of the node.
        z (float): The z-coordinate of the node.
        rx (float): The x rotation of the node.
        ry (float): The y rotation of the node.
        rz (float): The z rotation of the node.
    """
    node_id: int
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float

    @classmethod
    def from_line(cls, line: str):
        """
        Creates a PositionNode object from a string line.

        Args:
            line (str): A string containing space-separated values for node properties.

        Returns:
            PositionNode: An instance of PositionNode created from the line.
        """
        parts = line.split()
        return cls(int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]),
                   float(parts[4]), float(parts[5]), float(parts[6]))

    def write_to_file(self, file):
        """
        Writes the PositionNode object's data to a file.

        Args:
            file (file object): The file to write to.
        """
        file.write(f'    {self.node_id} {self.x:.6f} {self.y:.6f} {self.z:.6f} {self.rx:.6f} {self.ry:.6f} {self.rz:.6f}\n')


@dataclass
class Frame:
    """
    Represents a frame containing a collection of PositionNodes.

    Attributes:
        frame_id (int): The ID of the frame.
        positions (list[PositionNode]): The list of PositionNode objects in the frame.
    """
    frame_id: int
    positions: list[PositionNode]

    @classmethod
    def from_lines(cls, frame_id: int, lines: list[str]):
        """
        Creates a Frame object from a frame ID and a list of strings representing position node lines.

        Args:
            frame_id (int): The ID of the frame.
            lines (list[str]): A list of strings representing position node lines.

        Returns:
            Frame: An instance of Frame created from the frame ID and position node lines.
        """
        positions = [PositionNode.from_line(line) for line in lines]
        return cls(frame_id, positions)

    def write_to_file(self, file):
        """
        Writes the Frame object's data to a file.

        Args:
            file (file object): The file to write to.
        """
        file.write(f'  time {self.frame_id}\n')
        for pos in self.positions:
            pos.write_to_file(file)


@dataclass
class Node:
    """
    Represents a node in a scene graph with an ID, name, and parent ID.

    Attributes:
        node_id (int): The ID of the node.
        name (str): The name of the node.
        parent_id (int): The ID of the parent node.
    """
    node_id: int
    name: str
    parent_id: int

    @classmethod
    def from_line(cls, line: str):
        """
        Creates a Node object from a string line.

        Args:
            line (str): A string containing space-separated values for node properties.

        Returns:
            Node: An instance of Node created from the line.
        """
        parts = line.split()
        return cls(int(parts[0]), parts[1], int(parts[2]))

    def write_to_file(self, file):
        """
        Writes the Node object's data to a file.

        Args:
            file (file object): The file to write to.
        """
        file.write(f'  {self.node_id} {self.name} {self.parent_id}\n')
