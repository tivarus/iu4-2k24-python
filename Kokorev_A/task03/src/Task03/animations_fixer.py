def fix_animation(file: str, overwrite: bool = False):
    with open(file) as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if "time" in line:
            new_lines = lines[i + 1].split()
            for coordinate in range(5, 7):
                new_lines[coordinate] = "0.000000"
            lines[i + 1] = " ".join(new_lines)

    with open(file if overwrite else f"new_{file}", 'wt') as file:
        file.writelines(lines)


if __name__ == "__main__":
    filename = "a_move_c4_walkNE.smd"
    fix_animation(filename)
