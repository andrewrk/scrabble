#!/usr/bin/env python

import sys
import string

min_wd_size = 3
outwords = {}
permutations = {}

def read_board(file):
	return filter(lambda x: len(x)==0 or x[0] != '#', open(file).read().split('\n'))

def check_length(word):
	# for each letter remove it and call check_length on each one
	for i in range(len(word)):
		tmp = word[:i] + word[i+1:]
		
		if len(tmp) >= min_wd_size:
			check_words(tmp, 0)
			check_length(tmp)

def check_words(word, i):
	while i<len(word):
		# try it with letter[i] switched with all next letters
		for j in range(i, len(word)):
			test = swap(word, i, j)
			if dicwords.has_key(test):
				outwords[test] = 1
			if i < len(word) - 1:
				check_words(test, i+1)
		i += 1

def swap(word, i, j):
	wlist = list(word)
	tmp = wlist[i]
	wlist[i] = wlist[j]
	wlist[j] = tmp
	return ''.join(wlist)

def swapChar(word, index, char):
	wlist = list(word)
	wlist[index] = char
	return ''.join(wlist)

def get_combos(letters):
	check_words(letters, 0)
	check_length(letters)

def get_permutations(word):
	permutations = {}
	return get_permutations_rec(word, 0)

def get_permutations_rec(word, i):
	while i<len(word):
		# try it with letter[i] switched with all next letters
		for j in range(i, len(word)):
			test = swap(word, i, j)
			permutations[test] = 1
			if i < len(word) - 1:
				get_permutations_rec(test, i+1)
		i += 1
	
	return permutations.keys()
	

def wild(str, num_wild):
	if num_wild > 0:
		return [y + x for x in string.lowercase for y in wild(str, num_wild-1)]
	else:
		return [str]

def anagram(mask, chars):
	# mask is of the form: e__ph_*t
	# where lower case letters are literal, underscores can
	# be filled in with chars from chars, and asterisks
	# can be filled with any character a-z

	# clear the output hash
	outwords = {}
	# get the list of wildcard possibilities
	combos = wild('', mask.count('*'))
	# get the list of character permutations
	charPerms = get_permutations(chars)
	# do anagram for each wildcard possibility
	for combo in combos:
		newmask = mask
		lastAsterik = -1
		
		for i in range(len(combo)):
			lastAsterik = newmask.find("*", lastAsterik+1)

			if lastAsterik == -1:
				break

			newmask = swapChar(newmask, lastAsterik, combo[i])
		
		# fill the blanks with the permutations
		for x in range(len(charPerms)):
			permMask = newmask
			lastBlank = -1
			for i in range(len(charPerms[x])):
				lastBlank = permMask.find("_", lastBlank+1)
				
				if lastBlank == -1:
					break

				permMask = swapChar(permMask, lastBlank, charPerms[x][i])

			# check if permMask is a dictionary word
			if dicwords.has_key(permMask):
				outwords[permMask] = 1
	
	return outwords.keys()
		
		


if len(sys.argv) <= 2:
	print "Usage: anagram <mask> <list_of_letters> [<dictionary_file>]"
	sys.exit(1)

mask = sys.argv[1].lower()
chars = sys.argv[2].lower()
dicfile = "dictionaries/english"
if len(sys.argv) >= 4:
	dicfile = sys.argv[3]

# read dictionary words into hash
dicwords = {}
for word in open(dicfile).read().split('\n'):
	dicwords[word] = 1

wordlist = anagram(mask, chars)
wordlist.sort(lambda x,y: cmp(len(x),len(y)))
print '\n'.join(wordlist)

