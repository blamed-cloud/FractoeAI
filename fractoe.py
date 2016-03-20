#!/usr/bin/python
#fractal.py
###USAGE### fractal.py [-w] [-f <filename>] | [-l] [-f <filename>] [-p <num_players>] [-t] [-h] [-s <show_depth>] [-x] [-o] [-b] ; sms=N ; $#=0-9
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
arg_nums = [1,1,1,0,1,0,0,0,0,0]
regexs = [re_mk('file'),re_mk('players'),re_mk('show'),re_mk('load'),re_mk('test'),re_mk('history'),re_mk('watch'),re_mk("xhuman"),re_mk("ohuman"),re_mk("board")]
o_args = prgm_lib.arg_flag_ordering(sys.argv,arg_nums,regexs)
game_file = DEFAULT_GAME_FILE
num_humans = 2
test = False
load = False
history = False
watch = False
human_is_x = False
human_is_o = False
show_board = False
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
if str(o_args[7]) != "None":
	human_is_x = True
if str(o_args[8]) != "None" and not human_is_x:
	human_is_o = True
if str(o_args[9]) != "None":
	show_board = True
	
if watch and str(o_args[0]) == "None":
	print "Please enter the path to the file containing the game to watch:"
	game_file = prgm_lib.get_str()


player1 = player.Human()
player2 = player.Human()

if num_humans == 1:
	if human_is_x:
		player2 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
	elif human_is_o:
		player1 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
	else:
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

if watch:
	movie = watcher.Watcher(game_file)
	movie.set_heuristic(heuristics.game_heuristic1)
	movie.set_show_eval(True)
	movie.watch()
else:
	if not test:
		game = Board(player1, player2, game_file, history, load, show=show_board)
		game.play()
	else:
		if this_test == "draw1":
			player1 = player.RandomAI()
			player2 = player.RandomAI()
			max_turns = 0
			counter = 0
			while max_turns < 81:
				game = Board(player1, player2, game_file, history, load, True, show_board)
				game.play()
				counter += 1
				if game.get_turn() >= max_turns:
					game.opg()
					max_turns = game.get_turn()
					print str(max_turns) + " ; " + str(counter)
		elif this_test == "putingambit":
			player1 = player.AI_PutinGambit(heuristics.game_heuristic1, show_thought_level)
			player2 = player.AI_ABPruning(heuristics.game_heuristic1, show_thought_level)
			game = Board(player1, player2, game_file, history, load, show=show_board)
			game.play()
		elif this_test == "draw2":
			player1 = player.AI_ABPruning(heuristics.game_length, show_thought_level)
			player2 = player.AI_ABPruning(heuristics.game_length, show_thought_level)
			game = Board(player1, player2, game_file, history, load, show=show_board)
			game.play()





