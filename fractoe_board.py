#!/usr/bin/python
#fractoe_board.py
import re
import prgm_lib
import tictactoe
Tictactoe = tictactoe.Tictactoe
import os

DEFAULT_GAME_FILE = os.path.expanduser('~') + '/lib/fractoe_game'
TEMP_GAME_FILE = os.path.expanduser('~') + '/lib/fractoe_game_temp'

def coor_split(num):
	col = num % 3
	row = (num - col) / 3
	return [row,col]
	
def coor_splice(row,col):
	return row*3 + col

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
		
	def is_board_won(self, board):
		return self.boards_won[board]
	
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
#			tree = alphabeta.ABPruning_Tree(str(self), 5, LOWER_BOUND, UPPER_BOUND, game_heuristic1, self.get_player() == 1)
#			tree.search()
			pass
	
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
		else:
			print "The computer is thinking..."
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
			

