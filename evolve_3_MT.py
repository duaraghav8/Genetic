#!/usr/bin/env python3
#
#UNDER CONSTRUCTION
#
#
#A replica of evolve_3.py with the difference that this one exploits Multithreading for better performance.
#The Fitness Testing of the chromosomes takes place in parallel.
from string import ascii_letters;
from random import choice, randint;
import _thread as thread;

class Trainer:
	def __init__ (self, population, threshold, fitnessFunc, mutation, crossover):
		self.population = population
		self.threshold = threshold
		self.fitness = fitnessFunc
		self.mutation = mutation
		self.cross = crossover

	def evolve (self):
		nextGen = [];
		sortedPop = [];
		crossMask = '';

		while (True):
#			fitnesses = [self.fitness (i) for i in self.population];
#the above is what we used in evolve_3.py

			fitnesses = [];
			for chromosome in self.population:
				response = thread.start_new_thread (self.fitness, (chromosome, fitnesses));

			print (max (fitnesses));
#			comment the line above if do not you wish to see the progress of the fitness.
			sortedPop = [i for (h, i) in sorted (zip (fitnesses, self.population))];	#All chromosomes are sorted in decreasing order of their fitness. The replication, crossover and mutation - all happen from top down. So if crossover rate is 60%, we take top 60% of the chromosomes
			fitnesses.sort ();

			sortedPop.reverse ();
			fitnesses.reverse ();
			print (sortedPop [0]);

			if (max (fitnesses) >= self.threshold):
                                print ("Hypothess found: ", sortedPop [fitnesses.index (max (fitnesses))]);
                                break;

			fraction = int (((100 - self.cross) / 100) * len (fitnesses));	#fraction of population which is to be simply replicated into the next generation
			nextGen = sortedPop [ : fraction];

			#CROSSOVER
			#Extremely important to notice that I am only generating 1 offspring from the crossover. If I generate 2 and keep the rest of the process similar, it still gives me the correct answer but after 19 generations (double the time)
			fraction = int ((self.cross / 100) * len (fitnesses));	#fraction of population to be used for reproduction (this number MUST be even because reproduction will happen in pairs)
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
			fraction = int ((self.mutation / 100) * len (fitnesses));	#fraction of population to undergo mutation before being transmitted to the next generation
			for i in range (0, fraction):
				nextGen [i] = nextGen [i].replace (choice (nextGen [i]), choice (ascii_letters), 1);
				
			self.population = nextGen;

def fitnessFunc (caseString, fitnesses):
	global targetString;
	counter = 0;

	for i in range (0, len (targetString)):
		if (caseString [i] == targetString [i]):
			counter += 1;

	fitnesses.append (counter / len (targetString));

if (__name__ == '__main__'):
	population = [i.rstrip () for i in open ('population', 'r').readlines ()];
	targetString = 'Evolution';
	threshold = 1;
	mutation = 10;		#given in percentage form
	crossover = 60;		#percentage

	t = Trainer (population, threshold, fitnessFunc, mutation, crossover);
	t.evolve ();

