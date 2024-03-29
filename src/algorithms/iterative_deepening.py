from bot import Bot
import pygame
from sound import Sound
import threading

class Node:
    def __init__(self, game, depth, parent=None, move=None):
        self.game = game
        self.depth = depth
        self.parent = parent
        self.move = move

class IterativeDeepening(Bot):
    def __init__(self, game, move_list=[]):
        super().__init__(game)
        self.move_list = move_list

    def make_move(self):
        if self.game.is_moving or not self.game.level_active:
            return
        
        if self.move_list == []:
            self.move_list = self.iterative_deepening()

        def move_caller():
            self.game.is_moving = True
            pygame.time.delay(100)

            print(self.move_list[0])

            row, col = self.move_list[0]
            self.game.make_move(row, col)
            self.move_list.pop(0)
            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving = False
            
            print(f"[LOG] Bot Marley made move on row {row} and column {col}")


        move_thread = threading.Thread(target=move_caller)
        move_thread.start()
            
    def iterative_deepening(self):
        max_depth = 0

        while True:
            solution = self.dfs(max_depth)
            if solution:
                print(solution)
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