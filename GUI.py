import pygame
from game import Game
import sys

class GUI:

    cell_images = [
        pygame.image.load("square.jpg"),
        pygame.image.load("circle.jpg"),
        pygame.image.load("arrow.jpg"),
        pygame.image.load("border.jpg")
    ]

    def __init__(self, game, cell_size=70):
        self.game = game
        self.cell_size = cell_size
        self.width = game.board.getBoardSize() * cell_size
        self.height = game.board.getBoardSize() * cell_size
        self.screen = pygame.display.set_mode((self.width+2*cell_size, self.height+2*cell_size))
        pygame.display.set_caption("Cogito")
        self.cell_images = [
            pygame.transform.scale(image, (cell_size, cell_size)) for image in GUI.cell_images
        ]

    def run(self):
        pygame.init()

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // self.cell_size - 1
                    col = x // self.cell_size - 1
                    self.game.toggle_cell(row, col)

            self.game.draw_board(self.screen, self.cell_size, self.cell_images)
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()
        sys.exit()