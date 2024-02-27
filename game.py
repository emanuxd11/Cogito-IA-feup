from board import Board
import pygame

class Game:

    def __init__(self, board_size):
        self.board = Board(board_size)
        self.move_count = 0
        self.level = 1
        self.MOVEMENT_RULE_QNT = 12 # there are 12 distinct movement rules

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

    # utilitary functions
    def isLeftSideArrow(self, row, col):
        return col == 0 and 1 <= row <= 9

    def isRightSideArrow(self, row, col):
        return col == 10 and 1 <= row <= 9

    def isTopSideArrow(self, row, col):
        return row == 0 and 1 <= col <= 10

    def isBottomSideArrow(self, row, col):
        return row == 10 and 1 <= col <= 10

    def isArrowClick(self, row, col):
        return self.isLeftSideArrow(row, col) or \
                self.isRightSideArrow(row, col) or \
                self.isTopSideArrow(row, col) or \
                self.isBottomSideArrow(row, col)

    def toggle_cell(self, row, col):
        if self.isArrowClick(row, col):
            sound_path = "audio/arrow_click.mp3"
            arrow_sfx = pygame.mixer.Sound(sound_path)
            arrow_sfx.play()

            self.make_move(row, col)

    def make_move(self, row, col):
        move_set = {
                1: self.make_move_1,
                2: self.make_move_2,
                3: self.make_move_3,
                4: self.make_move_4,
                5: self.make_move_5,
                6: self.make_move_6,
                # ...
        }

        movement_rule_n = (self.level - 1) % self.MOVEMENT_RULE_QNT + 1
        move_set[movement_rule_n](row, col)

        self.move_count += 1
        print(f"move count {self.move_count}") # just for debug while there is no GUI indicator
    
    # read README.md for information on how these rules work

    def make_move_1(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)

    def make_move_2(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
            self.board.rotateColumnUp(col - 1)

    def make_move_3(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)

    def make_move_4(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)

    def make_move_5(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)

    def make_move_6(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
