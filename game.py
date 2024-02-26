from board import Board
import pygame

class Game:
    
    def __init__(self, board_size):
        self.board = Board(board_size)

    def toggle_cell(self, row, col):
        self.board.board[row][col] = not self.board.board[row][col]

    def draw_board(self, screen, cell_size, images):

        border = images[3]

        screen.blit(border, (0, 0))

        screen.blit(border, ((self.board.getBoardSize() + 1) * cell_size, (self.board.getBoardSize()+1) * cell_size))

        screen.blit(border, (0 * cell_size, (self.board.getBoardSize()+1) * cell_size))

        screen.blit(border, ((self.board.getBoardSize() + 1) * cell_size, 0))

        for row in range(1, self.board.getBoardSize() + 1):
            arrow = images[2]
            rotated_arrow = pygame.transform.rotate(arrow, 90)  # Rotate the arrow by 90 degrees
            screen.blit(rotated_arrow, (0, row * cell_size))
            
            rotated_arrow = pygame.transform.rotate(arrow, 270)  # Rotate the arrow by 270 degrees
            screen.blit(rotated_arrow, ((self.board.getBoardSize() + 1) * cell_size, row * cell_size))
            
            rotated_arrow = pygame.transform.rotate(arrow, 0)  # Rotate the arrow by 180 degrees
            screen.blit(rotated_arrow, (row * cell_size, 0))
            
            rotated_arrow = pygame.transform.rotate(arrow, 180)  # Rotate the arrow by 180 degrees
            screen.blit(rotated_arrow, (row * cell_size, (self.board.getBoardSize() + 1) * cell_size))


        
        for row in range(self.board.getBoardSize()):
            for col in range(self.board.getBoardSize()):
                cell_image = images[1] if self.board.board[row][col] else images[0]
                screen.blit(cell_image, ((col + 1) * cell_size, (row + 1) * cell_size))
