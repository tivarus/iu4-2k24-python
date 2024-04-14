
filename = 'a_move_walkW.smd'

mode = 'waiting'
nodes = {}
timeframes = []

class Timeframe:
    def __init__(self, time, node, x, y, z, pitch, yaw, roll):
    	self.time = time
    	self.node = node
    	self.x = x
    	self.y = y
    	self.z = z
    	self.pitch = pitch
    	self.yaw = yaw
    	self.roll = roll


with open(filename, 'r') as file:


	for line in file:
		if 'nodes' in line:
 			mode = 'nodes'
		elif 'skeleton' in line:
			mode = 'skeleton'
		elif 'end' in line:
			mode = 'waiting'


		if mode == 'waiting':
			i=0

		#print(mode) 
# блок нодов
		if mode == 'nodes':
			if i == 1:
				splitted = line.split()
				#print(node)
				k, v, a = [word.strip() for word in line.split()]
				nodes[k] = v

			i=1

# блок координат
		if mode == 'skeleton':
			if i == 1:
				if 'time' in line:
					time = line.split()
					k, timestamp = [word.strip() for word in line.split()]
				else:
					splitted = line.split()
					#print(splitted)
					a, b, c, d, e, f, g = [word.strip() for word in line.split()]
					if a == '0':
						timeframe = Timeframe(timestamp,a,0,0,0,0,0,0)
					else:
						timeframe = Timeframe(timestamp,a,b,c,d,e,f,g)
					timeframes.append(timeframe)

					print(a)
			i=1
			
print(nodes)
for timeframe in timeframes:
	print(f"time:{timeframe.time}, node:{timeframe.node}, x:{timeframe.x}, y:{timeframe.y}, z:{timeframe.z}, pitch:{timeframe.pitch}, yaw:{timeframe.yaw}, roll:{timeframe.roll}")

