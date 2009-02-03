#!/usr/bin/env python

import sys
import string

min_wd_size = 3
outwords = {}

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

def get_combos(letters):
	check_words(letters, 0)
	check_length(letters)


def wild(str, num_wild):
	if num_wild > 0:
		return [y + x for x in string.lowercase for y in wild(str, num_wild-1)]
	else:
		return [str]





if len(sys.argv) <= 1:
	print "Usage: anagram <list_of_letters> [<dictionary_file>]"
	sys.exit(1)

chars = sys.argv[1].lower()
dicfile = "dictionaries/english"
if len(sys.argv) >= 4:
	dicfile = sys.argv[2]

# read dictionary words into hash
dicwords = {}
for word in open(dicfile).read().split('\n'):
	dicwords[word] = 1

# get a list of possible words to use. combine tray letters one at a time
# with every letter in the alphabet
num_wild = chars.count('*')
chars = chars.replace('*','')

print "generating possible words..."
x = 0
combos = wild(chars, num_wild)
max = len(combos)
for combo in combos:
	print "%i / %i done" % (x, max)
	get_combos(combo)
	x += 1
	
wordlist = outwords.keys()
wordlist.sort(lambda x,y: cmp(len(y),len(x)));
print '\n'.join(wordlist)

