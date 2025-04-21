import copy

PLAYER = 1
AI = 2
EMPTY = 0
ROWS = 6
COLS = 7

def check_winner(board):
    # เช็คแนวนอน
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != EMPTY:
                return board[row][col]

    # เช็คแนวตั้ง
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != EMPTY:
                return board[row][col]

    # เช็คแนวทแยง (ล่างซ้ายไปบนขวา)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != EMPTY:
                return board[row][col]

    # เช็คแนวทแยง (บนซ้ายไปล่างขวา)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != EMPTY:
                return board[row][col]

    return None

def get_valid_moves(board):
    valid_moves = []
    for col in range(COLS):
        for row in range(ROWS - 1, -1, -1):  # เริ่มจากแถวล่างสุด
            if board[row][col] == EMPTY:
                valid_moves.append((row, col))
                break  # เมื่อเจอช่องว่างในคอลัมน์นั้นให้ออกจาก loop
    return valid_moves

def minimax(board, depth, maximizing, alpha=float('-inf'), beta=float('inf'), callback=None):
    winner = check_winner(board)
    if winner == AI:
        return 10, board
    elif winner == PLAYER:
        return -10, board
    elif depth == 0 or all(cell != EMPTY for row in board for cell in row):
        return 0, board

    if maximizing:
        max_eval = float('-inf')
        best_move = None
        for row, col in get_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[row][col] = AI
            if callback:
                callback(new_board, (row, col))
            eval, _ = minimax(new_board, depth - 1, False, alpha, beta, callback)
            if eval > max_eval:
                max_eval = eval
                best_move = new_board
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # beta cut-off
        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        for row, col in get_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[row][col] = PLAYER
            if callback:
                callback(new_board, (row, col))
            eval, _ = minimax(new_board, depth - 1, True, alpha, beta, callback)
            if eval < min_eval:
                min_eval = eval
                best_move = new_board
            beta = min(beta, eval)
            if beta <= alpha:
                break  # alpha cut-off
        return min_eval, best_move
