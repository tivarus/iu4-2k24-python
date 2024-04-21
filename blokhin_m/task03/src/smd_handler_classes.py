import os
from typing import TextIO
from smd_component_classes import Node, Frame


class SMDParser:
    @staticmethod
    def parse(fl: str, dir_path: str = os.getcwd()) -> tuple[str, str, list[Node], list[Frame]]:
        fl_path = os.path.join(dir_path, fl)
        try:
            with open(fl_path, 'rt') as smd:
                nodes, frames = SMDParser.read(smd)
                return fl, dir_path, nodes, frames
        except FileNotFoundError:
            return fl, dir_path, [], []

    @staticmethod
    def read(smd: TextIO) -> tuple[list[Node], list[Frame]]:
        nodes = []
        frames = []
        section = None
        positions = []
        frame_id = None
        for line in smd:
            line = line.strip()
            if line.startswith('nodes'):
                section = 'nodes'
            elif line.startswith('skeleton'):
                section = 'skeleton'
            elif line.startswith('end'):
                section = None
            elif section == 'nodes':
                nodes.append(Node.create_from_line(line))
            elif section == 'skeleton':
                if line.startswith('time'):
                    frame_id = int(line.split()[1])
                    positions = []
                else:
                    positions.append(line)
                    if len(positions) == len(nodes):
                        frames.append(Frame.create_frame(frame_id, positions))

        return nodes, frames


class SMDModifier:
    @staticmethod
    def create_new(smd_file: tuple[str, str, list[Node], list[Frame]]) -> None:
        fl, dir_path, nodes, frames = smd_file
        for frame in frames:
            frame.modify_positions()

        new_fl = f'new_{fl}'
        new_dir_path = os.path.join(dir_path, 'modified')
        fl_path = os.path.join(new_dir_path, new_fl)
        os.makedirs(new_dir_path, exist_ok=True)

        SMDModifier.output(fl_path, nodes, frames)

    @staticmethod
    def output(fl: str, nodes: list[Node], frames: list[Frame]) -> None:
        with open(fl, 'wt', encoding='utf-8') as new_smd:
            print('Version 2', file=new_smd)
            print('nodes', file=new_smd)
            for node in nodes:
                node.write_to_file(new_smd)
            print('end', file=new_smd)
            print('skeleton', file=new_smd)
            for frame in frames:
                frame.write_to_file(file=new_smd)
            print('end', file=new_smd)
