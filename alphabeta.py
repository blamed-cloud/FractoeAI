#!/usr/bin/python
#alphabeta.py
from __future__ import print_function
import random
import player
from fractoe_board import Board
from fractoe_board import DEFAULT_GAME_FILE
from fractoe_board import TEMP_GAME_FILE
from heuristics import UPPER_BOUND
from heuristics import LOWER_BOUND
from heuristics import is_volatile
import sys

DEFAULT_DEPTH = 5
VOLATILE_DEPTH = -3

class ABPruning_Tree:
	def __init__(self, game_state = "", depth_lim = DEFAULT_DEPTH, A = LOWER_BOUND, B = UPPER_BOUND, heuristic = None, i_am_max = True, p_depth = 0):
		self.state = game_state
		self.children = []
		self.best_child = [["",-1,-1]]
		self.alpha = A
		self.beta = B
		self.depth_limit = depth_lim
		self.evaluate = heuristic
		self.value = 0
		self.is_max = i_am_max
		self.print_depth = p_depth
		
	def set_heuristic(self, heuristic):
		self.evaluate = heuristic
		
	def set_state(self, game_state):
		self.state = game_state
		
	def set_children(self):
		game = Board(player.Player(),player.Player(),DEFAULT_GAME_FILE)
		game.load_state_from_string(self.state)
		self.children = game.get_children_states()
		
	def is_terminal_node(self):
		game = Board(player.Player(),player.Player(),DEFAULT_GAME_FILE)
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
		if (self.depth_limit <= 0 and not is_volatile(self.state)) or (self.depth_limit == VOLATILE_DEPTH) or self.is_terminal_node():
			self.value = self.evaluate(self.state)
		else:
			self.set_children()
			if self.depth_limit == DEFAULT_DEPTH:
				if self.print_depth > 0:
					print("TURN", file=sys.stderr)
			indent = "---="
			if self.is_max:
				self.value = LOWER_BOUND
				for child_state in self.children:
					child = ABPruning_Tree(child_state[0], self.depth_limit-1, self.alpha, self.beta, self.evaluate, not self.is_max, self.print_depth)
					child_value = child.search()
					layer = DEFAULT_DEPTH - self.depth_limit	
					if (self.print_depth != 0) and (layer < self.print_depth):
						print(indent * layer + "child is: ", str(child_state), file=sys.stderr)
						print(indent * layer + "child value is: ", str(child_value), file=sys.stderr)
						print(indent * layer + "best value is : ", str(self.value), file=sys.stderr)
					if child_value > self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### new best child found ###", file=sys.stderr)
						self.best_child = [child_state]
					elif child_value == self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### another best child added ###", file=sys.stderr)
						self.best_child += [child_state]
					self.value = max(self.value, child_value)
					self.alpha = max(self.alpha, self.value)
					if self.beta < self.alpha:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "ALPHA cutoff", file=sys.stderr)
						break
			else:
				self.value = UPPER_BOUND
				for child_state in self.children:
					child = ABPruning_Tree(child_state[0], self.depth_limit-1, self.alpha, self.beta, self.evaluate, not self.is_max, self.print_depth)
					child_value = child.search()
					layer = DEFAULT_DEPTH - self.depth_limit
					if (self.print_depth != 0) and (layer < self.print_depth):
						print(indent * layer + "child is: ", str(child_state), file=sys.stderr)
						print(indent * layer + "child value is: ", str(child_value), file=sys.stderr)
						print(indent * layer + "best value is : ", str(self.value), file=sys.stderr)
					if child_value < self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### new best child found ###", file=sys.stderr)
						self.best_child = [child_state]
					elif child_value == self.value:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "### another best child added ###", file=sys.stderr)
						self.best_child += [child_state]
					self.value = min(self.value, child_value)
					self.beta = min(self.beta, self.value)
					if self.beta < self.alpha:
						if (self.print_depth != 0) and (layer < self.print_depth):
							print(indent * layer + "BETA cutoff", file=sys.stderr)
						break
			if self.depth_limit == DEFAULT_DEPTH:
				if self.print_depth > 0:
					print("END TURN\n", file=sys.stderr)
		return self.value
	

