#!/usr/bin/env python

class Dictionary:
	def __init__(self, file='dictionaries/english'):
		self.words = {}
		for word in open(file).read().split('\n'):
			self.words[word] = True
	
	def is_word(self, word):
		return self.words.has_key(word)

