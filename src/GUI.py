import pygame
import sys

from game import Game
from sound import Sound 


class GUI:

    cell_images = [
        pygame.image.load("../img/square.jpg"),
        pygame.image.load("../img/circle.jpg"),
        pygame.image.load("../img/arrow.jpg"),
        pygame.image.load("../img/border.jpg")
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
            Sound.playBackgroundTheme()

            clock = pygame.time.Clock()
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #only accept left clicks
                        x, y = pygame.mouse.get_pos()
                        row = y // self.cell_size
                        col = x // self.cell_size
                        self.game.toggle_cell(row, col)

                self.game.draw_board(self.screen, self.cell_size, self.cell_images)
                pygame.display.flip()
                clock.tick(10)

                if self.game.board.isWinningBoard() and self.game.move_count > 0:
                    print(f"You Beat Level {self.game.level} With {self.game.move_count} moves!")
                    self.game.move_count = 0

                    Sound.playWinMusic()

                    self.game.level += 1
                    self.game.board.shuffle(self.game.shuffle_level)
                    # presumably here you would also increment the shuffle level at some point but I haven't yet figured out how that works 
                    print(f"you've advanced to level {self.game.level}")

            pygame.quit()
            sys.exit()

