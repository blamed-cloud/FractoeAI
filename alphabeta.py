#!/usr/bin/python
#alphabeta.py
import random
import player
from fractoe_board import Board
from fractoe_board import DEFAULT_GAME_FILE
from fractoe_board import TEMP_GAME_FILE
from heuristics import UPPER_BOUND
from heuristics import LOWER_BOUND

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
	

