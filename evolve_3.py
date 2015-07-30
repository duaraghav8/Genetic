#!/usr/bin/env python3
from string import ascii_letters;
from random import choice, randint;

class Trainer:
	def __init__ (self, population, threshold, fitnessFunc, mutation, crossover):
		self.population = population
		self.threshold = threshold
		self.fitness = fitnessFunc
		self.mutation = mutation
		self.cross = crossover

		self.crossMask = '111100000';	#this is AD HOC, aka, bad practice


	def evolve (self):
		nextGen = [];
		sortedPop = [];
		crossMask = '';

		while (True):
			fitnesses = [self.fitness (i) for i in self.population];
			print (max (fitnesses));
#			uncomment the line above if you wish to see the progress of the fitness. It rises to 0.778 (best fitness is 1, which is the target word) and then stops improving.
			sortedPop = [i for (h, i) in sorted (zip (fitnesses, self.population))];
			fitnesses.sort ();

			sortedPop.reverse ();
			fitnesses.reverse ();
			print (sortedPop [0]);

			if (max (fitnesses) >= self.threshold):
                                print ("Hypothess found: ", sortedPop [fitnesses.index (max (fitnesses))]);
                                break;

			fraction = int (((100 - self.cross) / 100) * len (fitnesses));
			nextGen = sortedPop [ : fraction];

			#CROSSOVER
			fraction = int ((self.cross / 100) * len (fitnesses));
			if (not fraction % 2 == 0):
				fraction -= 1;

			for i in range (0, fraction, 2):
				p1 = sortedPop [i];
				p2 = sortedPop [i + 1];

				#offspring = p1 [ : 4] + p2 [4 : ];
				offspring = '';
				for j in range (0, len (p1)):
					x = randint (1, 2);
					if (x == 1):
						offspring += p1 [j];
					else:
						offspring += p2 [j];

				nextGen.append (offspring);

			#MUTATION
			fraction = int ((self.mutation / 100) * len (fitnesses));
			for i in range (0, fraction):
				nextGen [i] = nextGen [i].replace (choice (nextGen [i]), choice (ascii_letters), 1);
				
			self.population = nextGen;

def fitnessFunc (caseString):
	global targetString;
	counter = 0;

	for i in range (0, len (targetString)):
		if (caseString [i] == targetString [i]):
			counter += 1;

	return ( counter / len (targetString));

if (__name__ == '__main__'):
	population = [i.rstrip () for i in open ('population', 'r').readlines ()];
	targetString = 'Evolution';
	threshold = 1;
	mutation = 10;		#given in percentage form
	crossover = 60;		#percentage

	t = Trainer (population, threshold, fitnessFunc, mutation, crossover);
	t.evolve ();
