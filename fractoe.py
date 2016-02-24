#!/usr/bin/python
#fractal_tic_tac_toe.py
###USAGE### fractal_tic_tac_toe.py [-w] [-f <filename>] | [-l] [-f <filename>] [-p <num_players>] [-t] [-h] [-s <show_depth>] ; sms=N ; $#=0-7
import prgm_lib
import sys
import random
import heuristics
import player
import watcher
from fractoe_board import Board
from fractoe_board import DEFAULT_GAME_FILE
from fractoe_board import TEMP_GAME_FILE

re_mk=prgm_lib.flag_re_mk

### main stuff ###

o_args = prgm_lib.arg_flag_ordering(sys.argv,[1,1,1,0,1,0,0],[re_mk('file'),re_mk('players'),re_mk('show'),re_mk('load'),re_mk('test'),re_mk('history'),re_mk('watch')])
game_file = DEFAULT_GAME_FILE
num_humans = 2
test = False
load = False
history = False
watch = False
this_test = "putingambit"
show_thought_level = 0
if str(o_args[0]) != "None":
	game_file = str(o_args[0])
if str(o_args[1]) != "None":
	num_humans = int(o_args[1])
if str(o_args[2]) != "None":
	show_thought_level = int(o_args[2])
if str(o_args[3]) != "None":
	load = True
if str(o_args[4]) != "None":
	test = True
	this_test = str(o_args[4])
if str(o_args[5]) != "None":
	history = True
if str(o_args[6]) != "None":
	watch = True
	
	
if watch and str(o_args[0]) == "None":
	print "Please enter the path to the file containing the game to watch:"
	game_file = prgm_lib.get_str()


player1 = player.Human()
player2 = player.Human()

if num_humans == 1:
	if random.randint(0,1) == 0:
		player1 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
	else:
		player2 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
elif num_humans == 0:
	player1 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
	player2 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
	if random.randint(0,1) == 0:
		player1 = player.RandomAI()
		print "Player 1 is random"
	else:
		player2 = player.RandomAI()
		print "Player 2 is random"

### decide which test to run ###
#this_test = "draw1"
#this_test = "putingambit"
#this_test = "draw2"

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
		if this_test == "draw1":
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
		elif this_test == "putingambit":
			player1 = player.AI_PutinGambit(heuristics.game_heuristic1, show_thought_level)
			player2 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
			game = Board(player1, player2, game_file, history, load)
			game.play()
		elif this_test == "draw2":
			player1 = player.AI_ABPruning(heuristics.game_length, show_thought_level)
			player2 = player.AI_ABPruning(heuristics.game_length, show_thought_level)
			game = Board(player1, player2, game_file, history, load)
			game.play()





