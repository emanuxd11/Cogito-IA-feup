from board import Board
import pygame

class Game:
    
    def __init__(self, board_size):
        self.board = Board(board_size)

    def toggle_cell(self, row, col):
        self.board.board[row][col] = not self.board.board[row][col]

    def draw_board(self, screen, cell_size, images):
        for row in range(self.board.getBoardSize()):
            for col in range(self.board.getBoardSize()):
                cell_image = images[1] if self.board.board[row][col] else images[0]
                screen.blit(cell_image, ((col + 1) * cell_size, (row + 1) * cell_size))
