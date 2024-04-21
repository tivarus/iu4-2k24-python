def print_console(nodes, timeframes):
    # print(nodes)
    for timeframe in timeframes:
        print(
            f"time:{timeframe.time}, node:{timeframe.node}, x:{timeframe.x}, y:{timeframe.y}, z:{timeframe.z}, pitch:{timeframe.pitch}, yaw:{timeframe.yaw}, roll:{timeframe.roll}")


def print_file(nodes, timeframes):
    output_filename = 'result.smd'
    with open(output_filename, 'w') as file:
        print('nodes', file=file)
        for node in nodes:
            print(
                f"  {node.id} {node.name} {node.coord}", file=file)
        print('end', file=file)
        print('skeleton', file=file)
        for timeframe in timeframes:
            if timeframe.node == '0':
                print(f"  time {timeframe.time}", file=file)
            print(
                f"    {timeframe.node} {timeframe.x} {timeframe.y} {timeframe.z} {timeframe.pitch} {timeframe.yaw} {timeframe.roll}",
                file=file)