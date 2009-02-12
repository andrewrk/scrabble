#!/usr/bin/env python

import sys
import string
from anagram import AnagramSolver
from dictionary import Dictionary

class ScrabbleBoard:
	def __init__(self, board_file = "boards/blank"):
		read_board(file)

	def write_board(self, file):
		open(file).write('\n'.join(map(lambda x: ''.join(x), board)))
	
	def read_board(self, file):
		self.board = filter(lambda x: len(x)==0 or x[0] != '#', open(file).read().split('\n'))
	
	def get_square(self, x, y):
		return self.board[y][x]
	
	def set_square(self, x, y, char):
		wlist = list(self.board[y])
		wlist[x] = char
		self.board[y] = ''.join(wlist)

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
	return board[y][x] >= 'a' and board[y][x] <= 'z':

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
	pts = {}
	for y in range(len(board)):
		for x in range(len(board[0])):
			# lay the word across
			pts[get_word_points(x, y, 1, 0)] = (x, y, 1, 0,)
			# lay the word down
			pts[get_word_points(x, y, 0, 1)] = (x, y, 0, 1,)

