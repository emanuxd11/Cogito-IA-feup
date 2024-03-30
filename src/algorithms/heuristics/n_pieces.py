def heuristic_count_pieces_outside(board):
    count = 0
    for row in range(len(board.board)):
        for col in range(len(board.board)):
            if board.board[row][col] != board.objective[row][col]:
                count += 1
    return count


def heuristic_sum_of_distances(board):
    total_distance = 0
    for row in range(len(board.board)):
        for col in range(len(board.board)):
            if board.board[row][col] != board.objective[row][col]:
                # Calculate distance between current position and correct position
                correct_row, correct_col = find_correct_position(board, row, col)
                distance = abs(row - correct_row) + abs(col - correct_col)
                total_distance += distance
    return total_distance

def find_correct_position(board, row, col):
    for i in range(len(board.board)):
        for j in range(len(board.board)):
            if board.objective[i][j] == board.board[row][col]:
                return i, j
            
def heuristic_sum_of_distances_to_center(board):
    total_distance = 0
    board_size = len(board.board)
    center_row = board_size // 2
    center_col = board_size // 2

    for row in range(board_size):
        for col in range(board_size):
            if board.board[row][col] != board.objective[row][col]:
                distance = abs(row - center_row) + abs(col - center_col)
                total_distance += distance
    return total_distance
