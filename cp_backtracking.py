import copy

#-----------CP & BACKTRACKING-----------###################################################################################################

#Function that takes for input the sudoku board by row, and returns the board by columns.
#The list generated contains the 9 columns of the sudoku boards as sublists.
def board_by_col(board): 
	board_col = []

	for i in range(0,9):
		board_col.append([])

		for j in range(0,9):
			board_col[i].append(board[j][i])

	return board_col

#Function that takes for input the sudoku board by row, and returns the board by box.
#The list generated contains the 9 sub-boxes of the sudoku boards as sublists.
def board_by_box(board):
	board_box = [[],[],[],
				 [],[],[],
				 [],[],[]]

	for i in range(0,9):
		if i <= 2:
			board_box[0] = board_box[0] + board[i][0:3]
			board_box[1] = board_box[1] + board[i][3:6]
			board_box[2] = board_box[2] + board[i][6:9]
		elif i <= 5:
			board_box[3] = board_box[3] + board[i][0:3]
			board_box[4] = board_box[4] + board[i][3:6]
			board_box[5] = board_box[5] + board[i][6:9]
		else:
			board_box[6] = board_box[6] + board[i][0:3]
			board_box[7] = board_box[7] + board[i][3:6]
			board_box[8] = board_box[8] + board[i][6:9]

	return board_box

def iterative_cp(board_row, board_col, board_box):
	flag = True

	while(flag):
		flag = False

		for i in range(0,9):
			for j in range(0,9):

				if isinstance(board_row[i][j], list):

					for k in board_row[i][j]:
						if (k in board_row[i]) or (k in board_col[j]) or (k in board_box[(i//3)*3 + j//3]):
							board_row[i][j].remove(k)
							flag = True

					if len(board_row[i][j]) == 1:
						board_row[i][j] = board_row[i][j][0]

		board_col = board_by_col(board_row)
		board_box = board_by_box(board_row)

#First iteratio of the costrain propagation
def constrain_propagation(board_row, board_col, board_box):
	#for each element of the board
	for i in range(0,9):
		for j in range(0,9):

			if board_row[i][j] == 0: #if the elemtent is empty
				n = []

				#assign the element a list that contains all the number between 1 and 9 that could be part of a consistent solution
				#so all the number that are not already in the same row, column or box
				for k in range(1,10):
					if not(k in board_row[i]) and not(k in board_col[j]) and not(k in board_box[(i//3)*3 + j//3]):
						n.append(k)

				if len(n) == 1:
					n = n[0]

				board_row[i][j] = n

	#iterate the propagation of the contrains until the board change
	iterative_cp(board_row, board_by_col(board_row), board_by_box(board_row))
	
	
def delete_forward(x, board, r, c) -> object:
    for j in range(c, len(board[r])):

        if (not isinstance(board[r][j], int)) and (x in board[r][j]):
            board[r][j].remove(x)

            if len(board[r][j]) == 0 and j != c:
                return False

    for j in range(r, len(board)):

        if (not isinstance(board[j][c], int)) and (x in board[j][c]):
            board[j][c].remove(x)

            if len(board[j][c]) == 0 and j != r:
                return False

    nrows = 3 - r % 3
    ncols = 3 - c % 3

    for i in range(0, nrows):
        for j in range(0, ncols):

            if (not isinstance(board[r + i][c + j], int)) and (x in board[r + i][c + j]):
                board[r + i][c + j].remove(x)
                if len(board[r + i][c + j]) == 0 and j != c and i != r:
                    return False

    board[r][c] = x
    return True


def backtracking(board_row, row, col, board_res):
    if row == 9 and col == 0:
        return True

    else:
        if col == 9:
            return backtracking(board_row, row + 1, 0, board_res)

        else:
            if isinstance(board_row[row][col], int):
                return backtracking(board_row, row, col + 1, board_res)
            else:
                for i in range(len(board_row[row][col])):
                    x = board_row[row][col][i]
                    tmp = copy.deepcopy(board_row)

                    if delete_forward(x, board_row, row, col):
                        res = backtracking(board_row, row, col + 1, board_res)

                        if res:
                            board_res[row][col] = x
                            return res

                    board_row = tmp

                return False
