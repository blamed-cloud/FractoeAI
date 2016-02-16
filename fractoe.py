#!/usr/bin/python
#fractal_tic_tac_toe.py
###USAGE### fractal_tic_tac_toe.py [-w] [-f <filename>] | [-l] [-f <filename>] [-p <num_players>] [-q] [-h] ; sms=N ; $#=0-3
import prgm_lib
import sys
import random
import heuristics
import player
import watcher
import os
from fractoe_board import Board
from fractoe_board import DEFAULT_GAME_FILE
from fractoe_board import TEMP_GAME_FILE

re_mk=prgm_lib.flag_re_mk

### main stuff ###

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


player1 = player.Human()
player2 = player.Human()

if num_humans == 1:
	if random.randint(0,1) == 0:
		player1 = player.AI_ABPruning(heuristics.game_heuristic1)
	else:
		player2 = player.AI_ABPruning(heuristics.game_heuristic1)
elif num_humans == 0:
	player1 = player.AI_ABPruning(heuristics.game_heuristic1)
	player2 = player.AI_ABPruning(heuristics.game_heuristic1)

if watch:
	movie = watcher.Watcher(game_file)
	movie.set_heuristic(heuristics.game_heuristic1)
	movie.set_show_eval(True)
	movie.watch()
else:
	if not test:
		game = Board(player1, player2, game_file, history, load)
		game.play()
	else:
		player1 = player.RandomAI()
		player2 = player.RandomAI()
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







