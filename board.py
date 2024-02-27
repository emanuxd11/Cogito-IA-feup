import random


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

    def rotateRowRight(self, row):
            self.board[row] = self.board[row][-1:] + self.board[row][:-1]
    def rotateRowLeft(self, row):
            self.board[row] = self.board[row][1:] + self.board[row][:1]

    def rotateColumnDown(self, col):
        previous = self.board[0][col]
        self.board[0][col] = self.board[-1][col]
        for i in range(1, self.getBoardSize()):
            new_previous = self.board[i][col]
            self.board[i][col] = previous 
            previous = new_previous

    def rotateColumnUp(self, col):
        previous = self.board[-1][col]
        for i in range(self.getBoardSize() - 2, -1, -1):
            new_previous = self.board[i][col]
            self.board[i][col] = previous 
            previous = new_previous
        self.board[-1][col] = previous


    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += str(row) + "\n"
        return board_str

