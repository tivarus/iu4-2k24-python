def generateSmd(elems: list):
    with open("smd_filik3.smd", "w") as file:
        nodes = elems[0]
        frames = elems[1]

        file.write("// Created by Crowbar 0.741\n")
        file.write("version 1\n")
        file.write("nodes\n")
        for node in nodes:
            file.write(f"  {str(node)}\n")
        file.write("end\n")
        file.write("skeleton\n")
        for frame in frames:
            file.write(f"{str(frame)}\n")
        file.write("end\n")
