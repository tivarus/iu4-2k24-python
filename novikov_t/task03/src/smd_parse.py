from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Vector:
    x: float
    y: float
    z: float


@dataclass
class Angle:
    pitch: float
    yaw: float
    roll: float


@dataclass
class Node:
    id: int
    title: str
    parent_id: int
    _pos: Optional[Vector] = None
    _rot: Optional[Angle] = None

    def set_position(self, pos: Vector):
        self._pos = pos

    def set_rotation(self, rot: Angle):
        self._rot = rot

    def print_pos(self):
        print(f"{self._pos.x:.6f} {self._pos.y:.6f} {self._pos.z:.6f}", end="")

    def print_rot(self):
        print(f"{self._rot.pitch:.6f} {self._rot.yaw:.6f} {
              self._rot.roll:.6f}", end="")


class SMDParser:

    def __init__(self, file_path: str):
        self.path = file_path
        self.nodes = {}
        with open(file_path, "r") as file:
            # Find node section
            while not (file.readline().startswith("nodes")):
                pass
            for line in file:
                if not (line.startswith("end")):
                    node_info = line.strip().split(' ')
                    node_id = int(node_info[0])
                    node_title = node_info[1]
                    node_parent_id = int(node_info[2])
                    node = Node(id=node_id, title=node_title,
                                parent_id=node_parent_id)
                    self.nodes[node_id] = node
                else:
                    return

    def frame_from_smd_file(self, frame_num: int) -> List[Node]:
        self.time = frame_num
        with open(self.path, "r") as file:
            # Find skeleton section
            while not (file.readline().startswith("skeleton")):
                pass

            # Find frame with № = frame_num
            while not (file.readline().startswith(f"  time {frame_num}")):
                pass

            # Read frame
            for line in file:
                if line.startswith("end") or line.startswith("  time"):
                    break
                else:
                    node_info = line.strip().split(" ")
                    node_id = int(node_info[0])
                    node_pos = Vector(float(node_info[1]), float(
                        node_info[2]), float(node_info[3]))
                    node_rot = Angle(float(node_info[4]), float(
                        node_info[5]), float(node_info[6]))
                    if self.nodes[node_id]:
                        node = self.nodes[node_id]
                        node.set_position(node_pos)
                        node.set_rotation(node_rot)

        return self.nodes

    def count_frames(self) -> int:
        with open(self.path, "r") as file:
            cnt = 0
            # Find skeleton section
            while not (file.readline().startswith("skeleton")):
                pass
            # Count times
            line = file.readline()
            while not (line.startswith("end")):
                if line.startswith("  time"):
                    cnt += 1
                line = file.readline()
            return cnt

    def print_nodes(self):
        print("nodes")
        for node_id, node in self.nodes.items():
            print(f"  {node.id} {str(node.title)} {node.parent_id}")

    def print_frame(self):
        print('skeleton')

        print(f"  time {self.time}")
        for node_id, node in self.nodes.items():
            print(f"    {node.id} ", end="")
            node.print_pos()
            print(" ", end="")
            node.print_rot()
            print()
