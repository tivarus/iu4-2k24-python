from dataclasses import dataclass
from lib import print_file


def main():
    filename = 'a_move_walkW.smd'
    mode = 'waiting'
    nodes = []
    timeframes = []
    trigger_first_point = 0

    @dataclass
    class Timeframe:
        time: str
        node: str
        x: str
        y: str
        z: str
        pitch: str
        yaw: str
        roll: str

    @dataclass
    class Node:
        id: str
        name: str
        coord: str

    with open(filename, 'r') as file:
        for line in file:
            if 'nodes' in line:
                mode = 'nodes'
            elif 'skeleton' in line:
                mode = 'skeleton'
            elif 'end' in line:
                mode = 'waiting'
            if mode == 'waiting':
                i = 0
            # блок нодов
            if mode == 'nodes':
                if i == 1:
                    splitted = line.split()
                    # print(node)
                    tokens = [word.strip() for word in line.split()]
                    node = Node(*tokens)
                    nodes.append(node)
                i = 1
            # блок координат
            if mode == 'skeleton':
                if i == 1:
                    if 'time' in line:
                        time = line.split()
                        k, timestamp = [word.strip() for word in line.split()]
                    else:
                        splitted = line.split()
                        tokens = [word.strip() for word in splitted]
                        if tokens[0] == '0':
                            if trigger_first_point == 0:
                                first_point = Timeframe(timestamp, *tokens)
                                trigger_first_point = 1
                            timeframe = first_point
                        else:
                            timeframe = Timeframe(timestamp, *tokens)
                        timeframes.append(timeframe)
                i = 1
    print_file(nodes, timeframes)


main()
