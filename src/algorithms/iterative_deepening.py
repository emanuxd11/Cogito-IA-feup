from bot import Bot
import pygame
from sound import Sound
from collections import deque

class Node:
    def __init__(self, game, depth, parent=None, move=None):
        self.game = game
        self.depth = depth
        self.parent = parent
        self.move = move

class IterativeDeepening(Bot):
    def __init__(self, game):
        super().__init__(game)
        self.board_sequence = []

    def make_move(self):
        if self.game.is_moving or not self.game.level_active:
            return

        def move_caller(newGame):
            self.game.is_moving = True
            pygame.time.delay(100)
            self.game = newGame
            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving = False
            # print(f"[LOG] Bot Marley made move on row {row} and column {col}")

        came_from = self.iterative_deepening()

        print(came_from)

        current = self.game

        #ajustar isto

        while current.board.board != self.game.board.objective:
            self.board_sequence.append(current.board)
            current = came_from[current]
        
        self.board_sequence.append(current.board)

        self.board_sequence.reverse()

        for game in self.board_sequence:
            move_caller(game)
            
    def iterative_deepening(self):
        max_depth = 0

        while True:
            solution = self.dfs(max_depth)
            if solution:
                return solution 
            
            max_depth += 1

    
    #returns solution sequence if found, else false
    def dfs(self, max_depth):
        frontier = []
        root = Node(self.game, 0)
        frontier.append(root)

        while frontier:
            current = frontier.pop()

            print(current.game.board)
            print(current.move)

            if current.game.board.isWinningBoard():
                return self.build_solution(current) 
            
            if current.depth > max_depth:
                return False
            
            valid_moves = current.game.valid_moves()
            for next_node in valid_moves:
                game, move = next_node
                if game.board != current.game.board:
                    node = Node(game, current.depth + 1, current, move)
                    frontier.append(node)
                
        return False
    
    def build_solution(node):
        solution = []

        while node.parent is not None:
            solution.append(node.move)

            node = node.parent

        return solution.reverse()