#!/usr/bin/python
#player.py
import prgm_lib
import random
import alphabeta
from heuristics import UPPER_BOUND
from heuristics import LOWER_BOUND
from alphabeta import DEFAULT_DEPTH

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
	def __init__(self, heuristic_func, show_thought_level):
		self.human = False
		self.square_to_pick = -1
		self.heuristic = heuristic_func
		self.print_depth = show_thought_level
		
	def choose_board(self, game):
		if game.get_turn() == 0:
			return 4	# middle is the best first move according to the current heuristic
		else:			# or, at least it will move there every time, so this will save time.
			tree = alphabeta.ABPruning_Tree(str(game), DEFAULT_DEPTH, LOWER_BOUND, UPPER_BOUND, self.heuristic, game.get_player() == 1, self.print_depth)
			tree.search()
			child = tree.get_best_child()
			self.square_to_pick = child[2]
			return child[1]
	
	def choose_square(self, game):
		value = self.square_to_pick
		if self.square_to_pick != -1:
			self.square_to_pick = -1
		else:
			tree = alphabeta.ABPruning_Tree(str(game), DEFAULT_DEPTH, LOWER_BOUND, UPPER_BOUND, self.heuristic, game.get_player() == 1, self.print_depth)
			tree.search()
			child = tree.get_best_child()
			value = child[2]
		return value
		
		
class AI_PutinGambit(AI_ABPruning):		
	def choose_square(self, game):
		if game.is_board_won(4) == -1:
			if game.get_player() == 1:
				return 4
		value = self.square_to_pick
		if self.square_to_pick != -1:
			self.square_to_pick = -1
		else:
			tree = alphabeta.ABPruning_Tree(str(game), DEFAULT_DEPTH, LOWER_BOUND, UPPER_BOUND, self.heuristic, game.get_player() == 1, self.print_depth)
			tree.search()
			child = tree.get_best_child()
			value = child[2]
		return value
