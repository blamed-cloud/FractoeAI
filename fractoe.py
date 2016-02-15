#!/usr/bin/python
#fractal_tic_tac_toe.py
###USAGE### fractal_tic_tac_toe.py [-w] [-f <filename>] | [-l] [-f <filename>] [-p <num_players>] [-q] [-h] ; sms=N ; $#=0-3
import prgm_lib
import sys
import re
import random
re_mk=prgm_lib.flag_re_mk

DEFAULT_GAME_FILE = '/home/denver/lib/fractoe_game'
TEMP_GAME_FILE = '/home/denver/lib/fractoe_game_temp'

UPPER_BOUND = 100
LOWER_BOUND = -100

def coor_split(num):
	col = num % 3
	row = (num - col) / 3
	return [row,col]
	
def coor_splice(row,col):
	return row*3 + col

class Tictactoe:
	def __init__(self):
		self.grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
		self.winner = " "

	def load(self, board_state):
		for num in range(9): 
			col = num % 3
			row = (num - (num % 3))/3
			self.grid[row][col] = board_state[num]
		self.check_for_winner()
		
	def __str__(self):
		value = ""
		for row in range(3):
			for col in range(3):
				value += self.grid[row][col]
		return value
		
	def __repr__(self):
		return self.__str__()
		
	def set_square(self,row,col,player):
		self.grid[row][col] = player
		self.check_for_winner()
		
	def get_square(self,row,col):
		return self.grid[row][col]
		
	def get_row(self,row):
		string = ' '
		for y in range(len(self.grid)):
			string += self.grid[row][y] + " | "
		return string[:-2]
		
	def check_for_winner(self):
		for x in range(len(self.grid)):
			if self.grid[x][0] == self.grid[x][1] == self.grid[x][2] != " ":
				self.winner = self.grid[x][0]
			if self.grid[0][x] == self.grid[1][x] == self.grid[2][x] != " ":
				self.winner = self.grid[0][x]
		if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != " ":
			self.winner = self.grid[1][1]
		if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != " ":
			self.winner = self.grid[1][1]
		if self.winner == " ":
			if self.is_full():
				self.winner = "C"
		return self.winner

	def is_full(self):
		full = True
		for row in range(3):
			for col in range(3):
				if self.grid[row][col] == " ":
					full = False
		return full

	def is_finished(self):
		return self.winner != " "

	def get_winner(self):
		value = -1
		if self.winner == "X":
			value = 1
		elif self.winner == "O":
			value = 2
		elif self.winner == "C":
			value = 0
		return value	
	
	def opg(self):
		for x in range(len(self.grid)):
			string = ' '
			for y in range(len(self.grid[x])):
				string += self.grid[x][y] + " | "
			print string[:-2]
			string2 = ''
			if x != 2:
				for var in range(len(string)-2):
					string2 += "-"
				print string2
	

class Board:
	def __init__(self, player1, player2, filename = DEFAULT_GAME_FILE, save_history = False, to_load = False, be_quiet = False):
		self.grid = [[Tictactoe(), Tictactoe(), Tictactoe()], [Tictactoe(), Tictactoe(), Tictactoe()], [Tictactoe(), Tictactoe(), Tictactoe()]]
		self.turn = 0
		self.current_box = -1
		self.current_row = -1
		self.current_col = -1
		self.boards_won = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
		self.winner = -1
		self.player_token = [" ","X","O"]
		self.players = ['', player1, player2]
		self.escapes = [":w", ":q", ":wq", ":r"]
		self.game_file = filename
		self.quiet = be_quiet
		self.history = save_history
		if self.history and not to_load:
			temp = open(self.game_file, 'w')	### erase contents of the game file
			temp.close()				###
		if to_load:
			self.load_state_from_file(self.game_file)
	
	def load_state_from_string(self, state_string):
		class_data = re.split(";", state_string)
		for num in range(9):
			col = num % 3
			row = (num - (num % 3))/3
			self.grid[row][col].load(class_data[num])
			if self.grid[row][col].is_finished():
				self.boards_won[num] = self.grid[row][col].get_winner()
		self.turn = int(class_data[9])
		self.current_box = int(class_data[10])
		if self.current_box != -1:
			x = self.current_box
			self.current_col = x % 3
			self.current_row = (x - (x % 3))/3
		else:
			self.current_row = -1
			self.current_col = -1
		self.check_for_winner()
	
	def load_state_from_file(self, file_name = DEFAULT_GAME_FILE):
		FILE = open(file_name, 'r')
		source = FILE.read()
		FILE.close()
		turn_list = re.split("\n+", source)
		turn_list = turn_list[:-1]
		last_turn = turn_list[-1]
		self.load_state_from_string(last_turn)
		
	def get_current_box(self):
		return self.current_box
		
	def get_board_string(self,row,col):
		return str(self.grid[row][col])
	
	def __str__(self):
		value = ""
		for row in range(3):
			for col in range(3):
				value += str(self.grid[row][col]) + ';'
		value += str(self.turn) + ';'
		value += str(self.current_box)
		return value
		
	def __repr__(self):
		return self.__str__()
	
	def save_state(self, file_name = DEFAULT_GAME_FILE):
		if not self.history:
			output = open(file_name, 'w')
		else:
			output = open(file_name, 'a')
		output.write(self.__str__() + '\n')
		output.close()	
		
	def get_turn(self):
		return self.turn
	
	def is_human_turn(self):
		return self.players[self.get_player()].is_human()
	
	def current_player(self):
		return self.players[self.get_player()]
	
	def handle_escape(self, code):
		if code == ":w":
			self.save_state(self.game_file)
		elif code == ":wq":
			self.save_state(self.game_file)
			raise SystemExit
		elif code == ":q":
			raise SystemExit
		elif code == ":r":
			tree = ABPruning_Tree(str(self), 5, LOWER_BOUND, UPPER_BOUND, game_heuristic1, self.get_player() == 1)
			tree.search()
	
	def get_player(self):
		return (self.turn % 2) + 1
	
	def check_full(self):
		full = True
		for x in self.boards_won:
			if x == -1:
				full = False
		return full
	
	def check_for_winner(self):
		for x in range(3):
			if self.boards_won[3*x] == self.boards_won[3*x+1] == self.boards_won[3*x+2] > 0:
				self.winner = self.boards_won[3*x]
			if self.boards_won[x] == self.boards_won[x+3] == self.boards_won[x+6] > 0:
				self.winner = self.boards_won[x]
		if self.boards_won[0] == self.boards_won[4] == self.boards_won[8] > 0:
			self.winner = self.boards_won[4]
		if self.boards_won[2] == self.boards_won[4] == self.boards_won[6] > 0:
			self.winner = self.boards_won[4]
		if self.winner == -1 and self.check_full():
			self.winner = 0
		return self.winner
		
	def get_children_states(self):
		root = str(self)
		children = []
		if self.current_box == -1:
			for box in range(9):
				if self.boards_won[box] == -1:
					for x in range(9):
						self.current_box = box
						self.current_col = box % 3
						self.current_row = (box - (box % 3))/3
						if self.try_placing_square(x):
							self.turn += 1
							children += [[str(self), box, x]]
							self.load_state_from_string(root)
		else:
			box = self.current_box
			for x in range(9):
				if self.try_placing_square(x):
					self.turn += 1
					children += [[str(self), box, x]]
					self.load_state_from_string(root)
		return children
		
	def opg(self):
		prgm_lib.cls(100)
		for x in range(len(self.grid)):
			size = 0
			string0 = ''
			for z in range(3):
				string1 = ''
				string2 = ''
				for y in range(len(self.grid[x])):
					string3 = self.grid[x][y].get_row(z)
					for var in range(len(string3)):
						string2 += "-"
					string1 += string3 + " || "
					string2 += " || "
				print string1[:-4]
				if z != 2:
					print string2[:-4]
				size = len(string1)-4
			for var in range(size):
				string0 += "="
			if x != 2:
				print string0
		print
		
	def play(self):
		if self.history:
			self.save_state(self.game_file)
		while self.winner == -1:
			self.do_turn()
		if not self.quiet:
			self.opg()
			if self.winner != 0:
				print "PLAYER" + str(self.winner) + " IS THE WINNER!!!"
			else:
				print "IT WAS A DRAW!"
			
	def get_num_for_square(self):
		human = self.is_human_turn()
		num = -1
		finished_getting_num = False
		while not finished_getting_num:
			num = self.current_player().choose_square(self)
			if str(num) in self.escapes:
				self.handle_escape(num)
			else:
				while (num < 0) or (num > 8):
					if human:
						print "please pick an int in [0-8]"
					num = self.current_player().choose_square(self)
					if str(num) in self.escapes:
						self.handle_escape(num)
						num = -1
				finished_getting_num = True
		return num
		
	def is_game_over(self):
		return self.winner != -1
		
	def try_placing_square(self, num):
		inner_col = num % 3
		inner_row = (num - (num % 3))/3
		value = False
		if self.grid[self.current_row][self.current_col].get_square(inner_row,inner_col) == " ":
			token = self.player_token[self.get_player()]
			self.grid[self.current_row][self.current_col].set_square(inner_row,inner_col,token)
			if self.grid[self.current_row][self.current_col].is_finished():
				box_winner = self.grid[self.current_row][self.current_col].get_winner()
				self.boards_won[self.current_box] = box_winner
				self.check_for_winner()
			if not self.grid[inner_row][inner_col].is_finished():
				self.current_box = num
				self.current_row = inner_row
				self.current_col = inner_col
			else:
				self.current_box = -1
				self.current_row = -1
				self.current_col = -1
			value = True
		return value
		
	def get_num_for_box(self):
		human = self.is_human_turn()
		num = -1
		finished = False
		while not finished:
			num = self.current_player().choose_board(self)
			if str(num) in self.escapes:
				self.handle_escape(num)
			else:
				while (num < 0) or (num > 8):
					if human:
						print "please pick an int in [0-8]"
					num = self.current_player().choose_board(self)
					if str(num) in self.escapes:
						self.handle_escape(num)
						num = -1
				if self.boards_won[num] != -1:
					if human:
						print "Sorry, that board is already complete, please pick another."
				else:
					finished = True	
		return num
								
	def do_turn(self):
		human = self.is_human_turn()
		if human:
			self.opg()
		if self.current_box != -1:
			if human:
				print "Current Square to be played in, at location (" + str(self.current_row) + ", " + str(self.current_col) + ")"
				self.grid[self.current_row][self.current_col].opg()
				print "Player" + str(self.get_player()) + ", it is your turn to play on this board."
				print "Please enter a number [0-8] corresponding to the space you would like to play in."
				print "Of course, with 0 corresponding to the top left:"
			num = -1
			finished_getting_num = False
			finished_playing = False
			while not finished_playing:
				num = self.get_num_for_square()
				if self.try_placing_square(num):
					self.turn += 1
					finished_playing = True
			if self.history:
				self.save_state(self.game_file)	
		else:
			if human:
				print "Player" + str(self.get_player()) + ", it is your choice which board to play on."
				print "Please enter a number [0-8] corresponding to the board you would like to play on."
				print "Of course, with 0 corresponding to the top left:"
			num = self.get_num_for_box()
			self.current_box = num
			self.current_col = num % 3
			self.current_row = (num - (num % 3))/3
			
class Watcher:
	def __init__(self, game_file):
		self.file = game_file
		FILE = open(self.file, 'r')
		source = FILE.read()
		FILE.close()
		self.turn_list = re.split("\n+", source)[:-1]
		self.current_turn = 0
		self.last_turn = len(self.turn_list)
		self.game = Board(Player(),Player(),TEMP_GAME_FILE)
		self.has_eval = False
		self.eval = None
		self.show_eval = False
		self.pos_value = 0

	def write_current_turn(self):
		self.game.load_state_from_string(self.turn_list[self.current_turn])
		if self.has_eval:
			self.pos_value = self.eval(str(self.game))
		
	def set_heuristic(self, heuristic):
		self.eval = heuristic
		self.has_eval = True
		
	def set_show_eval(self, flag):
		if self.has_eval:
			self.show_eval = flag	
		else:
			self.show_eval = False
				
	def next_turn(self):
		if self.current_turn < self.last_turn-1:
			self.current_turn += 1
		else:
			self.current_turn = 0
		self.write_current_turn()
	
	def previous_turn(self):
		if self.current_turn > 0:
			self.current_turn -= 1
		else:
			self.current_turn = self.last_turn - 1
		self.write_current_turn()

	def watch(self):
		done = False
		while not done:
			self.game.opg()
			print "Viewing turn " + str(self.current_turn) + " out of " + str(self.last_turn - 1)
			print "press 'q' to quit, 'a' to go to the previous turn, 'd' to go to the next turn."
			if self.show_eval:
				print "This position evaluates to: " + str(self.pos_value)
			input_char = prgm_lib.getch()
			if input_char == 'q':
				done = True
			elif input_char == 'a':
				self.previous_turn()
			elif input_char == 'd':
				self.next_turn()


class Player:
	def __init__(self):
		self.human = False
		
	def is_human(self):
		return self.human
		
	def choose_board(self, game):
		pass
		
	def choose_square(self, game):
		pass
		

class Human(Player):
	def __init__(self):
		self.human = True

	def choose_board(self, game):
		return prgm_lib.get_int_escape_codes(game.escapes)
		
	def choose_square(self, game):
		return prgm_lib.get_int_escape_codes(game.escapes)
		
		
class RandomAI(Player):
	def __init__(self):
		self.human = False
		
	def choose_board(self, game):
		return random.randint(0,8)
		
	def choose_square(self, game):
		return random.randint(0,8)


class AI_ABPruning(Player):
	def __init__(self, heuristic_func):
		self.human = False
		self.square_to_pick = -1
		self.heuristic = heuristic_func
		
	def choose_board(self, game):
		tree = ABPruning_Tree(str(game), 5, LOWER_BOUND, UPPER_BOUND, self.heuristic, game.get_player() == 1)
		tree.search()
		child = tree.get_best_child()
		self.square_to_pick = child[2]
		return child[1]
	
	def choose_square(self, game):
		value = self.square_to_pick
		if self.square_to_pick != -1:
			self.square_to_pick = -1
		else:
			tree = ABPruning_Tree(str(game), 5, LOWER_BOUND, UPPER_BOUND, self.heuristic, game.get_player() == 1)
			tree.search()
			child = tree.get_best_child()
			value = child[2]
		return value
		
				
class ABPruning_Tree:
	def __init__(self, game_state = "", depth_lim = 10, A = LOWER_BOUND, B = UPPER_BOUND, heuristic = None, i_am_max = True):
		self.state = game_state
		self.children = []
		self.best_child = [["",-1,-1]]
		self.alpha = A
		self.beta = B
		self.depth_limit = depth_lim
		self.evaluate = heuristic
		self.value = 0
		self.is_max = i_am_max
		
	def set_heuristic(self, heuristic):
		self.evaluate = heuristic
		
	def set_state(self, game_state):
		self.state = game_state
		
	def set_children(self):
		game = Board(Player(),Player(),DEFAULT_GAME_FILE)
		game.load_state_from_string(self.state)
		self.children = game.get_children_states()
		
	def is_terminal_node(self):
		game = Board(Player(),Player(),DEFAULT_GAME_FILE)
		game.load_state_from_string(self.state)
		return game.is_game_over()
		
	def get_best_child(self):
		value = []
		if len(self.best_child)==1:
			value = self.best_child[0]
		else:
			size = len(self.best_child)-1
			value = self.best_child[random.randint(0,size)]
		return value
		
		
	def search(self):
		if self.depth_limit == 0 or self.is_terminal_node():
			self.value = self.evaluate(self.state)
		else:
			self.set_children()
			if self.is_max:
				self.value = LOWER_BOUND
				for child_state in self.children:
					child = ABPruning_Tree(child_state[0], self.depth_limit - 1, self.alpha, self.beta, self.evaluate, not self.is_max)
					child_value = child.search()
					if self.depth_limit == 5:						######
						print "child is: " + str(child_state)				######
						print "child value is: " + str(child_value)			######
						print "best value is : " + str(self.value)			######
					if child_value > self.value:
						if self.depth_limit == 5:					######
							print "### new best child found ###"			######
						self.best_child = [child_state]
					elif child_value == self.value:
						if self.depth_limit == 5:					######
							print "### another best child added ###"		######
						self.best_child += [child_state]
					self.value = max(self.value, child_value)
					self.alpha = max(self.alpha, self.value)
					if self.beta <= self.alpha:
						break
			else:
				self.value = UPPER_BOUND
				for child_state in self.children:
					child = ABPruning_Tree(child_state[0], self.depth_limit - 1, self.alpha, self.beta, self.evaluate, not self.is_max)
					child_value = child.search()
					if self.depth_limit == 5:						######
						print "child is: " + str(child_state)				######
						print "child value is: " + str(child_value)			######
						print "best value is : " + str(self.value)			######
					if child_value < self.value:
						if self.depth_limit == 5:					######
							print "### new best child found ###"			######
						self.best_child = [child_state]
					elif child_value == self.value:
						if self.depth_limit == 5:					######
							print "### another best child added ###"		######
						self.best_child += [child_state]
					self.value = min(self.value, child_value)
					self.beta = min(self.beta, self.value)
					if self.beta <= self.alpha:
						break
		return self.value
	

def list_product(thing):
	product = 1
	for x in thing:
		product *= x
	return product
	
def tictactoe_string_to_numbers(tic_state):
	player_map = {"X":1, " ":0, "O":-1}
	grid = []
	for j in range(3):
		row = []
		for k in range(3):
			row.append(player_map[tic_state[3*j+k]])
		grid.append(row)
	return grid

def tictactoe_moves_to_win(grid):	
	products_rows = [list_product(row) for row in grid]
	products_cols = [list_product([grid[row][col] for row in range(3)]) for col in range(3)]
	main_diag = grid[0][0] * grid[1][1] * grid[2][2]
	off_diag = grid[2][0] * grid[1][1] * grid[0][2]
	value = max(products_rows + products_cols + [main_diag] + [off_diag])
	return value
	
def jank_log2(num):
	power = 0
	while 2 ** power <= num:
		power += 1
	return power 
			
def count_won_boards(moves_grid):
	value = 0
	for x in range(3):
		for y in range(3):
			if moves_grid[x][y]==8:
				value += 1
	return value
			
def game_heuristic1(game_state):
	value = 0
	board_list = re.split(";", game_state)[:-2]
	big_grid_x = []
	big_grid_o = []
	for x in range(3):
		row_x = []
		row_o = []
		for y in range(3):
			grid = tictactoe_string_to_numbers(board_list[3*x + y])
			grid_x = [[grid[j][k]+1 for k in range(3)] for j in range(3)]
			grid_o = [[abs(grid[j][k]-1) for k in range(3)] for j in range(3)]
			row_x += [tictactoe_moves_to_win(grid_x)]
			row_o += [tictactoe_moves_to_win(grid_o)]
		big_grid_x += [row_x]
		big_grid_o += [row_o]
	won_boards_x = count_won_boards(big_grid_x)
	won_boards_o = count_won_boards(big_grid_o)
	board_offset = 5*(won_boards_x - won_boards_o)
	moves_till_x_wins = tictactoe_moves_to_win(big_grid_x)
	moves_till_o_wins = tictactoe_moves_to_win(big_grid_o)
	if moves_till_x_wins != 0:
		moves_x = 10 - jank_log2(moves_till_x_wins)
	else:
		moves_x = -1
	if moves_till_o_wins != 0:
		moves_o = 10 - jank_log2(moves_till_o_wins)
	else:
		moves_o = -1
	if moves_x != -1 and moves_o != -1:
		value = moves_o - moves_x + board_offset
	elif moves_x == -1 and moves_o == -1:
		value = 0
	elif moves_x == -1 and moves_o != -1:
		value = LOWER_BOUND / 2
	elif moves_x != -1 and moves_o == -1:
		value = UPPER_BOUND / 2
	elif moves_x == 0:
		value = UPPER_BOUND
	elif moves_y == 0:
		value = LOWER_BOUND
	return value

o_args = prgm_lib.arg_flag_ordering(sys.argv,[1,1,0,0,0,0],[re_mk('file'),re_mk('players'),re_mk('load'),re_mk('test'),re_mk('history'),re_mk('watch')])
game_file = DEFAULT_GAME_FILE
num_humans = 2
test = False
load = False
history = False
watch = False
if str(o_args[0]) != "None":
	game_file = str(o_args[0])
if str(o_args[1]) != "None":
	num_humans = int(o_args[1])
if str(o_args[2]) != "None":
	load = True
if str(o_args[3]) != "None":
	test = True
if str(o_args[4]) != "None":
	history = True
if str(o_args[5]) != "None":
	watch = True
	
if watch and str(o_args[0]) == "None":
	print "Please enter the path to the file containing the game to watch:"
	game_file = prgm_lib.get_str()


player1 = Human()
player2 = Human()

if num_humans == 1:
	if random.randint(0,1) == 0:
		player1 = AI_ABPruning(game_heuristic1)
	else:
		player2 = AI_ABPruning(game_heuristic1)
elif num_humans == 0:
	player1 = AI_ABPruning(game_heuristic1)
	player2 = AI_ABPruning(game_heuristic1)

if watch:
	movie = Watcher(game_file)
	movie.set_heuristic(game_heuristic1)
	movie.set_show_eval(True)
	movie.watch()
else:
	if not test:
		game = Board(player1, player2, game_file, history, load)
		game.play()
	else:
		player1 = RandomAI()
		player2 = RandomAI()
		max_turns = 0
		counter = 0
		while max_turns < 81:
			game = Board(player1, player2, game_file, history, load, True)
			game.play()
			counter += 1
			if game.get_turn() >= max_turns:
				game.opg()
				max_turns = game.get_turn()
				print str(max_turns) + " ; " + str(counter)







