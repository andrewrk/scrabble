#!/usr/bin/env python

import sys
import string
from anagram import AnagramSolver
from dictionary import Dictionary

class ScrabbleBoard:
	def __init__(self, board_file = "boards/blank"):
		self.board = []
		self.pieces = {}
		self.read_board(file)

	def write_board(self, file):
		open(file).write('\n'.join(map(lambda x: ''.join(x), board)))
	
	def read_board(self, file):
		lines = filter(lambda x: len(x) != 0 and x[0] != '#', open(file).read().split('\n'))
		self.board = filter(lambda x: x.find(':') == -1, lines)
		self.pieces = dict([map(lambda y: y.strip(), x.split(':')) for x in filter(lambda x: x.find(':') != -1, lines)])
		for key in self.pieces.keys():
			self.pieces[key] = self.pieces[key].split('x')

	def get_square(self, x, y):
		return self.board[y][x]
	
	def set_square(self, x, y, char):
		wlist = list(self.board[y])
		wlist[x] = char
		self.board[y] = ''.join(wlist)
	
	def piece_score(self, char):
		return self.pieces[char][1]
	
	def piece_count(self, char):
		return self.pieces[char][0]
	
	def width(self):
		return len(self.board[0])
	
	def height(self):
		return len(self.board)

def get_word_points(x, y, xdir, ydir):
	xi = x
	yi = y
	charsLeft = len(chars)
	charString = ''
	while charsLeft > 0:
		if is_letter(x,y):
			charString += board[yi][xi]
		x += xdir
		y += ydir
		

def is_letter(x, y):
	return board[y][x] >= 'a' and board[y][x] <= 'z'

def valid_move(old_board, new_board):
	return move_points(old_board, new_board) == -1

def move_points(board, word, x, y, dir_x, dir_y, is_root = True):
	# how many points are earned for moving here?
	# -1 means it is not a valid move
	bx = x
	by = y
	
	# TODO: this doesn't take into account multiple
	# word connections at once yet.
	word_multiplier = 1
	word_score = 0
	for i in range(len(word)):
		letter_score = board.piece_score(word[i])
		if board.get_square(bx, by) == '2':
			letter_score *= 2
		else if board.get_square(bx, by) == '3':
			letter_score *= 3
		else if board.get_square(bx, by) == 'D':
			word_multiplier *= 2
		else if board.get_square(bx, by) == 'T':
			word_multiplier *= 3
		word_score += letter_score

		bx += dir_x
		by += dir_y
	
	word_score *= word_multiplier
	# TODO don't forget to add the offshoots to word score later
	
	return word_score 


if __name__=='__main__':
	if len(sys.argv) <= 2:
		print "Usage: scrabble <board_file> <list_of_letters> [<dictionary_file>]"
		sys.exit(1)

	board = ScrabbleBoard(sys.argv[1])
	chars = sys.argv[2].lower()
	dicfile = "dictionaries/english"
	if len(sys.argv) >= 4:
		dicfile = sys.argv[3]
	

	# go through each open square
	# on the scrabble board and try to play every word. keep track of how 
	# many points each move is worth (if it is valid)
	ags = AnagramSolver(dicfile)
	pts = {}
	for y in range(board.height()):
		for x in range(board.width()):
			# come up with words to play here
			for each choice in ags.anagram('_______', chars):
				# lay the word across
				pts[move_points(board, choice, x, y, 1, 0)] = (choice, x, y, 1, 0,)
				# lay the word down
				pts[move_points(board, choice, x, y, 0, 1)] = (choice, x, y, 0, 1,)

	# sort the keys of pts to discover the highest scoring option
	moves = pts.keys()
	moves.sort(reverse=True)

	print pts[moves[0]][0]
