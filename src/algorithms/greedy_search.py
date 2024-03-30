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

class GreedySearch(Bot):
    def __init__(self, game, heuristic_func):
        super().__init__(game)
        self.heuristic_func = heuristic_func
        self.move_sequence = []
        self.tree = []

    def make_move(self):
        if self.game.is_moving or not self.game.level_active:
            return

        if not self.move_sequence:
            self.move_sequence = self.greedy_search()

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
        
    def greedy_search(self):
        frontier = PriorityQueue()
        initial_node = Node(self.game)
        self.tree.append(initial_node)
        frontier.put((0, initial_node))

        while not frontier.empty():
            _, current = frontier.get()
            print(current.game.board)
            if current.game.board.isWinningBoard():
                return self.construct_path(current)
                break

            valid_moves = current.game.valid_moves()
            for next_node in valid_moves:
                node_game, move = next_node

                # Calculate priority based only on the heuristic function
                priority = self.heuristic_func(node_game.board)

                if node_game.board == current.game.board:
                    priority = float('inf')  # Penalize revisiting same state

                new_node = Node(node_game, current, move)
                frontier.put((priority, new_node))
                self.tree.append(new_node)

        return []

    def construct_path(self, node):
        path = []
        while node.parent:
            path.append(node.move)
            node = node.parent
        path.reverse()
        return path
