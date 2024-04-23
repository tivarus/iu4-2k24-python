from structure import Frame, Node


def print_nodes(nodes):
    file_path = 'output.smd'
    with open(file_path, "w") as file:
        print("nodes", file=file)
        for node in nodes:
            print(f"  {node.id} {node.bone_name} {node.parent_id}", file=file)
        print("end", file=file)


def print_frames(frames):
    file_path = 'output.smd'
    with open(file_path, "a") as file:
        print('skeleton', file=file)
        for frame in frames:
            if frame.bone_id == '0':
                print(f"  time {frame.time}", file=file)
            print(f"    {frame.bone_id} {frame.posx} {frame.posy} {frame.posz} "
                  f"{frame.rotx} {frame.roty} {frame.rotz}", file=file)


def smd_parse(filename: str):
    area = 0
    nodes = []
    frames = []

    with open(filename, 'r') as file:
        for line in file:
            if 'nodes' in line:
                area = 1
            if (area == 1) and not ('end' in line) and not ('skeleton' in line) and not (line.startswith("nodes")):
                node = Node(*line.split())
                nodes.append(node)

            if 'skeleton' in line:
                area = 2
            if (area == 2) and not ('end' in line) and (not line.startswith("skeleton")):
                if 'time' in line:
                    unused, value_time = line.split()
                else:
                    line_split = line.split()
                    if line_split[0] == '0':
                        if value_time == '0':
                            start_coord = Frame(value_time, *line_split)
                        frame = Frame(value_time, line_split[0], start_coord.posx, start_coord.posy, start_coord.posz,
                                      start_coord.rotx, start_coord.roty, start_coord.rotz)
                    else:
                        frame = Frame(value_time, *line_split)
                    frames.append(frame)
    print_nodes(nodes)
    print_frames(frames)
