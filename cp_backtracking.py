import copy

#-----------CONSTRAIN PROPAGATION & BACKTRACKING-----------###################################################################################################

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


#Function that iterate the constrain propagation until the sudoku board changes
def iterative_cp(board_row, board_col, board_box):
	flag = True

	#until the board changes
	while(flag):
		flag = False

		#for each element
		for i in range(0,9):
			for j in range(0,9):

				if isinstance(board_row[i][j], list): #if the element is a list

					for k in board_row[i][j]: #for each element of the list
						#if the element could not be part of a consistent solution delete it
						#i.e. if there is already the same number in the same row, column or box, delete the number in the list
						if (k in board_row[i]) or (k in board_col[j]) or (k in board_box[(i//3)*3 + j//3]):
							board_row[i][j].remove(k)
							flag = True

					if len(board_row[i][j]) == 1:
						board_row[i][j] = board_row[i][j][0]

		#propagate the changes on the board by column and by box, for the next iteration        
		board_col = board_by_col(board_row)
		board_box = board_by_box(board_row)


#First iteration of the costrain propagation
def constrain_propagation(board_row, board_col, board_box):
	#for each element of the board
	for i in range(0,9):
		for j in range(0,9):

			if board_row[i][j] == 0: #if the elemtent is empty
				n = []

				#assign to the element a list that contains all the number between 1 and 9 that could be part of a consistent solution
				#so all the number that are not already in the same row, column or box
				for k in range(1,10):
					if not(k in board_row[i]) and not(k in board_col[j]) and not(k in board_box[(i//3)*3 + j//3]):
						n.append(k)

				if len(n) == 1:
					n = n[0]

				board_row[i][j] = n

	#iterate the propagation of the contrains until the board changes
	iterative_cp(board_row, board_by_col(board_row), board_by_box(board_row))
	

#Function that performs the forward checking for the backtracking
#Given a number and its position on the sudoku board, delete that number from the other lists on the same row, column and box of that number.
#If at some point, by deleting this element, we obtain an empty list, then return False, otherwise return True.
def delete_forward(x, board, r, c):
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


#Function that implements the backtracking with forward checking
def backtracking(board_row, row, col, board_res):
	#base case, if the board is finished return True
	if row == 9 and col == 0:
		return True

	else:
		#if the row is finished, call the recursion on the start of next row
		if col == 9:
			return backtracking(board_row, row + 1, 0, board_res)

		else:
			#if the current element is a number, then call the recursion on the next element
			if isinstance(board_row[row][col], int):
				return backtracking(board_row, row, col + 1, board_res)
			#otherwise, if the current element is a list
			else:
				#for each element of the list
				for i in range(len(board_row[row][col])):
					x = board_row[row][col][i]
					tmp = copy.deepcopy(board_row)

					#if we can perform the forward checking
					if delete_forward(x, board_row, row, col):
						#proceed with the recursion
						res = backtracking(board_row, row, col + 1, board_res)

						if res:
							board_res[row][col] = x #if the backtracking succeed, save the value on the resulting board
							return res

					#otherwise go back to the previous state		
					board_row = tmp

				return False #if none element of the list can be part of the solution return False
