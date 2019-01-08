#   overseer.py
#   Theodore Stumpf
#	Manages tournaments between contestants
from lin_analyzer import LinearAnalyzer
from random import shuffle

class Overseer():

	def __init__(self, pop_size = 500, batches = 1, top_keep = 0.05, mix_keep = 0.4, new_pop = 0.1, games = 5):
		self.population_size = pop_size
		self.batches = batches
		self.top_keep_perc = top_keep
		self.mix_keep_perc = mix_keep
		self.new_pop_perc = new_pop
		self.games_played = games

		self.generation = 1
		self.tournament_status = 0
		self.population = []

	def create_starting_population(self):
		for i in range(self.population_size):
			self.population.append(LinearAnalyzer(True))