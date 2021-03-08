#-----------CP & BACKTRACKING-----------###################################################################################################

def board_by_col(board):
	board_col = []

	for i in range(0,9):
		board_col.append([])

		for j in range(0,9):
			board_col[i].append(board[j][i])

	return board_col

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

def constrain_propagation(board_row, board_col, board_box):
	for i in range(0,9):
		for j in range(0,9):

			if board_row[i][j] == 0:
				n = []

				for k in range(1,10):
					if not(k in board_row[i]) and not(k in board_col[j]) and not(k in board_box[(i//3)*3 + j//3]):
						n.append(k)

				if len(n) == 1:
					n = n[0]

				board_row[i][j] = n

	iterative_cp(board_row, board_col, board_box)
	
	
def delete_forward(x, board, r, c) -> object:
    # print("rrr",x, r, c) # DEBUG

    for j in range(c, len(board[r])):
        if (not isinstance(board[r][j], int)) and (x in board[r][j]):
            board[r][j].remove(x)
            if len(board[r][j]) == 0 and j != c:
                # print("a", x,r,c) # DEBUG
                return False
    for j in range(r, len(board)):
        if (not isinstance(board[j][c], int)) and (x in board[j][c]):
            board[j][c].remove(x)
            if len(board[j][c]) == 0 and j != r:
                # print("b", x,r,c) # DEBUG
                return False
    nrows = 3 - r % 3
    ncols = 3 - c % 3
    for i in range(0, nrows):
        for j in range(0, ncols):
            if (not isinstance(board[r + i][c + j], int)) and (x in board[r + i][c + j]):

                board[r + i][c + j].remove(x)
                if len(board[r + i][c + j]) == 0 and j != c and i != r:
                    # print("c", x,r,c) # DEBUG
                    return False
    board[r][c] = x
    return True


def backtracking_theRevenge(board_row, row, col, board_res):
    if row == 9 and col == 0:
        return True
    else:
        if col == 9:
            return backtracking_theRevenge(board_row, row + 1, 0, board_res)
        else:
            if isinstance(board_row[row][col], int):
                return backtracking_theRevenge(board_row, row, col + 1, board_res)
            else:
                for i in range(len(board_row[row][col])):
                    x = board_row[row][col][i]
                    temp = copy.deepcopy(board_row)
                    if delete_forward(x, board_row, row, col):
                        res = backtracking_theRevenge(board_row, row, col + 1, board_res)
                        if res:
                            board_res[row][col] = x
                            return res
                    board_row = temp
                    # print(board_row) #DEBUG
                return False
