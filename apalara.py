class Constants:
	INVALID_BOX_NAME = 'Invalid box name'
	INVALID_PARAM = 'Invalid parameter'


def get_box(self, letter):
	box = None
	letter = letter.upper()
	if letter == 'A':
		box = self.A
	elif letter == 'B':
		box = self.B
	elif letter == 'C':
		box = self.C
	elif letter == 'D':
		box = self.D
	elif letter == 'E':
		box = self.E
	elif letter == 'F':
		box = self.F

	return box


class Apalara:
	def __init__(self):
		self.position = [
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0],
			['A', 'B', 'C', 'D', 'E', 'F']
		]
		self.A = [5, 0]
		self.B = [5, 1]
		self.C = [5, 2]
		self.D = [5, 3]
		self.E = [5, 4]
		self.F = [5, 5]
		self.box_names = ['A', 'B', 'C', 'D', 'E', 'F']
		self.robot_arm = [4, 0]

	def __str__(self):
		output = '\n'.join(' '.join(map(str, i)) for i in self.position)
		return output

	"""
	Action proposition over the robot world
	"""

	def move_arm_to(self, x):
		box = x
		if type(x) != list:
			box = get_box(self, x)
		_index_0 = box[0]
		_index_1 = box[1]
		self.robot_arm = [_index_0 - 1, _index_1]
		arm = self.robot_arm
		position_for_print = self.position[arm[0]][arm[1]]
		print('Robot arm at ' + str(position_for_print))

	def arm_grasp(self):
		arm_0 = self.robot_arm[0] + 1
		arm_1 = self.robot_arm[1]
		self.robot_arm = [[arm_0], [arm_1]]
		print('Object grasped')

	def arm_free(self):
		arm = self.robot_arm
		arm_0 = arm[0] - 1
		arm_1 = arm[1]
		self.robot_arm = [arm_0, arm_1]
		print('Arm:' + str(self.robot_arm))

	def arm_place_on_table(self, x):
		# The object must be grasped
		position = self.position
		for i in position[5]:
			if i in self.box_names:
				continue
			else:
				self.move_arm_to(position[5][i])
				self.robot_arm = [5, i]
				self.arm_free()
				print(self.position)
				print('Box placed on table')

	def nop(self):
		pass

	"""
	Relation proposition over the robot world objects
	"""

	def on(self, x, y):
		x, y = str(x).upper(), str(y).upper()

		if (x or y) not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box_x = get_box(self, x)
		box_y = get_box(self, y)
		print('box_x:' + str(box_x))
		print('box_y:' + str(box_y))

		if (box_x[0] != box_y[0]) and abs(box_x[0] - box_y[0]) == 1 and (box_x[1] == box_y[1]):
			return True

		return False

	def clear(self, x):
		x = str(x).upper()
		if x not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box = get_box(self, x)
		truth = True
		print(box)
		for _box in self.box_names:
			_box = (self, _box)
			if _box == box:
				continue
			if (_box[0] != box[0]) and (_box[1] == box[1]):
				truth = False

		return truth

	def on_table(self, x):
		x = str(x).upper()
		if x not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box = get_box(self, x)
		if box[0] != 5:
			return False

		return True

	def on_left(self, x, y):
		x, y = str(x).upper(), str(y).upper()

		if (x or y) not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box_x = get_box(self, x)
		box_y = get_box(self, y)

		if (box_x[0] == box_y[0]) and (box_y[1] - box_x[1] == 1):
			return True

		return False

	def on_right(self, x, y):
		x, y = str(x).upper(), str(y).upper()

		if (x or y) not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box_x = get_box(self, x)
		box_y = get_box(self, y)

		if (box_x[0] == box_y[0]) and (box_x[1] - box_y[1] == 1):
			return True

		return False

	def under(self, x, y):
		x, y = str(x).upper(), str(y).upper()

		if (x or y) not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box_x = get_box(self, x)
		box_y = get_box(self, y)
		if (box_x[0] != box_y[0]) and (box_x[0] - box_y[0] == 1) and (box_x[1] == box_y[1]):
			return True
		return False

	def box(self, pos):
		if type(pos) != list:
			return Constants.INVALID_PARAM

		for _box in self.box_names:
			if get_box(self, _box) == pos:
				return True

		return False

	def grasping(self, x):
		# Do shit here
		if self.robot_arm == get_box(self, x):
			return True
		return False

	"""
	Box move controls
	"""
	def update_position(self, old, new):
		old_index_0 = old[0]
		old_index_1 = old[1]
		new_index_0 = new[0]
		new_index_1 = new[1]
		self.position[new_index_0][new_index_1] = self.position[old_index_0][old_index_1]
		self.position[old_index_0][old_index_1] = 0

	# To move from source to destination
	def move(self, box, destination):
		self.move_arm_to(box)
		self.arm_grasp()
		self.move_arm_to(destination)
		self.arm_free()
		self.update_position(box, destination)

	def put_box_on(self, x, y):
		# Put x on top of y
		x = get_box(self, x)
		y = get_box(self, y)
		y = [y[0] - 1, y[1]]
		self.move(x, y)


obj = Apalara()

obj.put_box_on('e', 'c')
print(obj)
