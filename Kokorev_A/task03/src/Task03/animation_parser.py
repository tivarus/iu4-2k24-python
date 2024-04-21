from dataclasses import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float


@dataclass
class Node:
    node_id: int
    name: str
    parent_id: int


@dataclass
class Bone:
    bone_id: int
    position: Vector3
    rotation: Vector3


@dataclass
class Frame:
    frame_time: int
    bones: list[Bone]


def parse_nodes(file: str) -> list[Node]:
    nodes = []
    parsing = False
    with open(file, "rt") as file:
        for line in file:
            if "nodes" in line:
                parsing = True
                continue
            elif not parsing:
                continue
            if parsing:
                if "end" in line:
                    return nodes
                line = line.split()
                node_id = int(line[0])
                name = line[1]
                parent_id = int(line[2])
                nodes.append(Node(node_id, name, parent_id))


def parse_animation(file: str) -> list[Frame]:
    frames = []
    current_frame_bones = []
    current_frame_time = None
    parsing = False
    with open(file, "rt") as file:
        for line in file:
            if "skeleton" in line:
                parsing = True
                continue
            elif not parsing:
                continue
            if parsing:
                if "end" in line:
                    frames.append(Frame(frame_time=current_frame_time, bones=current_frame_bones))
                    return frames
                if "time" in line:
                    if current_frame_time is None:
                        current_frame_time = int(line.split()[1])
                        continue
                    frames.append(Frame(frame_time=current_frame_time, bones=current_frame_bones))
                    current_frame_bones = []
                    current_frame_time = int(line.split()[1])
                else:
                    line = line.split()
                    x_pos, y_pos, z_pos, x_rot, y_rot, z_rot = map(float, line[1:])
                    bone = Bone(bone_id=int(line[0]),
                                position=Vector3(x=x_pos, y=y_pos, z=z_pos),
                                rotation=Vector3(x=x_rot, y=y_rot, z=z_rot))
                    current_frame_bones.append(bone)


def show_result(parsed_nodes, parsed_animation):
    for node in parsed_nodes:
        print(f"ID: {node.node_id}, Name: {node.name}, Parent ID: {node.parent_id}")
    for frame in parsed_animation:
        print(f"Frame time: {frame.frame_time}")


if __name__ == "__main__":
    filename = "a_move_c4_walkNE.smd"
    parsed_nodes = parse_nodes(filename)
    parsed_animation = parse_animation(filename)
    show_result(parsed_nodes, parsed_animation)
