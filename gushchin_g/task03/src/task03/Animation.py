import re
import io

from typing import List
from typing import TextIO
from typing import Union


class Animation:
    version: int = 0
    __nodes: List[Union[int, str, int]] = []  # id name value
    __steps: List[
        Union[
            int,  # time
            List[
                Union[int, List[float]]  # id, values
            ],
        ]
    ] = []  # time [id vectors x6]

    def __init__(
        self,
        version: int = None,
        nodes: List[Union[int, str, int]] = None,
        steps: List[Union[int, List[Union[int, List[float]]]]] = None,
    ):
        if version is None or nodes is None or steps is None:
            self.__clear()
            return

        self.version = version
        self.__nodes = nodes
        self.__steps = steps
        return

    def __eq__(self, other) -> bool:
        if not isinstance(other, Animation):
            return False
        return (
            self.version == other.version
            and self.__nodes == other.__nodes
            and self.__steps == other.__steps
        )

    def __clear(self):
        self.version = -1
        self.__nodes = []
        self.__steps = []

    def __from_stream_or_str(self, stream, is_str: bool):
        self.__clear()

        pars_nodes: bool = False
        pars_skeleton: bool = False

        line_number: int = 0
        frame_number: int = -1

        lines = stream.splitlines() if is_str else stream.readlines()

        for line in lines:
            line_number += 1

            if pars_nodes:
                pars_nodes = self.__parsNode(line, line_number)
                continue
            if pars_skeleton:
                (pars_skeleton, frame_number) = self.__parsSkeletone(
                    line, line_number, frame_number
                )
                continue

            if self.__isCommnet(line, line_number):
                continue

            if "version" in line:
                values: List[int] = list(map(int, re.findall(r"\d+", line)))
                if len(values) != 1:
                    raise NameError(
                        f"Line: {line_number} is invalid. The version is invalid"
                    )
                self.version = values[0]
                continue

            if "nodes" in line:
                pars_nodes = True
                continue

            if "skeleton" in line:
                pars_skeleton = True
                continue

        self.__isValid()
        return

    def __isValid(self):
        for node in self.__nodes:
            matches: List = [x for x in self.__nodes if x[0] == node[0]]
            if len(matches) != 1:
                raise NameError(f"Nodes has dublicated id: {matches[0][0]}")

        for step in self.__steps:
            for node in self.__nodes:
                matches: List = [x for x in step[1] if x[0] == node[0]]
                if len(matches) < 1:
                    raise NameError(f"Frame: {step[0]} has an undefined id: {node[0]}")
                if len(matches) > 1:
                    raise NameError(f"Frame: {step[0]} has dublicated ids: {node[0]}")
        return

    def __isCommnet(self, line: str, line_number: int) -> bool:
        first_dash: bool = False
        for symbol in line:
            if first_dash is True:
                if symbol != "/":
                    raise NameError(f"Line {line_number} is invalid")
                return True
            if symbol == "/":
                first_dash = True

        return False

    def __parsNode(self, line: str, line_number: int) -> int:
        if "end" in line:
            return False

        values: List[int] = list(map(int, re.findall(r" -?\d+", line)))
        names: List[str] = list(map(str, re.findall(r'"([^"]*)"', line)))

        if len(values) != 2 or len(names) != 1:
            raise NameError(f"Line: {line_number} not a node.")

        self.__nodes.append((values[0], names[0], values[1]))

        return True

    def __parsSkeletone(
        self, line: str, line_number: int, frame_number: int
    ) -> Union[bool, int]:
        if self.__isCommnet(line, line_number):
            return (True, frame_number)

        if "end" in line:
            return (False, frame_number)

        if "time" in line:
            frame_number += 1

            values: List[int] = list(map(int, re.findall(r"\d+", line)))
            if len(values) != 1:
                raise NameError(
                    f"Line: {line_number} is invalid. The time mark is invalid"
                )
            if values[0] != frame_number:
                missed_or_dublicated = (
                    "missed" if values[0] > frame_number else "dublicated"
                )
                raise NameError(
                    f"Line: {line_number} is invalid. Some time marks was {missed_or_dublicated}"
                )

            self.__steps.append((frame_number, []))
            return (True, frame_number)

        values: List[float] = list(map(float, re.findall(r"[-+]?(?:\d*\.*\d+)", line)))
        if len(values) != 7:
            raise NameError(f"Line: {line_number} is invalid. The frame is invalide")

        id = values[0]
        data = [values[1], values[2], values[3], values[4], values[5], values[6]]
        self.__steps[frame_number][1].append((id, data))
        return (True, frame_number)

    @property
    def nodes(self) -> List[Union[int, str, int]]:
        return self.__nodes

    def step(self, step_number: int) -> Union[int, List[Union[int, List[float]]]]:
        if step_number >= len(self.__steps):
            raise NameError(
                f"element {step_number} out of range: [0 : {len(self.__steps) - 1}]"
            )
        return self.__steps[step_number]

    @property
    def steps(self) -> List[Union[int, List[Union[int, List[float]]]]]:
        return self.__steps

    def from_str(self, text: str):
        if not isinstance(text, str):
            raise NameError(f"text is no a {type(str)}. Actual type: {type(text)}")
        self.__from_stream_or_str(text, True)

    def from_stream(self, stream: io.TextIOWrapper):
        if not isinstance(stream, io.TextIOWrapper):
            raise NameError(
                f"stream is no a {type(io.TextIOWrapper)}. Actual type: {type(stream)}"
            )
        self.__from_stream_or_str(stream, False)

    def to_str(self) -> str:
        output: str = ""
        output = f"{output}version {self.version}\n"
        output = f"{output}nodes\n"

        for node in self.__nodes:
            output = f'{output}  {node[0]} "{node[1]}" {node[2]}\n'
        output = f"{output}end\n"
        output = f"{output}skeleton\n"

        for step in self.__steps:
            output = f"{output}  time {step[0]}\n"
            for data in step[1]:
                output = f"{output}    {int(data[0])}"
                for val in data[1]:
                    output = f"{output} {'{0:.6f}'.format(val)}"
                output = f"{output}\n"
        output = f"{output}end\n"

        return output

    def to_stream(self, stream: TextIO) -> TextIO:
        stream.write(f"version {self.version}\n")
        stream.write("nodes\n")

        for node in self.__nodes:
            stream.write(f'  {node[0]} "{node[1]}" {node[2]}\n')
        stream.write("end\n")
        stream.write("skeleton\n")

        for step in self.__steps:
            stream.write(f"  time {step[0]}\n")
            for data in step[1]:
                stream.write(f"    {data[0]}")
                for val in data[1]:
                    stream.write(f" {'{0:.6f}'.format(val)}")
                stream.write("\n")
        stream.write("end\n")
        print(stream.read())

        return stream


def main():
    print("No errors")


if __name__ == "__main__":
    main()
