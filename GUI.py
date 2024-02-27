import pygame
import sys

from game import Game


class GUI:

    cell_images = [
        pygame.image.load("img/square.jpg"),
        pygame.image.load("img/circle.jpg"),
        pygame.image.load("img/arrow.jpg"),
        pygame.image.load("img/border.jpg")
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
            last_shift_time = pygame.time.get_ticks()  # Track the last time the board shifted

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        row = y // self.cell_size
                        col = x // self.cell_size
                        self.game.toggle_cell(row, col)

                # Check if 2 seconds have elapsed since the last shift
                current_time = pygame.time.get_ticks()
                if current_time - last_shift_time >= 2000:  # 2000 milliseconds = 2 seconds
                    # self.game.board.rotateRowRight(7)
                    # self.game.board.rotateRowLeft(3)
                    # self.game.board.rotateColumnUp(2)
                    # self.game.board.rotateColumnDown(8)
                    last_shift_time = current_time  # Update the last shift time

                self.game.draw_board(self.screen, self.cell_size, self.cell_images)
                pygame.display.flip()

                clock.tick(10)

            pygame.quit()
            sys.exit()
