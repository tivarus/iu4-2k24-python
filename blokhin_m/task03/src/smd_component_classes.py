from dataclasses import dataclass


@dataclass
class PositionNode:
    node_id: int
    x: float
    y: float
    z: float
    rx: float
    ry: float
    rz: float

    @classmethod
    def create_from_line(cls, line: str):
        parts = line.split()
        return cls(int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]),
                   float(parts[4]), float(parts[5]), float(parts[6]))

    def write_to_file(self, file):
        print(f'    {self.node_id} {self.x:.6f} {self.y:.6f} {self.z:.6f} {self.rx:.6f} {self.ry:.6f} {self.rz:.6f}', file=file)


@dataclass
class Frame:
    frame_id: int
    positions: list[PositionNode]

    @classmethod
    def create_frame(cls, frame_id: int, lines: list[str]):
        positions = [PositionNode.create_from_line(line) for line in lines]
        return cls(frame_id, positions)

    def write_to_file(self, file):
        print(f'  time {self.frame_id}', file=file)
        for pos in self.positions:
            pos.write_to_file(file)

    def modify_positions(self):
        if self.positions:
            pos = self.positions[0]
            pos.x = 0.0
            pos.y = 0.0


@dataclass
class Node:
    node_id: int
    name: str
    parent_id: int

    @classmethod
    def create_from_line(cls, line: str):
        parts = line.split()
        return cls(int(parts[0]), parts[1], int(parts[2]))

    def write_to_file(self, file):
        print(f'  {self.node_id} {self.name} {self.parent_id}', file=file)
