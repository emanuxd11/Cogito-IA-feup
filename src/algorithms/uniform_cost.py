from bot import Bot
import pygame
from sound import Sound
import heapq
from queue import PriorityQueue


class UniformCost(Bot):

    def make_move(self):

        if self.game.is_moving or not self.game.level_active:
            return

        def move_caller():
            
            moves = self.valid_moves()

            self.game.is_moving= True
            pygame.time.delay(100)

            self.game.make_move(row, col)
            Sound.playMoveSound()
            self.game.move_count += 1
            self.game.is_moving= False

            print(f"[LOG] Bot Marley made move on row {row} and column {col}")

        self.uniform_cost()
        #row, col = self.pick_move()
        #move_thread = threading.Thread(target=move_caller)
        #move_thread.start()

    
    def uniform_cost(self):
        
        frontier = PriorityQueue()
        frontier.put((0, self.game))
        came_from = {}
        cost_so_far = {self.game: 0}
        queue_size = 1 
        
        while queue_size > 0:
            _, current = frontier.get()

            queue_size -= 1

            if current.board.isWinningBoard():
                break
            
            # print(f"Valid Moves Size {len(self.valid_moves())}")

            valid_moves = current.valid_moves()

            i = 0

            for next_node in valid_moves:

                if (next_node.board == current.board):
                    new_cost = cost_so_far[current] + 1000

                else:
                    new_cost = cost_so_far[current] + 1

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    print(next_node.board)
                    cost_so_far[next_node] = new_cost
                    priority = new_cost
                    frontier.put((priority, next_node))
                    came_from[next_node] = current
                    queue_size += 1 

        return came_from, cost_so_far