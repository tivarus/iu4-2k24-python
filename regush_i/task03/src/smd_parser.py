"""A program for parsing smd files."""


class BonePosition:
    """Class to represent the position of a bone."""

    def __init__(self, **kwargs):
        """
        Initialize BonePosition object.

        Parameters:
        - x (float): X-coordinate of the bone position.
        - y (float): Y-coordinate of the bone position.
        - z (float): Z-coordinate of the bone position.
        - angle_x (float): X-axis rotation angle of the bone.
        - angle_y (float): Y-axis rotation angle of the bone.
        - angle_z (float): Z-axis rotation angle of the bone.
        """

        self.x = kwargs.get('x', 0.0)
        self.y = kwargs.get('y', 0.0)
        self.z = kwargs.get('z', 0.0)
        self.angle_x = kwargs.get('angle_x', 0.0)
        self.angle_y = kwargs.get('angle_y', 0.0)
        self.angle_z = kwargs.get('angle_z', 0.0)


class BonesTime:
    """Class to represent a collection of bone positions at a specific time."""

    def __init__(self):
        """Initialize BonesTime object."""
        self.bones = {}

    def append_bone(self, number, position: BonePosition):
        """
        Append a bone position to the collection.

        Parameters:
        - number (int): Number identifying the bone.
        - position (BonePosition): Position of the bone.
        """

        self.bones[number] = position

    def get_bone(self, number) -> BonePosition:
        """
        Retrieve the position of a bone by its number.

        Parameters:
        - number (int): Number identifying the bone.

        Returns:
        BonePosition: Position of the bone if found, None otherwise.
        """
        return self.bones.get(number)


class Animation:
    """Class to represent an animation."""

    def __init__(self, filename: str):
        """
        Initialize Animation object.

        Parameters:
        - filename (str): Path to the animation file.
        """

        try:
            self._filepath = filename
            with open(self._filepath, "rt", encoding="utf-8") as fp:
                lines = fp.readlines()

                nodes_start = next((i for i, line in enumerate(
                    lines) if line.strip() == "nodes"), None)
                nodes_end = next((i for i, line in
                                  enumerate(lines[nodes_start:]) if line.strip() == "end"), None)

                self.nodes = {int(line.strip().split()[0]): line.strip().split('"')[1]
                              for line in lines[nodes_start + 1: nodes_end]}

                skeleton_start = next((i for i, line in enumerate(lines)
                                       if line.strip() == "skeleton"), None)

                self.times = {}
                current_time = 0

                for line in lines[skeleton_start + 1:]:
                    if line.strip().startswith("end"):
                        break
                    if line.strip().startswith("time"):
                        current_time = int(line.strip().split()[1])
                        self.times[current_time] = BonesTime()
                        continue

                    current_position = BonePosition(
                        x=float(line.strip().split()[1]),
                        y=float(line.strip().split()[2]),
                        z=float(line.strip().split()[3]),
                        angle_x=float(line.strip().split()[4]),
                        angle_y=float(line.strip().split()[5]),
                        angle_z=float(line.strip().split()[6]))

                    self.times[current_time].append_bone(number=int(line.strip().split()[0]),
                                                         position=current_position)

        except FileNotFoundError as e:
            print(f"File not found: {e}")

    def get_bone(self, number) -> str:
        """
        Get the name of the bone by its number.

        Parameters:
        - number (int): Number identifying the bone.

        Returns:
        str: Name of the bone if found, None otherwise.
        """

        return self.nodes.get(number)

    def get_time(self, number) -> BonesTime:
        """
        Get the BonesTime object by its number.

        Parameters:
        - number (int): Number identifying the BonesTime object.

        Returns:
        BonesTime: BonesTime object if found, None otherwise.
        """

        return self.times.get(number)
