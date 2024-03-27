from bot import Bot
import pygame
from sound import Sound

class GreedySearch(Bot):
    def __init__(self, game, heuristic_func):
        super().__init__(game)
        self.heuristic_func = heuristic_func
        self.board_sequence = []

    def make_move(self):
        if self.game.is_moving or not self.game.level_active:
            return

        def move_caller(newGame):
            self.game.is_moving = True
            pygame.time.delay(100)
            self.game.board = newGame.board
            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving = False
            print(f"[LOG] Bot made move on row -1 and column -1")

        current = self.game
        while not current.board.isWinningBoard():
            valid_moves = current.valid_moves()
            next_node = min(valid_moves, key=lambda node: self.heuristic_func(node.board))
            self.board_sequence.append(next_node)
            current = next_node

        for game in self.board_sequence:
            move_caller(game)
