
# Prints the chess board with correct formatting
def printBoard(board):
    for i in range (0, len(board)):
        print(' ', end='')
        for j in range(0, len(board)):
            print(str(board[i][j]) + ' | ', end='')
        print('')
    print(' ')

# Returns true if a queen can be placed in the given position (given as an array of length 2 in the format [y, x])
def checkIfValid(board, pos):
    if board[pos[0]][pos[1]] == 'Q':
        return False

    for i in range(0, len(board)):
        for j in range(0, len(board)):
        	# Check column
            if board[i][pos[1]] == 'Q':
                return False
            # Check row
            if board[pos[0]][i] == 'Q':
                return False
            # Check diagonal
            if abs(i - pos[0]) == abs(j - pos[1]):
                if board[i][j] == 'Q':
                    return False
    return True

# Recursive algorithm to place queens
# n is the current row in which a queen is being placed, so start off with n = 0
# The limit is so the algorithm knows when to end - it is set to n, when the problem is for n queens on a n x n board
def placeQueens(board, n, limit):
	# All queens have been successfully placed so increment the combinations variable
    if n == limit:
        global combinations
        combinations = combinations + 1
    else:
    	# Loop through each position in the row, and if the position is valid call the function recursively with the next row
        for i in range(0, len(board)):
            if checkIfValid(board, [n, i]):
                board[n][i] = 'Q'
                placeQueens(board, n+1, limit)
                # Once this branch has been explored, reset the position on the board
                board[n][i] = '-'

# Default value of n
n = 8

# Create the board
board = []
for i in range(0, n):
    row = []
    for j in range(0, n):
        row.append('-')
    board.append(row)


# Calculate the answer
combinations = 0
placeQueens(board, 0, n)
print('Total number of combinations for ' + str(n) + ' queens on a ' + str(n) + 'x' + str(n) + ' chess board: ' + str(combinations))
