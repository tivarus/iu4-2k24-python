from dataclasses import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    @classmethod
    def from_list(cls, nums: list[float]):
        return cls(*nums)

    def __repr__(self):
        return f"{self.x:.6f} {self.y:.6f} {self.z:.6f}"

    def to_zero(self):
        self.x = 0
        self.y = 0
        self.z = 0


@dataclass
class Node:
    node_id: int
    name: str
    parent_id: int

    @classmethod
    def from_text(cls, text: str):
        tokens = [token.strip() for token in text.split()]
        if len(tokens) != 3:
            raise ValueError(f"Invalid line for node: {text=}")
        try:
            values = [int(tokens[0]), tokens[1], int(tokens[2])]
        except ValueError:
            raise ValueError(f"Cannot create Node from text: {text=}")
        return cls(*values)

    def __repr__(self):
        return f"{self.node_id} {self.name} {self.parent_id}"


@dataclass
class Bone:
    bone_id: int
    position: Vector3
    rotation: Vector3

    @classmethod
    def from_text(cls, text: str):
        tokens_bone = [float(token.strip()) for token in text.split()]
        if len(tokens_bone) != 7:
            raise ValueError(f"Invalid line for bone: {text=}")
        try:
            values = [int(tokens_bone[0]),
                      Vector3.from_list(tokens_bone[1:4]),
                      Vector3.from_list(tokens_bone[4:7])]
        except ValueError:
            raise ValueError(f"Cannot create Bone from text: {text=}")
        return cls(*values)

    def __repr__(self):
        return f"{self.bone_id} {self.position} {self.rotation}"


@dataclass
class Frame:
    frame_time: int
    bones: list[Bone]

    @classmethod
    def from_file(cls, frame_id: int, bones: list[Bone]):
        return cls(frame_id, bones)

    def __repr__(self):
        tokens = [f"  time {self.frame_time}"]
        for bone in self.bones:
            tokens.append(f"    {str(bone)}")
        return "\n".join(tokens)
