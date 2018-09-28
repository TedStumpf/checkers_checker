#   lin_analyzer.py
#   Theodore Stumpf
#   A linear analyzer for a checkers game board
from random import random as rand
from random import choice

#   The LinearAnalyzer is used to enhance the min-max algorithm
class LinearAnalyzer:

    #   __init__():  Initialize the LinearAnalyzer
    #   make_random: When make_random is False, the LinearAnalyzer will
    #       use the default values for its analysis
    def __init__(self, make_random = False):
        if (make_random):
            #   Fill our data with random values
            piece = [rand(), rand(), rand(), rand()]
            board = [rand() for i in range(32)]
            self.data = [piece, board]
        else:
            #   Use the default values
            piece = [0.3, 1, 0.3, 1]
            board = [1 for i in range(32)]
            self.data = [piece, board]


    #   mutate():      Mutates the LinearAnalyzer in place
    #   mutate_chance: The decimal percentage chance of a data point being changed
    #   mutate_scale:  The maximum ammount to change by
    #   NOTE: Data values are clamped between 0 and 1
    def mutate(self, mutate_chance = 0.1, mutate_scale = 1):
        for sec in range(len(self.data)):
            for i in range(len(self.data[sec])):
                if (rand() < mutate_chance):
                    self.data[sec][i] = min(1, max(0, self.data[sec][i] + mutate_scale * rand() * choice(-1, 1)))

    #   merge():      Merges this LinearAnalyzer with another one, returns the new LinearAnalyzer
    #   other_par:    The other LinearAnalyzer to merge with
    #   parent_split: What percentage of the child LinearAnalyzer comes from the other parent
    def merge(self, other_par, parent_split = 0.5):
        child = LinearAnalyzer()
        for sec in range(len(self.data)):
            for i in range(len(self.data[sec])):
                if (rand() < parent_split):
                    #   The child draws from the other parent
                    child.set_raw_data(sec, i, other_par.get_raw_data(sec, i))
                else:
                    #   The child draws from this parent
                    child.set_raw_data(sec, i, self.get_raw_data(sec, i))
        return child

    #   get_raw_data(): Return the data for a certain section
    #   section: What section are we getting the data from
    #   index:   What entry we are accessing
    def get_raw_data(self, section, index):
        return self.data[section][index]

    #   set_raw_data(): Sets the data for a certain section
    #   section: What section are we getting the data from
    #   index:   What entry we are accessing
    #   value:   The value that we will set the data to
    def set_raw_data(self, section, index, value):
        self.data[section][index] = value

    #   get_friendly_man(): Returns the weighted value of a friendly man
    def get_friendly_man(self):
        return self.get_raw_data(0, 0)

    #   get_friendly_king(): Returns the weighted value of a friendly king
    def get_friendly_king(self):
        return self.get_raw_data(0, 1)

    #   get_enemy_man(): Returns the weighted value of a enemy man
    def get_enemy_man(self):
        return self.get_raw_data(0, 2)

    #   get_enemy_king(): Returns the weighted value of a enemy king
    def get_enemy_king(self):
        return self.get_raw_data(0, 3)

    #   get_square_value(): Returns the weighted value of a given square on the board
    #   row, column: The cordinates of the square on the board
    def get_square_value(self, row, column):
        index = column // 2 + 4 * row
        return self.get_raw_data(1, index)
