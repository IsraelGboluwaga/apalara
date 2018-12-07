from apalara import Apalara


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
		print('Ode bi')
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
			if resp.lower() == 'why':
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
run_apalara(apalara)
