from board import Board
from sound import Sound
from GUI import GUI

import random
import pygame
import threading
import copy


class Game:

    def __init__(self, board_size):
        self.isComputerMode = False
        self.bot = None
        self.level_active = False
        self.is_moving = False
        self.is_shuffling = False
        self.shuffle_level = 30 # don't quite know how this evolves tbh
        self.shuffles_applied = 0
        self.board = Board(board_size)
        self.move_count = 0
        self.level = 1
        self.is_timing = False
        self.level_start_time = 0
        self.level_beat_time = 0
        self.MOVEMENT_RULE_QNT = 12 # there are 12 distinct movement rules
        self.secondary_arrow_layout = {
            "row": [False, True, True, False, True, True, True, False, True, True, False],
            "col": [False, True, False, False, True, True, True, False, True, True, False]
        }
        self.secondary_layout_mov_rules = (4, 10)

    def setGUI(self, gui: GUI):
        self.gui = gui

    def setComputerMode(self, bot):
        self.bot = bot
        self.isComputerMode = True

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
        if self.requires2ndLayout() and not self.checkArrow2ndLayout(row, col):
            return False

        return self.isLeftSideArrow(row, col) or \
                self.isRightSideArrow(row, col) or \
                self.isTopSideArrow(row, col) or \
                self.isBottomSideArrow(row, col)

    def toggle_cell(self, row, col):
        # don't allow making moves before the level has started
        # or if the game is not on human mode
        if not self.level_active or self.isComputerMode: 
            return
        if self.isArrowClick(row, col):
            Sound.playMoveSound()
            self.make_move(row, col)
            self.move_count += 1

    def mt_board_shuffle(self):
        # shuffles the board on a new thread, doesn't block rendering new frames
        def shuffle_caller():
            self.shuffle_board()
        shuffle_thread = threading.Thread(target=shuffle_caller)
        shuffle_thread.start()

    def currentLevelTime(self):
        return pygame.time.get_ticks() - self.level_start_time

    def getTimeString(self):
        if not self.is_timing:
            return "00:00:00"

        total_seconds = self.currentLevelTime() // 1000 if self.is_timing else self.level_beat_time

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # starts a new level
    def startLevel(self):
        Sound.playBackgroundTheme()
        self.mt_board_shuffle()

    # when a level is won
    def endLevel(self):
        self.gui.showWinMessage()
        self.level_active = False
        self.is_timing = False
        self.level_beat_time = self.currentLevelTime()
        self.shuffles_applied = 0
        self.shuffle_level += 5 # just adding 5 for now
        self.move_count = 0
        self.level += 1
        Sound.playWinMusic()

    def startTiming(self):
        self.level_start_time = pygame.time.get_ticks()
        self.is_timing = True

    def updateLogic(self):
        if not self.level_active: # start level
            self.startLevel()

        if not self.is_timing and self.level_active:
            self.startTiming()

        if self.board.isWinningBoard() and self.level_active:
            self.endLevel()
            self.startLevel()

    def shuffle_board(self):
        if self.is_shuffling:
            return

        self.is_shuffling = True # to block the user from moving before it's done and the timer from timing too soon
        for _ in range(self.shuffle_level):
            direction = random.randint(1, 4)
            index = random.randint(0, self.board.getBoardSize() - 1)
            if direction == 1:
                self.make_move(0, index)
            elif direction == 2:
                self.make_move(10, index)
            elif direction == 3:
                self.make_move(index, 0)
            elif direction == 4:
                self.make_move(index, 10)
            self.shuffles_applied += 1
            Sound.playMoveSound()
            pygame.time.delay(100)

        self.is_shuffling = False
        self.level_active = True

    def getMovementRule(self):
        return (self.level - 1) % self.MOVEMENT_RULE_QNT + 1

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

        movement_rule_n = self.getMovementRule()
        move_set[movement_rule_n](row, col)

    def requires2ndLayout(self):
        return self.getMovementRule() in self.secondary_layout_mov_rules

    def checkArrow2ndLayout(self, row, col):
        if col in (0, 10) and \
            self.secondary_arrow_layout['col'][row] is False:
            return False 
        if row in (0, 10) and \
            self.secondary_arrow_layout['row'][col] is False:
            return False
        return True


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
            self.board.rotateColumnUp(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateColumnDown(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateRowLeft(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateRowRight(col - 1)

    def make_move_4(self, row, col):
        if self.checkArrow2ndLayout(row, col):
            self.make_move_1(row, col)

    def make_move_5(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowLeft(row - 1)
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowRight(row - 1)
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnUp(col - 1)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnDown(col - 1)

    def make_move_6(self, row, col):
        if self.isLeftSideArrow(row, col):
            self.board.rotateRowLeft(9 - row )
        elif self.isRightSideArrow(row, col):
            self.board.rotateRowRight(9 - row )
        elif self.isTopSideArrow(row, col):
            self.board.rotateColumnUp(9 - col)
        elif self.isBottomSideArrow(row, col):
            self.board.rotateColumnDown(9 - col)

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

    def make_move_10(self, row, col):
        if self.checkArrow2ndLayout(row, col):
            self.make_move_8(row, col)

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

    def __lt__(self, other):
        return (self.board < other.board)
    
        
    def valid_moves(self):
        valid_moves = set()
        for i in range (0, 15):
            for j in range (0, 15):
                gamecopy = self.deep_copy_game()
                if gamecopy.isArrowClick(i, j):
                    gamecopy.make_move(i,j)
                    print(f"({i},{j})")
                    valid_moves.add(gamecopy)
        return valid_moves
    
    def deep_copy_game(self):
        new_game = Game(len(self.board.board))  # Create a new Game instance with the same board size
        
        # Copy over attributes
        new_game.isComputerMode = self.isComputerMode
        new_game.bot = self.bot
        new_game.level_active = self.level_active
        new_game.is_moving = self.is_moving
        new_game.is_shuffling = self.is_shuffling
        new_game.shuffle_level = self.shuffle_level
        new_game.shuffles_applied = self.shuffles_applied
        new_game.move_count = self.move_count
        new_game.level = self.level
        new_game.is_timing = self.is_timing
        new_game.level_start_time = self.level_start_time
        new_game.level_beat_time = self.level_beat_time
        new_game.MOVEMENT_RULE_QNT = self.MOVEMENT_RULE_QNT
        new_game.secondary_arrow_layout = self.secondary_arrow_layout
        new_game.secondary_layout_mov_rules = self.secondary_layout_mov_rules
        
        # Deep copy the board
        new_game.board = copy.deepcopy(self.board)
        
        return new_game

