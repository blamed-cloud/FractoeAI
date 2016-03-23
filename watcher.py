#!/usr/bin/python
#watcher.py
import re
import PythonLibraries.prgm_lib as prgm_lib
from fractoe_board import Board
from fractoe_board import DEFAULT_GAME_FILE
from fractoe_board import TEMP_GAME_FILE
import player

class Watcher:
	def __init__(self, game_file):
		self.file = game_file
		FILE = open(self.file, 'r')
		source = FILE.read()
		FILE.close()
		self.turn_list = re.split("\n+", source)[:-1]
		self.current_turn = 0
		self.last_turn = len(self.turn_list)
		self.game = Board(player.Player(),player.Player(),TEMP_GAME_FILE)
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


