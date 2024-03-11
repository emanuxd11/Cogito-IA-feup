import random
import threading
import pygame

from sound import Sound


class Bot:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        pass

class RandomBot(Bot):
    def make_move(self):
        # wait for the game to be ready to make another move
        if self.game.is_moving or not self.game.level_active:
            return

        row, col = self.pick_move()

        def move_caller():
            self.game.is_moving= True
            pygame.time.delay(100)
            self.game.make_move(row, col)
            Sound.playMoveSound()
            self.game.move_count += 1
            print(f"Bot Marley made move on row {row} and column {col}")
            self.game.is_moving= False

        if self.game.level_active:
            move_thread = threading.Thread(target=move_caller)
            move_thread.start()

    def pick_move(self):
        orientation = random.choice(["vertical", "horizontal"])

        if orientation == "vertical":
            row = random.choice([0, 10])
            col = random.randint(1, 9)
        else:
            row = random.randint(1, 9)
            col = random.choice([0, 10])

        return row, col

class WhateverBot(Bot):
    def make_move(self):
        # implement
        pass

