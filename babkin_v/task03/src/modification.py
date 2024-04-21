from types import Node, Frame


def modificateFile(elems: list[list[Node], list[Frame]]) -> list[list[Node], list[Frame]]:
    frames = elems[1]
    for frame in frames:
        frame.bones[0].position.to_zero()
    return elems
