import pygame

from sound import Sound
from menu import Menu


class GUI:

    def __init__(self, game, cell_size=65):
        self.game = game

        self.board_top_margin = 130
        self.board_right_margin = 600
        self.board_bottom_margin = 50
        self.board_left_margin = 40
        self.cell_size = cell_size
        self.width = self.game.board.getBoardSize() * cell_size + self.board_right_margin + 2 * cell_size
        self.height = self.board_top_margin + self.game.board.getBoardSize() * cell_size + self.board_bottom_margin + 2 * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Cogito")

        # initialize images (always use convert as this has insane impact on performance)
        self.cell_images = [
            pygame.image.load("../img/square.jpg").convert(),
            pygame.image.load("../img/circle.jpg").convert(),
            pygame.image.load("../img/arrow.jpg").convert(),
            pygame.image.load("../img/border.jpg").convert()
        ]
        self.info_board_img = pygame.image.load("../img/info.jpg").convert()
        self.background_img = pygame.image.load("../img/background.jpg").convert()

        self.info_screen_font = "../fonts/digital-7-mono.ttf"

        # perform transformations on images in the beginning to save processing time in the rendering of each frame
        self.cell_images = [
            pygame.transform.scale(image, (cell_size, cell_size)) for image in self.cell_images
        ]
        self.objective_scale_factor = 0.6
        self.objective_filled_cell = self.resizeImage(self.cell_images[1], self.objective_scale_factor)
        self.objective_empty_cell = self.resizeImage(self.cell_images[0], self.objective_scale_factor)
        self.info_board = self.resizeImage(self.info_board_img, 0.55)
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))
        self.arrow_right = pygame.transform.rotate(self.cell_images[2], 90)
        self.arrow_left = pygame.transform.rotate(self.cell_images[2], 270)
        self.arrow_down = pygame.transform.rotate(self.cell_images[2], 0)
        self.arrow_up = pygame.transform.rotate(self.cell_images[2], 180)

        # initialize clock
        self.clock = pygame.time.Clock()

        # Initialize font for rendering text
        pygame.font.init()
        self.font = pygame.font.Font(self.info_screen_font, 34) # should add other fonts and this would be different then

        # cap fps
        self.fps = 60

    def show_menu(self, menu_items):
        menu = Menu(menu_items)

        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle menu events
            result = menu.handle_event(event)
            if result:
                if result == "Human Mode":
                    return
                elif result == "Exit":
                    pygame.quit()
                    sys.exit()

            # Reset display to all black
            self.screen.fill((0, 0, 0))

            self.screen.blit(pygame.transform.scale(menu.background_image, (self.width, self.height)), (0, 0))

            # Render menu
            menu.draw(self.screen, self.width/2, self.height/2 +150)

            # Apply changes
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.fps)


    def run(self):
        Sound.playBackgroundTheme()

        # Show the menu before starting the game
        menu_items = ["Human Mode", "Computer Mode", "Exit"]
        self.show_menu(menu_items)

        running = True
        while running:
            self.game.updateLogic()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    row = (y - self.board_top_margin) // self.cell_size
                    col = (x - self.board_left_margin) // self.cell_size
                    self.game.toggle_cell(row, col)

            # reset display to all black (prevents ghosting)
            self.screen.fill((0, 0, 0))

            # set background image
            self.screen.blit(self.background_img, (0, 0))

            # render board
            self.drawBoard()
            self.drawGoalBoard(820, 400)

            # render the info board
            self.renderInfoBoard()

            # apply changes
            pygame.display.flip()

            # cap the frame rate to the specific fps
            self.clock.tick(self.fps)

    def render_text(self, text, position, color=(255, 255, 255)):
        rendered_text = self.font.render(text, True, color)
        self.screen.blit(rendered_text, position)

    def resizeImage(self, image, factor):
        orig_width = image.get_width()
        orig_height = image.get_height()

        new_width = orig_width * factor
        new_height = orig_height * factor

        return pygame.transform.scale(image, (new_width, new_height))

    def drawBoard(self):
        start_height = self.board_top_margin
        left_gap = self.board_left_margin
        border = self.cell_images[3]
        screen = self.screen
        cell_size = self.cell_size

        screen.blit(border, (0 + left_gap, 0 + start_height))
        screen.blit(border, ((self.game.board.getBoardSize() + 1) * cell_size + left_gap, (self.game.board.getBoardSize() + 1) * cell_size + start_height))
        screen.blit(border, (0 * cell_size + left_gap, (self.game.board.getBoardSize() + 1) * cell_size + start_height))
        screen.blit(border, ((self.game.board.getBoardSize() + 1) * cell_size + left_gap, 0 + start_height))

        for row in range(1, self.game.board.getBoardSize() + 1):
            screen.blit(self.arrow_right, (0 + left_gap, row * cell_size + start_height))
            screen.blit(self.arrow_left, ((self.game.board.getBoardSize() + 1) * cell_size + left_gap, row * cell_size + start_height))
            screen.blit(self.arrow_down, (row * cell_size + left_gap, 0 + start_height))
            screen.blit(self.arrow_up, (row * cell_size + left_gap, (self.game.board.getBoardSize() + 1) * cell_size + start_height))

        for row in range(self.game.board.getBoardSize()):
            for col in range(self.game.board.getBoardSize()):
                cell_image = self.cell_images[1] if self.game.board.board[row][col] else self.cell_images[0]
                screen.blit(cell_image, ((col + 1) * cell_size + left_gap, (row + 1) * cell_size + start_height))

    def drawGoalBoard(self, x_offset, y_offset):
        start_height = y_offset
        left_gap = x_offset
        screen = self.screen

        board = self.game.board.objective
        board_size = self.game.board.getBoardSize()

        cell_size = int(self.cell_size * self.objective_scale_factor)

        board_surface = pygame.Surface((cell_size * board_size, cell_size * board_size)).convert_alpha()

        for row in range(board_size):
            for col in range(board_size):
                cell_image = self.objective_filled_cell if board[row][col] else self.objective_empty_cell
                board_surface.blit(cell_image, (col * cell_size, row * cell_size))

        screen.blit(board_surface, (left_gap, start_height))

    def renderInfoBoard(self):
        # Create a surface for the info panel
        info_panel_surface = pygame.Surface(self.info_board.get_size()).convert_alpha()

        # Clear the info panel surface
        info_panel_surface.fill((0, 0, 0))

        # Frame
        info_panel_surface.blit(self.info_board, (0, 0))

        # Current level timer
        level_timer_text = self.game.getTimeString()
        level_timer_surface = self.font.render(level_timer_text, True, pygame.Color("red"))
        info_panel_surface.blit(level_timer_surface, (27, 10))

        # Current level
        level_text = f"{self.game.level:03}"
        level_surface = self.font.render(level_text, True, pygame.Color("yellow"))
        info_panel_surface.blit(level_surface, (15, 40))

        # Current shuffle level
        shuffle_qnt_text = f"{self.game.shuffle_level:03}"
        shuffle_qnt_surface = self.font.render(shuffle_qnt_text, True, pygame.Color("yellow"))
        info_panel_surface.blit(shuffle_qnt_surface, (115, 40))

        # Current number of moves
        moves_text = f"{self.game.move_count:05}"
        moves_surface = self.font.render(moves_text, True, pygame.Color("red"))
        info_panel_surface.blit(moves_surface, (47, 70))

        # Position the info panel on the screen
        info_panel_x = 230 + self.board_left_margin
        info_panel_y = 7

        # Blit the info panel surface onto the main display
        self.screen.blit(info_panel_surface, (info_panel_x, info_panel_y))

