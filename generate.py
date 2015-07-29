#!/usr/bin/env python3
from string import ascii_letters;
from random import choice;

#target string: Evolution (A total of 26 ^ 9 = 5429503678976 possible combinations of alphabets)
examples = [];
while (not len (examples) == 90000):
	randString = '';
	for j in range (0, 9):
		randString += choice (ascii_letters).lower ();

	if (examples.count (randString) == 0):
		examples.append (randString);
		print (randString);
