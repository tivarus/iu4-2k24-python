from dataclasses import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float


def vector_to_line(vector: Vector3) -> str:
    line = " ".join([str(vector.x), str(vector.y), str(vector.z)])
    return line

@dataclass
class Node:
    node_id: int
    name: str
    parent_id: int

    @classmethod
    def fill_from_line(cls, line):
        line = line.split()
        return cls(int(line[0]), line[1], int(line[2]))


@dataclass
class Bone:
    bone_id: int
    position: Vector3
    rotation: Vector3


def bone_to_line(bone: Bone) -> str:
    line = " ".join([str(bone.bone_id), str(vector_to_line(bone.position)), str(vector_to_line(bone.rotation))])
    return line

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
                nodes.append(Node.fill_from_line(line))


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


def fix_frames(parsed_animation)-> list[Frame]:
    for frame in parsed_animation:
        frame.bones[0].position = Vector3(x=0.000000, y=0.000000, z=0.000000)
    return parsed_animation


def fix_animation(file, parsed_nodes, parsed_frames, overwrite: bool = False):
    with open(file if overwrite else f"new_{file}", 'wt') as file:
        file.writelines("//fixed_animation")
        file.writelines("nodes")
        for node in parsed_nodes:
            line = " ".join([str(node.node_id), node.name, str(node.parent_id)])
            file.writelines(line)
        file.writelines("end")
        file.writelines("skeleton")
        parsed_frames = fix_frames(parsed_frames)
        for frame in parsed_frames:
            line = "time" + str(frame.frame_time)
            file.writelines(line)
            for bone in frame.bones:
                line = bone_to_line(bone)
                file.writelines(line)
        file.writelines("end")
        file.close()


def output_result(parsed_nodes, parsed_animation):
    for node in parsed_nodes:
        print(f"ID: {node.node_id}, Name: {node.name}, Parent ID: {node.parent_id}")
    for frame in parsed_animation:
        print(f"Frame time: {frame.frame_time}")


if __name__ == "__main__":
    filename = "a_move_c4_walkNE.smd"
    parsed_nodes = parse_nodes(filename)
    parsed_animation = parse_animation(filename)
    output_result(parsed_nodes, parsed_animation)
    fix_animation(filename, parsed_nodes, parsed_animation)
