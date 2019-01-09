#   overseer.py
#   Theodore Stumpf
#   Manages tournaments between contestants
from lin_analyzer import LinearAnalyzer
from board import GameBoard
from random import shuffle, randrange

class Overseer():

    def __init__(self, pop_size = 500, batches = 1, top_keep = 0.05, mix_keep = 0.4, new_pop = 0.1, games = 5):
        self.population_size = pop_size
        self.batches = batches
        self.top_keep_perc = top_keep
        self.mix_keep_perc = mix_keep
        self.new_pop_perc = new_pop
        self.games_played = games

        self.generation = 1
        self.tournament_player = 0
        self.tournament_game = 0
        self.population = []
        self.tournament = []

    def create_starting_population(self):
        for i in range(self.population_size):
            self.population.append(LinearAnalyzer(True))

    def get_tournament_status(self):
        return (self.tournament_player, self.tournament_game)


    def set_up_tournament(self):
        #   Create a list of player IDs
        player_ids = [[i] for i in range(self.population_size)]
        #   Fill out each list
        for brk in player_ids:
            while (len(brk) <= self.games_played):
                n = randrange(self.population_size)
                if (not n in brk):
                    brk.append(n)

        self.tournament = player_ids
        self.tournament_player = 0
        self.tournament_game = 0

    def do_tournament_step(self):
        if (not self.is_tournament_completed()):
            print("Player ", self.tournament[self.tournament_player][0], " vs Player ", 
                    self.tournament[self.tournament_player][self.tournament_game + 1], sep = "", end = ":  ")

            board = GameBoard()
            winner = board.play_game(self.population[self.tournament[self.tournament_player][0]], 
                    self.population[self.tournament[self.tournament_player][self.tournament_game + 1]])
            if (winner == 0):
                print("Draw")
            elif (winner == 1):
                print("Won")
            else:
                print("Lost")
            self.tournament_game += 1
            if (self.tournament_game == self.games_played):
                self.tournament_player += 1
                self.tournament_game = 0
                print()


    def is_tournament_completed(self):
        return (self.tournament_player == self.population_size)

    def get_pop_size(self):
        return self.pop_size

    def get_games_played(self):
        return self.games_played