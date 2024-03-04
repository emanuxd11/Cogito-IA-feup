import pygame

from sound import Sound 


class GUI:

    cell_images = [
        pygame.image.load("../img/square.jpg"),
        pygame.image.load("../img/circle.jpg"),
        pygame.image.load("../img/arrow.jpg"),
        pygame.image.load("../img/border.jpg")
    ]
    info_board_img = pygame.image.load("../img/info.jpg")
    background_img = pygame.image.load("../img/background.jpg")

    board_top_margin = 130
    board_right_margin = 600
    board_bottom_margin = 50
    board_left_margin = 40

    info_screen_font = "../fonts/digital-7-mono.ttf"

    def __init__(self, game, cell_size=65):
        self.game = game

        self.cell_size = cell_size
        self.width = self.game.board.getBoardSize() * cell_size + GUI.board_right_margin + 2 * cell_size
        self.height = GUI.board_top_margin + self.game.board.getBoardSize() * cell_size + GUI.board_bottom_margin + 2 * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.cell_images = [
            pygame.transform.scale(image, (cell_size, cell_size)) for image in GUI.cell_images
        ]

        self.clock = pygame.time.Clock()

        # Initialize font for rendering text
        pygame.font.init()
        self.font = pygame.font.Font(GUI.info_screen_font, 34) # should add other fonts and this would be different then

        pygame.display.set_caption("Cogito")

    def run(self):
        Sound.playBackgroundTheme()

        # rescale it to fit entire screen
        background = pygame.transform.scale(GUI.background_img, (self.width, self.height))

        running = True
        while running:
            self.game.updateLogic()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    row = (y - GUI.board_top_margin) // self.cell_size
                    col = (x - GUI.board_left_margin) // self.cell_size
                    self.game.toggle_cell(row, col)

            # reset display to all black (prevents ghosting)
            self.screen.fill((0, 0, 0))

            # set background image
            self.screen.blit(background, (0, 0))

            # render board
            self.drawBoard()
            self.drawGoalBoard(0.6, 820, 400)

            # render the info board
            self.renderInfoBoard()

            # apply changes
            pygame.display.flip()

            # Cap the frame rate to 60 fps
            self.clock.tick(999999)

    def render_text(self, text, position, color=(255, 255, 255)):
        rendered_text = self.font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def resizeImage(self, image, factor):
        orig_width = image.get_width()
        orig_height = image.get_height()

        new_width = orig_width * factor
        new_height = orig_height * factor

        return pygame.transform.scale(image, (new_width, new_height))

    def renderGoalBoard(self):
        pass

    def drawBoard(self):
        start_height = GUI.board_top_margin
        left_gap = GUI.board_left_margin
        border = self.cell_images[3]
        screen = self.screen
        cell_size = self.cell_size

        screen.blit(border, (0 + left_gap, 0 + start_height))
        screen.blit(border, ((self.game.board.getBoardSize() + 1) * cell_size + left_gap, (self.game.board.getBoardSize() + 1) * cell_size + start_height))
        screen.blit(border, (0 * cell_size + left_gap, (self.game.board.getBoardSize() + 1) * cell_size + start_height))
        screen.blit(border, ((self.game.board.getBoardSize() + 1) * cell_size + left_gap, 0 + start_height))

        for row in range(1, self.game.board.getBoardSize() + 1):
            arrow = self.cell_images[2]
            rotated_arrow = pygame.transform.rotate(arrow, 90)
            screen.blit(rotated_arrow, (0 + left_gap, row * cell_size + start_height))
            rotated_arrow = pygame.transform.rotate(arrow, 270)
            screen.blit(rotated_arrow, ((self.game.board.getBoardSize() + 1) * cell_size + left_gap, row * cell_size + start_height))
            rotated_arrow = pygame.transform.rotate(arrow, 0)
            screen.blit(rotated_arrow, (row * cell_size + left_gap, 0 + start_height))
            rotated_arrow = pygame.transform.rotate(arrow, 180)
            screen.blit(rotated_arrow, (row * cell_size + left_gap, (self.game.board.getBoardSize() + 1) * cell_size + start_height))

        for row in range(self.game.board.getBoardSize()):
            for col in range(self.game.board.getBoardSize()):
                cell_image = self.cell_images[1] if self.game.board.board[row][col] else self.cell_images[0]
                screen.blit(cell_image, ((col + 1) * cell_size + left_gap, (row + 1) * cell_size + start_height))

    def drawGoalBoard(self, scale_factor, x_offset, y_offset):
        start_height = y_offset
        left_gap = x_offset
        screen = self.screen

        board = self.game.board.objective
        board_size = self.game.board.getBoardSize()

        cell_size = int(self.cell_size * scale_factor)
        empty_cell = self.resizeImage(self.cell_images[0], scale_factor)
        filled_cell = self.resizeImage(self.cell_images[1], scale_factor)

        for row in range(board_size):
            for col in range(board_size):
                cell_image = filled_cell if board[row][col] else empty_cell
                screen.blit(cell_image, ((col + 1) * cell_size + left_gap, (row + 1) * cell_size + start_height))

    def renderInfoBoard(self):
        # resize the board
        board = self.resizeImage(GUI.info_board_img, 0.55)

        # position the board itself
        self.screen.blit(board, (230 + GUI.board_left_margin, 7))

        # current level timer
        level_timer = self.game.getTimeString()
        self.render_text(level_timer, (258 + GUI.board_left_margin, 15), pygame.Color("red"))

        # current level
        level_text = f"{self.game.level:03}"
        self.render_text(level_text, (247 + GUI.board_left_margin, 47), pygame.Color("yellow"))

        # current shuffle level
        shuffle_qnt = f"{self.game.shuffle_level:03}"
        self.render_text(shuffle_qnt, (341 + GUI.board_left_margin, 47), pygame.Color("yellow"))

        # current number of moves
        moves_text = f"{self.game.move_count:05}"
        self.render_text(moves_text, (280 + GUI.board_left_margin, 78), pygame.Color("red"))

