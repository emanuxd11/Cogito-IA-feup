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

    info_board_img = pygame.image.load("../img/info.jpg")

    info_screen_font = "../fonts/digital-font.ttf"

    board_height_start = 130

    def __init__(self, board_size=9, cell_size=65):
        self.cell_size = cell_size
        self.width = board_size * cell_size
        self.height = board_size * cell_size
        self.screen = pygame.display.set_mode((self.width + 2 * cell_size, GUI.board_height_start + self.height + 2 * cell_size)) # adding some extra height for testing
        pygame.display.set_caption("Cogito")
        self.cell_images = [
            pygame.transform.scale(image, (cell_size, cell_size)) for image in GUI.cell_images
        ]
        self.game = Game(board_size)
        self.clock = pygame.time.Clock()

        # Initialize font for rendering text
        pygame.font.init()
        self.font = pygame.font.Font("../fonts/digital-7-mono.ttf", 34)  # Choose your font and size

    def run(self):
        Sound.playBackgroundTheme()

        running = True
        while running:
            self.game.updateLogic()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    row = (y - GUI.board_height_start) // self.cell_size
                    col = x // self.cell_size
                    self.game.toggle_cell(row, col)

            # reset display to all black (prevents ghosting)
            self.screen.fill((0, 0, 0))

            # render board
            self.game.board.draw(self.screen, self.cell_size, self.cell_images, GUI.board_height_start)

            # render the info boar
            self.renderInfoBoard()

            # apply changes
            pygame.display.flip()

            # print(f"Level: {self.game.level} Moves: {self.game.move_count} FPS: {round(self.clock.get_fps())}", end='\r', flush=True) # just for debug while there is no GUI indicator
            # Cap the frame rate to 60 fps
            self.clock.tick(999999)

    # utils

    def render_text(self, text, position, color=(255, 255, 255)):
        rendered_text = self.font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def resizeImage(self, image, factor):
        orig_width = image.get_width()
        orig_height = image.get_height()

        new_width = orig_width * factor
        new_height = orig_height * factor

        return pygame.transform.scale(image, (new_width, new_height))

    def renderInfoBoard(self):
        # resize the board
        board = self.resizeImage(GUI.info_board_img, 0.55)

        # position the board itself
        self.screen.blit(board, (230, 7))

        # current level timer
        level_timer = self.game.getTimeString()
        self.render_text(level_timer, (258, 15), pygame.Color("red"))

        # current level
        level_text = f"{self.game.level:03}"
        self.render_text(level_text, (247, 47), pygame.Color("yellow"))

        # current shuffle level
        shuffle_qnt = f"{self.game.shuffle_level:03}"
        self.render_text(shuffle_qnt, (341, 47), pygame.Color("yellow"))

        # current number of moves
        moves_text = f"{self.game.move_count:05}"
        self.render_text(moves_text, (280, 78), pygame.Color("red"))

