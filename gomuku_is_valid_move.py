# # For now, the board can be anywhere between 5x5 and 19x19, so need variable to determine size of board
# n = 10
# def is_valid_move(board, row, col):
#     if row < 0 or row >= n or col < 0 or col >= n:
#         return False
#     if board[row][col] != 0:
#         return False
#
#     return True