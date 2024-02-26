import random

RIGHT = "right"
LEFT = "left"


class Board:

    def __init__(self, board_size):
        self.board = [[False for _ in range(board_size)] for _ in range(board_size)]

        list = []
        count = 0
        while count < 9:
            x = random.randint(0, board_size - 1)
            y = random.randint(0, board_size - 1)
            if (x, y) in list:
                continue
            else:
                self.board[x][y] = True
                count += 1
                list.append((x,y))

    def getBoardSize(self):
        return len(self.board)

    # The default is shifting to the right
    def rotateRow(self, row, direction=RIGHT):
        if direction == RIGHT:
            self.board[row] = self.board[row][-1:] + self.board[row][:-1]
        elif direction == LEFT:
            self.board[row] = self.board[row][1:] + self.board[row][:1]

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += str(row) + "\n"
        return board_str

