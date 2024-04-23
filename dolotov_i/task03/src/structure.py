from dataclasses import dataclass


@dataclass
class Node:
    id: str
    bone_name: str
    parent_id: str


@dataclass
class Frame:
    time: str
    bone_id: str
    posx: str
    posy: str
    posz: str
    rotx: str
    roty: str
    rotz: str
