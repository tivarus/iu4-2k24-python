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

    def get_position(self) -> Vector:
        return self._pos

    def set_rotation(self, rot: Angle):
        self._rot = rot

    def get_rotation(self) -> Angle:
        return self._rot

    def pos_to_str(self) -> str:
        return f"{self._pos.x:.6f} {self._pos.y:.6f} {self._pos.z:.6f}"

    def rot_to_str(self) -> str:
        return f"{self._rot.pitch:.6f} {self._rot.yaw:.6f} {self._rot.roll:.6f}"


class SMDParser:

    def __init__(self, file_path: str):
        self.path = file_path
        self.nodes = {}
        with open(file_path, "rt") as file:
            # Find node section
            while not file.readline().startswith("nodes"):
                pass
            for line in file:
                if line.startswith("end"):
                    return
                else:
                    node_info = line.strip().split(" ")
                    node_id = int(node_info[0])
                    node_title = node_info[1]
                    node_parent_id = int(node_info[2])
                    node = Node(id=node_id, title=node_title,
                                parent_id=node_parent_id)
                    self.nodes[node_id] = node

    def frame_from_smd_file(self, frame_num: int) -> List[Node]:
        self.time = frame_num
        with open(self.path, "rt") as file:
            # Find skeleton section
            while not file.readline().startswith("skeleton"):
                pass

            # Find frame with № = frame_num
            while not file.readline().startswith(f"  time {frame_num}"):
                pass

            # Read frame
            for line in file:
                if line.startswith("end") or line.startswith("  time"):
                    break
                node_info = line.strip().split(" ")
                if self.nodes[int(node_info[0])]:
                    node = self.nodes[int(node_info[0])]
                    node.set_position(Vector(float(node_info[1]), float(
                        node_info[2]), float(node_info[3])))
                    node.set_rotation(Angle(float(node_info[4]), float(
                        node_info[5]), float(node_info[6])))

        return self.nodes

    def count_frames(self) -> int:
        with open(self.path, "rt") as file:
            count = 0
            # Find skeleton section
            while not file.readline().startswith("skeleton"):
                pass
            # Count times
            line = file.readline()
            while not line.startswith("end"):
                if line.startswith("  time"):
                    count += 1
                line = file.readline()
            return count

    def print_nodes(self, file_path: str):
        with open(file_path, "a") as f:
            print("nodes", file=f)
            for node_id, node in self.nodes.items():
                print(f"  {node.id} {str(node.title)} {
                      node.parent_id}", file=f)
            print("end\n", file=f)

    def print_frame(self, file_path: str):
        with open(file_path, "a") as f:
            print('skeleton', file=f)

            print(f"  time {self.time}", file=f)
            for node_id, node in self.nodes.items():
                print(f"    {node.id} ", end="", file=f)
                print(node.pos_to_str(), end="", file=f)
                print(" ", end="", file=f)
                print(node.rot_to_str(), end="", file=f)
                print("", file=f)
            print("end\n", file=f)


parser_1 = SMDParser(
    "C:\\OTHER\\учеба\\8 семестр\\python\\iu4-2k24-python\\novikov_t\\task03\\animset_t_anims\\a_move_c4_runS.smd")
parser_1.print_nodes("output.smd")
parser_1.frame_from_smd_file(20)
parser_1.print_frame("output.smd")
