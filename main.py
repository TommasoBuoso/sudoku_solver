from cp_backtracking import constrain_propagation, board_by_col, board_by_box

def is_solved(board_row, board_col, board_box):
	solved = True

	for i in range(0,9):
		for j in range(0,9):
			k = board_row[i][j]

			if isinstance(board_row[i][j], list) or (board_row[i].count(k) > 1) or (board_col[j].count(k) > 1) or (board_box[(i//3)*3 + j//3].count(k) > 1):
				solved = False
				break

	if solved:
		print("SUDOKU SOLVED!!")
	else:
		print("NOT SOLVED =(")

#-----------MAIN-----------###################################################################################################

board_row =[[3,7,0,5,0,0,0,0,6],
	        [0,0,0,3,6,0,0,1,2],
	        [0,0,0,0,9,1,7,5,0],
	        [0,0,0,1,5,4,0,7,0],
	        [0,0,3,0,7,0,6,0,0],
	        [0,5,0,6,3,8,0,0,0],
	        [0,6,4,9,8,0,0,0,0],
	        [5,9,0,0,2,6,0,0,0],
	        [2,0,0,0,0,5,0,6,4]]

board_col = board_by_col(board_row)
board_box = board_by_box(board_row)

constrain_propagation(board_row, board_col, board_box)

for i in board_row:
	print(i)

is_solved(board_row, board_col, board_box)
#print(board_col)
#print(board_box)
#print(solve(board_row, board_col, board_box))