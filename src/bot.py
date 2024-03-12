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

        def move_caller():
            self.game.is_moving= True
            pygame.time.delay(100)

            self.game.make_move(row, col)
            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving= False

            print(f"[LOG] Bot Marley made move on row {row} and column {col}")

        row, col = self.pick_move()
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

class ListBot(Bot):
    # This bot calculates a list af moves to get him to the victory position
    def __init__(self, game, move_list=[]):
        super().__init__(game)
        self.move_list = move_list 

    def make_move(self):
        if self.game.is_moving or not self.game.level_active:
            return

        if self.move_list == []:
            self.calculate_moves()

        def move_caller():
            self.game.is_moving = True
            pygame.time.delay(100)

            row, col = self.move_list[0]
            self.game.make_move(row, col)
            self.move_list.pop(0)
            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving= False

            print(f"[LOG] Bot Wyatt made move on row {row} and column {col}")

        move_thread = threading.Thread(target=move_caller)
        move_thread.start()

    def calculate_moves(self):
        for _ in range(50):
            self.move_list.append(self.pick_random_move())

    # temporary thing just to test initializing a moves list and playing moves from it
    def pick_random_move(self):
        orientation = random.choice(["vertical", "horizontal"])

        if orientation == "vertical":
            row = random.choice([0, 10])
            col = random.randint(1, 9)
        else:
            row = random.randint(1, 9)
            col = random.choice([0, 10])

        return row, col

