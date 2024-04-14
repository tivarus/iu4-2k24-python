from types import Node, Frame, Bone


def parse_nodes(filepath: str) -> list[Node]:
    nodes = []
    flag_parsing = False
    with open(filepath, "rt") as fp:
        for line in fp.readlines():
            if flag_parsing:
                if "end" in line:
                    return nodes
                nodes.append(Node.from_text(line.strip()))
            elif "nodes" in line:
                flag_parsing = True
    raise ValueError("Did not met an end")


def parse_frames(filepath: str) -> list[Frame]:
    frames = []
    frame_id = None
    flag_parsing = False
    bones = []
    with open(filepath, "rt") as fp:
        for line in fp.readlines():
            if flag_parsing:
                if "end" in line:
                    frames.append(Frame.from_file(frame_id, bones))
                    return frames
                elif "time" in line:
                    if frame_id is not None:
                        frames.append(Frame.from_file(frame_id, bones))
                    bones = []
                    try:
                        frame_id = int(line.strip().split()[1])
                    except ValueError:
                        raise NameError("Wrong type of frame_id: {frame_id=}")
                else:
                    bones.append(Bone.from_text(line.strip()))
            elif "skeleton" in line:
                flag_parsing = True
    raise ValueError("Did not met an end")


def parse_file(filepath: str):
    nodes = parse_nodes(filepath)
    frames = parse_frames(filepath)
    return [nodes, frames]
