import pygame

from game import Game
from sound import Sound 


class GUI:

    cell_images = [
        pygame.image.load("../img/square.jpg"),
        pygame.image.load("../img/circle.jpg"),
        pygame.image.load("../img/arrow.jpg"),
        pygame.image.load("../img/border.jpg")
    ]

    def __init__(self, board_size=9, cell_size=70):
        self.cell_size = cell_size
        self.width = board_size * cell_size
        self.height = board_size * cell_size
        self.screen = pygame.display.set_mode((self.width + 2 * cell_size, self.height + 2 * cell_size))
        pygame.display.set_caption("Cogito")
        self.cell_images = [
            pygame.transform.scale(image, (cell_size, cell_size)) for image in GUI.cell_images
        ]
        self.game = Game(board_size)
        self.clock = pygame.time.Clock()

    def run(self):
        Sound.playBackgroundTheme()

        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    row = y // self.cell_size
                    col = x // self.cell_size
                    self.game.toggle_cell(row, col)

            # Render the game state
            self.game.draw_board(self.screen, self.cell_size, self.cell_images)
            pygame.display.flip()

            # Update game logic here without waiting for user input
            self.update_game_logic()

            # Cap the frame rate to 60 fps
            # print("rendered frame")
            print(f"fps: {round(self.clock.get_fps())}", end='\r', flush=True)
            self.clock.tick(60)

    def update_game_logic(self):
        # Update game logic here
        # For example, you can handle animations, AI moves, etc.
        if self.game.board.isWinningBoard() and self.game.move_count > 0:
            print(f"You beat level {self.game.level} with {self.game.move_count} moves!")
            self.game.move_count = 0

            Sound.playWinMusic()

            self.game.level += 1
            self.game.board.shuffle(self.game.shuffle_level)
            print(f"you've advanced to level {self.game.level}")

