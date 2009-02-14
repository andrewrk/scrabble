#!/usr/bin/env python

import sys
import string
from anagram import AnagramSolver
from dictionary import Dictionary

class ScrabbleBoard:
	def __init__(self, board_file = "boards/blank"):
		self.board = []
		self.pieces = {}
		self.read_board(board_file)

	def write_board(self, board_file):
		open(board_file).write('\n'.join(map(lambda x: ''.join(x), board)))
	
	def read_board(self, board_file):
		lines = filter(lambda x: len(x) != 0 and x[0] != '#', open(board_file).read().split('\n'))
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
		return int(self.pieces[char][1])
	
	def piece_count(self, char):
		return int(self.pieces[char][0])
	
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
		elif board.get_square(bx, by) == '3':
			letter_score *= 3
		elif board.get_square(bx, by) == 'D':
			word_multiplier *= 2
		elif board.get_square(bx, by) == 'T':
			word_multiplier *= 3
		word_score += letter_score

		bx += dir_x
		by += dir_y

		if bx >= board.width() or by >= board.height():
			return -1 #invalid move - off the board
	
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
			print "Looking at (%i, %i)..." % (x, y)
			print "----------------------"
			# come up with words to play here
			# lay the word across and down
			for m in range(2):
				xdir = 1-m
				ydir = m
				overlay = '_______'
				xi = x
				yi = y
				overlay_pos = -1 # first position when we cross a letter

				for i in range(len(overlay)):
					if string.lowercase.find(board.get_square(xi,yi)) != -1:
						# there is a letter here; add it to overlay
						tmp = list(overlay)
						tmp[i] = board.get_square(xi, yi)
						overlay = ''.join(tmp)
						if overlay_pos == -1:
							overlay_pos = i
					xi += xdir
					yi += ydir

					if xi >= board.width() or yi >= board.height():
						break
				
				if xi < board.width() and yi < board.height():
					if string.lowercase.find(board.get_square(xi,yi)) != -1:
						# there is a letter here; add it to overlay
						tmp = list(overlay)
						tmp[i] = board.get_square(xi, yi)
						overlay = ''.join(tmp)
						if overlay_pos == -1:
							overlay_pos = len(overlay)
				
				for i in range(len(overlay)-1):
					# remove i characters from overlay
					overlay = overlay[:-1]
					
					if overlay_pos != -1 and overlay_pos <= len(overlay):
						for choice in ags.anagram(overlay, chars):
							# lay the word 
							print "Testing word: %s" % choice
							pts[move_points(board, choice, x, y, xdir, ydir)] = (choice, x, y, xdir, ydir,)
	
	# sort the keys of pts to discover the highest scoring option
	moves = pts.keys()
	moves.sort(reverse=True)
	
	directions = {'01': 'down', '10': 'across'}
	print "Best move: '%s' at position (%i, %i) %s which scores %i points." % (pts[moves[0]][0], pts[moves[0]][1], pts[moves[0]][2], directions[str(pts[moves[0]][3])+str(pts[moves[0]][4])], moves[0])
