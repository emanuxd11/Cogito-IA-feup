class Board:

    def __init__(self, board_size):
        self.board = [[False for _ in range(board_size)] for _ in range(board_size)]
        self.objective = [[False for _ in range(board_size)] for _ in range(board_size)]

        for i in range(3, 6):
             for j in range(3, 6):
                self.board[i][j] = True
                self.objective[i][j] = True

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

    def isWinningBoard(self):
        for row in range(self.getBoardSize()):
            for col in range(self.getBoardSize()):
                if self.board[row][col] != self.objective[row][col]:
                    return False
        return True

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += str(row) + "\n"
        return board_str

    

    def __lt__(self, other):
        return (len(self.board) < len(other.board))
    
    def __eq__(self, other):
        for row in range (len(self.board)):
            for col in range (len(self.board)):
                if (self.board[row][col] != other.board[row][col]):
                    return False
        return True



