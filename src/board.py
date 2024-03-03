import pygame


class Board:

    def __init__(self, board_size):
        self.board = [[False for _ in range(board_size)] for _ in range(board_size)]
        self.objective = [[False for _ in range(board_size)] for _ in range(board_size)]

        for i in range(3, 6):
             for j in range(3, 6):
                self.board[i][j] = True
                self.objective[i][j] = True

    def draw(self, screen, cell_size, images, start_height=0):
        border = images[3]
        screen.blit(border, (0, 0 + start_height))  # Adjust the y coordinate for the top border
        screen.blit(border, ((self.getBoardSize() + 1) * cell_size, (self.getBoardSize()+1) * cell_size + start_height))  # Adjust the y coordinate for the right border
        screen.blit(border, (0 * cell_size, (self.getBoardSize()+1) * cell_size + start_height))  # Adjust the y coordinate for the bottom border
        screen.blit(border, ((self.getBoardSize() + 1) * cell_size, 0 + start_height))  # Adjust the y coordinate for the right border

        for row in range(1, self.getBoardSize() + 1):
            arrow = images[2]
            rotated_arrow = pygame.transform.rotate(arrow, 90)  # Rotate the arrow by 90 degrees
            screen.blit(rotated_arrow, (0, row * cell_size + start_height))  # Adjust the y coordinate for the arrow
            
            rotated_arrow = pygame.transform.rotate(arrow, 270)  # Rotate the arrow by 270 degrees
            screen.blit(rotated_arrow, ((self.getBoardSize() + 1) * cell_size, row * cell_size + start_height))  # Adjust the y coordinate for the arrow
            
            rotated_arrow = pygame.transform.rotate(arrow, 0)  # Rotate the arrow by 180 degrees
            screen.blit(rotated_arrow, (row * cell_size, 0 + start_height))  # Adjust the y coordinate for the arrow
            
            rotated_arrow = pygame.transform.rotate(arrow, 180)  # Rotate the arrow by 180 degrees
            screen.blit(rotated_arrow, (row * cell_size, (self.getBoardSize() + 1) * cell_size + start_height))  # Adjust the y coordinate for the arrow

        for row in range(self.getBoardSize()):
            for col in range(self.getBoardSize()):
                cell_image = images[1] if self.board[row][col] else images[0]
                screen.blit(cell_image, ((col + 1) * cell_size, (row + 1) * cell_size + start_height))  # Adjust the y coordinate for the cell

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

