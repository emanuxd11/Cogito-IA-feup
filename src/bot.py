import pygame


# Define a strategy interface or base class
class BotMode:
    def make_move(self):
        pass

# Concrete implementations of different modes
class RandomMode(BotMode):
    def make_move(self):
        # Implement random move logic
        pass

# Define the Bot class
class Bot:
    def __init__(self, mode):
        self.mode = mode

    def make_move(self, game):
        self.mode.make_move(game)

