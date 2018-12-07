class Constants:
	INVALID_BOX_NAME = 'Invalid box name'
	INVALID_PARAM = 'Invalid parameter'


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

	"""
	Action proposition over the robot world
	"""

	def move_arm_to(self, x):
		box = x
		if type(x) != list:
			box = self.get_box(x)
		_index_0 = box[0]
		_index_1 = box[1]
		self.robot_arm = [_index_0 - 1, _index_1]

	def arm_grasp(self):
		arm_0 = self.robot_arm[0] + 1
		arm_1 = self.robot_arm[1]
		self.robot_arm = [[arm_0], [arm_1]]

	def arm_free(self):
		arm = self.robot_arm
		arm_0 = arm[0] - 1
		arm_1 = arm[1]
		self.robot_arm = [arm_0, arm_1]

	def arm_place_on_table(self, x):
		position = self.position
		for index, i in enumerate(position[5], start=0):
			if str(i) in self.box_names:
				continue
			else:
				x_ = self.get_box(x)
				self.robot_arm = [5, index]
				self.move(x_, self.robot_arm)
				self.update_position(x_, self.robot_arm)
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

		box_x = self.get_box(x)
		box_y = self.get_box(y)

		if (box_x[0] != box_y[0]) and abs(box_x[0] - box_y[0]) == 1 and (box_x[1] == box_y[1]):
			return True

		return False

	def clear(self, x):
		x = str(x).upper()
		if x not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box = self.get_box(x)
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

		box = self.get_box(x)
		if box[0] != 5:
			return False

		return True

	def on_left(self, x, y):
		x, y = str(x).upper(), str(y).upper()

		if (x or y) not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box_x = self.get_box(x)
		box_y = self.get_box(y)

		if (box_x[0] == box_y[0]) and (box_y[1] - box_x[1] == 1):
			return True

		return False

	def on_right(self, x, y):
		x, y = str(x).upper(), str(y).upper()

		if (x or y) not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box_x = self.get_box(x)
		box_y = self.get_box(y)

		if (box_x[0] == box_y[0]) and (box_x[1] - box_y[1] == 1):
			return True

		return False

	def under(self, x, y):
		x, y = str(x).upper(), str(y).upper()

		if (x or y) not in self.box_names:
			return Constants.INVALID_BOX_NAME

		box_x = self.get_box(x)
		box_y = self.get_box(y)
		if (box_x[0] != box_y[0]) and (box_x[0] - box_y[0] == 1) and (box_x[1] == box_y[1]):
			return True
		return False

	def box(self, pos):
		if type(pos) != list:
			return Constants.INVALID_PARAM

		for _box in self.box_names:
			if self.get_box(_box) == pos:
				return True

		return False

	def grasping(self, x):
		# Do shit here
		if self.robot_arm == self.get_box(x):
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
		# new_position_name = self.position[new[0]][new[1]]
		# self.update_box(new_position_name, [old_index_0, old_index_1])

	def swap_position_and_update(self, old, new):
		old_index_0, old_index_1 = old[0], old[1]
		new_index_0, new_index_1 = new[0], new[1]
		box_position_old = self.position[old_index_0][old_index_1]
		box_position_new = self.position[new_index_0][new_index_1]
		self.position[new_index_0][new_index_1] = box_position_old
		self.position[old_index_0][old_index_1] = box_position_new
		# new_position_name = self.position[new[0]][new[1]]
		# old_position_name = self.position[old[0]][old[1]]
		# self.update_box(old_position_name, [new_index_0, new_index_1])
		# self.update_box(new_position_name, [old_index_0, old_index_1])

	def update_box(self, x, value):
		x_ = x.upper()
		if x_ == 'A':
			self.A = value
		elif x_ == 'B':
			self.B = value
		elif x_ == 'C':
			self.C = value
		elif x_ == 'D':
			self.D = value
		elif x_ == 'E':
			self.E = value
		elif x_ == 'F':
			self.F = value

	# To move from source to destination
	def move(self, box, destination):
		self.move_arm_to(box)
		self.arm_grasp()
		self.move_arm_to(destination)
		self.arm_free()
		self.update_position(box, destination)

	def put_box_on(self, x, y):
		# Put x on top of y
		_x = self.get_box(x)
		_y = self.get_box(y)
		_y = [_y[0] - 1, _y[1]]
		self.move(_x, _y)
		self.update_box(x, _y)

	def swap_boxes(self, x, y):
		x_ = self.get_box(x)
		y_ = self.get_box(y)
		self.swap_position_and_update(x_, y_)

	"""
	Other
	"""

	def can_arm_grasp(self, x):
		box = self.get_box(x)
		if self.position[box[0] - 1][box[1]] == 0:
			return True
		return False

	def is_box_in_middle(self, x):
		box = self.get_box(x)
		if box[0] == 5:
			return False
		elif self.position[box[0] - 1][box[1]] != 0 and self.position[box[0] + 1][box[1]] != 0:
			return True
		return False

	def is_box_under_another(self, x):
		box = self.get_box(x)
		if self.position[box[0] - 1][box[1]] != 0:
			return True
		return False

	def is_box_on_table(self, x):
		box = self.get_box(x)
		if box[0] == 5:
			return True
		return False

	def get_box_position(self, x):
		x = x.upper()
		box = self.get_box(x)
		if box[0] == 5:
			return str(x) + " is on the table"
		else:
			box_under = [box[0] + 1, box[1]]
			for i in self.box_names:
				if self.get_box(i) == box_under:
					return "Box " + str(x) + " is on top of box " + str(i)

	def get_neighbours(self, x):
		x = x.upper()
		box = self.get_box(x)
		neighbours = []
		for each_box in self.box_names:
			each__box = self.get_box(each_box)
			if each__box[0] == box[0] and (abs(each__box[1] - box[1]) == 1):
				neighbours.append(each_box)

		if len(neighbours) == 1:
			output = "The neighbour of " + str(x) + " is " + neighbours[0]
		elif len(neighbours) == 2:
			output = "The neighbours of " + str(x) + " are " + neighbours[0] + " and " + neighbours[1]
		else:
			output = str(x) + " has no neighbours"

		return output


"""
===========================================================================================
"""


def get_command():
	instruction = input('Enter command or query below:\n').lower()
	return instruction


def handle_action_interactions(self, command):
	if 'swap boxes' in command:
		if len(command) != 18:
			print('Invalid command')

		box_1 = command[-7]
		box_2 = command[-1]
		self.swap_boxes(box_1, box_2)
		print(self)

	elif 'place box' in command and 'on the table' not in command and 'under box' not in command:
		if len(command) != 20:
			print('Invalid command')

		box_top_name = command[10]
		box_under_name = command[-1]
		self.put_box_on(box_top_name, box_under_name)
		print(self)

	elif 'place box' in command and 'under box' in command:
		if len(command) != 23:
			print('Invalid command')

		box_under_name = command[10]
		box_top_name = command[-1].upper()
		box_top = self.get_box(box_top_name)

		if self.is_box_under_another(box_top_name):
			other_box = self.position[box_top[0] - 1][box_top[1]]
			responses = {
				"resp": "This is not possible \n",
				"why": "Because box " + str(box_top_name) + " is under box " + str(other_box) + "\n",
				"and_then": "I cannot remove a box under another box \n",
				"why_again": "The stacked boxes will fall \n"
			}
			resp = input(responses['resp'])

			if 'why' in resp.lower():
				resp = input(responses['why'])
				if "and then" in resp.lower():
					resp = input(responses['and_then'])
					if "why" in resp.lower():
						print(responses['why_again'])

		else:
			self.put_box_on(box_top_name, box_under_name)
			print(self)

	elif 'place box' in command and 'on the table' in command:
		if len(command) != 24:
			print('Invalid command')

		box_for_table = command[10]
		self.arm_place_on_table(box_for_table)
		print(self)

	elif 'generate the' in command:
		if 'three' in command:
			self.put_box_on('B', 'A')
			self.put_box_on('C', 'B')
			self.put_box_on('E', 'D')
			self.put_box_on('F', 'E')
			print(self)

		if 'six' in command:
			self.put_box_on('B', 'A')
			self.put_box_on('C', 'B')
			self.put_box_on('D', 'C')
			self.put_box_on('E', 'D')
			self.put_box_on('F', 'E')
			print(self)

	elif 'stack' in command:
		if len(command) != 48:
			print('Invalid command')

		base_box = command[-1]
		first_box = command[6]
		second_box = command[9]
		third_box = command[12]
		fourth_box = command[19]

		self.put_box_on(fourth_box, base_box)
		self.put_box_on(third_box, fourth_box)
		self.put_box_on(second_box, third_box)
		self.put_box_on(first_box, second_box)
		print(self)

	elif 'grasp' in command:
		box_name = command[-2]
		box = self.get_box(box_name)
		if self.is_box_under_another(box_name):
			other_box = self.position[box[0] - 1][box[1]]
			responses = {
				"resp": "This is not possible \n",
				"why": "Because box " + str(box_name) + " is under box " + str(other_box) + "\n",
				"and_then": "I cannot remove a box under another box \n",
				"why_again": "The stacked boxes will fall \n"
			}
			resp = input(responses['resp'])
			if 'why' in resp.lower():
				resp = input(responses['why'])
				if "and then" in resp.lower():
					resp = input(responses['and_then'])
					if "why" in resp.lower():
						print(responses['why_again'])

		else:
			self.move_arm_to(box)
			self.arm_grasp()
			print('Grasped')

	elif 'where is' in command:
		if command[-1] == '?':
			box_name = command[-2]
		else:
			box_name = command[-1]
		location = self.get_box_position(box_name)
		print(location)

	elif 'is box' in command and 'on the table' in command:
		box_name = command[7]
		if self.is_box_on_table(box_name):
			print('Yes, box ' + str(box_name) + ' is on the table')
		else:
			print(self.get_box_position(box_name))

	elif 'what boxes are' in command and 'neighbour' in command:
		if command[-1] == '?':
			box_name = command[-2]
		else:
			box_name = command[-1]
		print(self.get_neighbours(box_name))

	else:
		print('Invalid input')
		exit()


def run_apalara(self):
	command = get_command()
	if command.lower() == 'exit':
		return exit()

	handle_action_interactions(self, command)
	run_apalara(self)


print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
print('Welcome to Apalara!')
print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')

print('Below is the default robot world')
apalara = Apalara()
print(apalara)
print('--------------------------------\n')
print('Kindly enter "exit" to exit your session')
run_apalara(apalara)
