from board import Board
from sound import Sound

import pygame
import threading


class Game:

    def __init__(self, board_size):
        self.shuffle = True
        self.shuffle_level = 30 # don't quite know how this evolves tbh
        self.board = Board(board_size)
        self.move_count = 0
        self.level = 1
        self.MOVEMENT_RULE_QNT = 12 # there are 12 distinct movement rules

    # utilitary functions
    def isLeftSideArrow(self, row, col):
        return col == 0 and 1 <= row <= 9

    def isRightSideArrow(self, row, col):
        return col == 10 and 1 <= row <= 9

    def isTopSideArrow(self, row, col):
        return row == 0 and 1 <= col <= 9

    def isBottomSideArrow(self, row, col):
        return row == 10 and 1 <= col <= 9

    def isArrowClick(self, row, col):
        return self.isLeftSideArrow(row, col) or \
                self.isRightSideArrow(row, col) or \
                self.isTopSideArrow(row, col) or \
                self.isBottomSideArrow(row, col)

    def toggle_cell(self, row, col):
        if self.isArrowClick(row, col):
            Sound.playMoveSound()
            self.make_move(row, col)

    def mt_board_shuffle(self):
        # shuffles the board on a new thread, doesn't block rendering new frames
        def shuffle_caller():
            self.board.shuffle(self.shuffle_level)
        shuffle_thread = threading.Thread(target=shuffle_caller)
        shuffle_thread.start()

    # when a level is won
    def levelBeat(self):
        print(f"You beat level {self.level} with {self.move_count} moves!")
        self.move_count = 0
        Sound.playWinMusic()

    def goToNextLevel(self):
        print(f"you've advanced to level {self.level}")
        self.level += 1
        self.mt_board_shuffle()
        Sound.playBackgroundTheme()

    def updateLogic(self):
        if self.shuffle:
            self.mt_board_shuffle()
            self.shuffle = False

        if self.board.isWinningBoard() and self.move_count > 0:
            self.levelBeat()
            self.goToNextLevel()

    def make_move(self, row, col):
        move_set = {
                1: self.make_move_1,
                2: self.make_move_2,
                3: self.make_move_3,
                4: self.make_move_4,
                5: self.make_move_5,
                6: self.make_move_6,
                7: self.make_move_7,
                8: self.make_move_8,
                9: self.make_move_9,
                10: self.make_move_10,
                11: self.make_move_11,
                12: self.make_move_12,
        }

        movement_rule_n =(self.level - 1) % self.MOVEMENT_RULE_QNT + 1
        move_set[movement_rule_n](row, col)

        self.move_count += 1

    # read README.md for information on how these rules work

    # rule done
    def make_move_1(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)

    # rule done
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

    # rule done
    def make_move_3(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateColumnUp(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateColumnDown(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateRowLeft(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateRowRight(col - 1)

    # rule requires different arrow layout
    def make_move_4(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)

    # rule done
    def make_move_5(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)

    # rule done
    def make_move_6(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowLeft(9 - row )
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowRight(9 - row )
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnUp(9 - col)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnDown(9 - col)

    # rule done
    def make_move_7(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowLeft(9 - row )
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowRight(9 - row )
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnUp(9 - col)
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnDown(9 - col)
            self.board.rotateColumnUp(col - 1)

    # rule done
    def make_move_8(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
            self.board.rotateColumnUp(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
            self.board.rotateColumnDown(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
            self.board.rotateRowLeft(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
            self.board.rotateRowRight(col - 1)

    # rule done
    def make_move_9(self, row, col):
        if row == 5 or col == 5:
            self.make_move_1(row, col)
        elif self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
            self.board.rotateRowRight(9 - row)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
            self.board.rotateRowLeft(9 - row)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
            self.board.rotateColumnDown(9 - col)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
            self.board.rotateColumnUp(9 - col)

    # rule requires different arrow layout
    def make_move_10(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)

    # rule done
    def make_move_11(self, row, col):
        if row == 9 or col == 9:
            adj = 0 
        else:
            adj = row if (col == 0 or col == 10) else col

        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
            self.board.rotateRowRight(adj)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
            self.board.rotateRowLeft(adj)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
            self.board.rotateColumnDown(adj)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
            self.board.rotateColumnUp(adj)

    # rule done
    def make_move_12(self, row, col):
        if col == 1 or col == 2 or row == 1 or row == 2:
            adj = 6 + row if (col == 0 or col == 10) else 6 + col
        else:
            adj = row - 3 if (col == 0 or col == 10) else col - 3

        if self.isLeftSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
            self.board.rotateRowRight(adj)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
            self.board.rotateRowLeft(adj)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)
            self.board.rotateColumnDown(adj)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
            self.board.rotateColumnUp(adj)

