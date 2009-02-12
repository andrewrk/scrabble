#!/usr/bin/env python

import sys
import string
from dictionary import Dictionary

class AnagramSolver:
	def __init__(self, dictionary = Dictionary()):
		self.outwords = {}
		self.permutations = {}
		self.dictionary = dictionary

	def swap(self, word, i, j):
		wlist = list(word)
		tmp = wlist[i]
		wlist[i] = wlist[j]
		wlist[j] = tmp
		return ''.join(wlist)

	def swapChar(self, word, index, char):
		wlist = list(word)
		wlist[index] = char
		return ''.join(wlist)

	def get_combos(self, letters):
		check_words(letters, 0)
		check_length(letters)

	def get_permutations(self, word):
		self.permutations = {}
		self.get_permutations_rec(word, 0)
		return self.permutations.keys()

	def get_permutations_rec(self, word, i):
		while i<len(word):
			# try it with letter[i] switched with all next letters
			for j in range(i, len(word)):
				test = self.swap(word, i, j)
				self.permutations[test] = 1
				if i < len(word) - 1:
					self.get_permutations_rec(test, i+1)
			i += 1
		
		

	def wild(self, str, num_wild):
		if num_wild > 0:
			return [y + x for x in string.lowercase for y in wild(str, num_wild-1)]
		else:
			return [str]

	def anagram(self, mask, chars):
		# mask is of the form: e__ph_*t
		# where lower case letters are literal, underscores can
		# be filled in with chars from chars, and asterisks
		# can be filled with any character a-z
		
		# clear the output hash
		self.outwords = {}
		# get the list of wildcard possibilities
		combos = self.wild('', mask.count('*'))
		# get the list of character permutations
		charPerms = self.get_permutations(chars)
		# do anagram for each wildcard possibility
		for combo in combos:
			newmask = mask
			lastAsterik = -1
			
			for i in range(len(combo)):
				lastAsterik = newmask.find("*", lastAsterik+1)

				if lastAsterik == -1:
					break

				newmask = self.swapChar(newmask, lastAsterik, combo[i])
			
			# fill the blanks with the permutations
			for x in range(len(charPerms)):
				permMask = newmask
				lastBlank = -1
				for i in range(len(charPerms[x])):
					lastBlank = permMask.find("_", lastBlank+1)
					
					if lastBlank == -1:
						break

					permMask = self.swapChar(permMask, lastBlank, charPerms[x][i])

				# check if permMask is a dictionary word
				if self.dictionary.is_word(permMask):
					self.outwords[permMask] = 1
		
		return self.outwords.keys()
			
if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print "Usage: anagram <mask> <list_of_letters> [<dictionary_file>]"
		sys.exit(1)

	mask = sys.argv[1].lower()
	chars = sys.argv[2].lower()
	dicfile = "dictionaries/english"
	if len(sys.argv) >= 4:
		dicfile = sys.argv[3]
	dictionary = Dictionary(dicfile)

	ags = AnagramSolver(dictionary)

	wordlist = ags.anagram(mask, chars)
	wordlist.sort(lambda x,y: cmp(len(x),len(y)))
	print '\n'.join(wordlist)

