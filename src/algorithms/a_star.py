from bot import Bot
import pygame
from sound import Sound
from queue import PriorityQueue
import threading

class AStar(Bot):
    def __init__(self, game, heuristic_func):
        super().__init__(game)
        self.heuristic_func = heuristic_func
        self.came_from = {}

    def make_move(self):

        if self.game.is_moving or not self.game.level_active:
            return

        move_sequence = []
        if not self.came_from:
            self.came_from, _ = self.a_star()
            print(self.came_from)
            current_board = self.game
            while not self.game.board.board == current_board.board.objective:
                print(current_board.board)
                next_board, move = self.came_from[current_board.board]
                current_board = next_board
                move_sequence.append(move)
            move_sequence.reverse()

        def move_caller():
            self.game.is_moving = True
            pygame.time.delay(10)

            if move_sequence:
                row, col = move_sequence.pop(0)
                self.game.make_move(row, col)
            else:
                print("[LOG] No more moves in sequence")

            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving = False

        move_thread = threading.Thread(target=move_caller)
        move_thread.start()

    def a_star(self):
        frontier = PriorityQueue()
        frontier.put((0, self.game))
        came_from = {}
        cost_so_far = {self.game: 0}

        while not frontier.empty():
            print(int(frontier.qsize()))  # Track queue size for debugging
            _, current = frontier.get()

            print(current.board)

            if current.board.isWinningBoard():
                break

            valid_moves = current.valid_moves()
            for next_node in valid_moves:
                node_game, move = next_node
                new_cost = cost_so_far[current] + 1

                if node_game.board == current.board:
                    new_cost = float('inf')  # Penalize revisiting same state

                if node_game not in cost_so_far or new_cost < cost_so_far[node_game]:
                    cost_so_far[node_game] = new_cost
                    priority = new_cost + self.heuristic_func(node_game.board)
                    frontier.put((priority, node_game))
                    came_from[node_game.board] = (current, move)

        return came_from, cost_so_far

    def find_difference(self, board1, board2):
        for row in range(len(board1)):
            for col in range(len(board1)):
                if board1[row][col] != board2[row][col]:
                    return row, col
