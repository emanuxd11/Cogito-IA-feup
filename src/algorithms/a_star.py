from bot import Bot
import pygame
from sound import Sound
from queue import PriorityQueue
import threading
from board import Board

class Node:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move

    def __lt__(self, other):
        return self.game.board < other.game.board

class AStar(Bot):
    def __init__(self, game, heuristic_func):
        super().__init__(game)
        self.heuristic_func = heuristic_func
        self.came_from = {}
        self.move_sequence = []
        self.tree = []

    def make_move(self):

        if self.game.is_moving or not self.game.level_active:
            return

        if not self.came_from:
            self.move_sequence = self.a_star()
            print(self.move_sequence)
            """
            current_board = Board(9)
            current_board.board = self.gamecopy.board.objective.copy()
            while self.gamecopy.board.board != current_board.board:
                print("--------------------------")
                print(current_board)
                next_board, move = self.came_from[current_board]
                print(next_board.board)
                print(move)

                temp = Board(9)
                temp.board = next_board.board.board.copy()
                current_board = temp
                self.move_sequence.append(move)
            self.move_sequence.reverse()
            """
        
        def move_caller():
            self.game.is_moving = True
            pygame.time.delay(100)
            print(self.move_sequence)
            if self.move_sequence:
                row, col = self.move_sequence[0]
                self.move_sequence = self.move_sequence[1:]
                self.game.make_move(row, col)
                print(f"[LOG] Moved ({row}, {col})")
            else:
                print("[LOG] No more moves in sequence")

            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving = False

        move_thread = threading.Thread(target=move_caller)
        move_thread.start()
        
    def a_star(self):
        frontier = PriorityQueue()
        initial_node = Node(self.game)
        self.tree.append(initial_node)
        frontier.put((0, initial_node))
        cost_so_far = {initial_node.game.board: 0}

        while not frontier.empty():
            print(int(frontier.qsize()))  # Track queue size for debugging
            _, current = frontier.get()

            print(current.game.board)

            if current.game.board.isWinningBoard():
                return self.construct_path(current)
                break

            valid_moves = current.game.valid_moves()
            for next_node in valid_moves:
                node_game, move = next_node
                new_cost = cost_so_far[current.game.board] + 1

                if node_game.board == current.game.board:
                    new_cost = float('inf')  # Penalize revisiting same state
                    

                if node_game.board not in cost_so_far or new_cost < cost_so_far[node_game.board]:
                    cost_so_far[node_game.board] = new_cost
                    priority = new_cost + self.heuristic_func(node_game.board)
                    new_node = Node(node_game, current, move)
                    frontier.put((priority, new_node))
                    self.tree.append(new_node)
                    #came_from[node_game.board] = (current, move)

        return new_node

    def construct_path(self, node):
        path = []
        while node.parent:
            path.append(node.move)
            node = node.parent
        path.reverse()
        return path