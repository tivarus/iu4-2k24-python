def modificateFile(elems: list):
    frames = elems[1]
    for frame in frames:
        frame.bones[0].position.to_zero()
    return elems
