from bot import Bot
import pygame
from sound import Sound
from queue import PriorityQueue

class AStar(Bot):
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
            print(f"[LOG] Bot Marley made move on row -1 and column -1")

        came_from, _ = self.a_star()

        current = self.game
        i = 0
        while current.board.board != self.game.board.board:
            print(f"Working {i}")
            i += 1
            self.board_sequence.append(current)
            current = came_from[current.board]
        
        self.board_sequence.append(current)

        self.board_sequence.reverse()

        for game in self.board_sequence:
            move_caller(game)

        return

    def a_star(self):
        frontier = PriorityQueue()
        frontier.put((0, self.game))
        came_from = {}
        cost_so_far = {self.game: 0}

        while not frontier.empty():
            print(int(frontier.qsize()))
            _, current = frontier.get()

            print(current.board)

            if current.board.isWinningBoard():
                break

            valid_moves = current.valid_moves()
            for next_node in valid_moves:
                new_cost = cost_so_far[current] + 1

                if (next_node.board == current.board):
                    new_cost = float('inf')

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic_func(next_node.board)
                    frontier.put((priority, next_node))
                    came_from[next_node.board] = current

        return came_from, cost_so_far

    def find_difference(self, board1, board2):
        for row in range(len(board1)):
            for col in range(len(board1)):
                if board1[row][col] != board2[row][col]:
                    return row, col
