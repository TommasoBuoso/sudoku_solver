from cp_backtracking import constrain_propagation, board_by_col, board_by_box, backtracking
from relaxation_labeling import generateR, relaxation_labeling, from_p_to_board
import copy
import time

#Function that, given a board, returns True if the sudoku is solved, False otherwise
def is_solved(board_row):
	board_col = board_by_col(board_row)
	board_box = board_by_box(board_row)
	solved = True

	for i in range(0,9):
		for j in range(0,9):
			k = board_row[i][j]

			if isinstance(board_row[i][j], list) or (board_row[i].count(k) > 1) or (board_col[j].count(k) > 1) or (board_box[(i//3)*3 + j//3].count(k) > 1):
				solved = False
				break

	return solved

#-----------MAIN-----------###################################################################################################

boards = []

#Solved only with constrain propagation
boards.append([[3,7,0,5,0,0,0,0,6],
				[0,0,0,3,6,0,0,1,2],
				[0,0,0,0,9,1,7,5,0],
				[0,0,0,1,5,4,0,7,0],
				[0,0,3,0,7,0,6,0,0],
				[0,5,0,6,3,8,0,0,0],
				[0,6,4,9,8,0,0,0,0],
				[5,9,0,0,2,6,0,0,0],
				[2,0,0,0,0,5,0,6,4]])

#Easy
boards.append([[6,0,0,0,1,7,3,0,0],
				[0,4,3,0,2,0,0,0,1],
				[0,5,0,0,9,0,7,0,0],
				[0,0,0,2,6,0,0,0,0],
				[0,1,6,4,0,5,0,3,0],
				[0,0,0,1,8,9,0,0,2],
				[0,0,0,0,0,0,2,5,8],
				[0,0,4,0,0,6,9,0,0],
				[5,9,1,0,0,2,4,0,0]])

#Not solved only with constrain propagation
boards.append([[0,0,0,0,2,0,0,4,0],
				[0,0,8,0,3,5,0,0,0],
				[0,0,0,0,7,0,6,0,2],
				[0,3,1,0,4,6,9,7,0],
				[2,0,0,0,0,0,0,0,0],
				[0,0,0,5,0,1,2,0,3],
				[0,4,9,0,0,0,7,3,0],
				[0,0,0,0,0,0,0,1,0],
				[8,0,0,0,0,4,0,0,0]])

#Medium
boards.append([[0,9,6,0,0,8,3,0,0],
				[0,0,0,0,0,0,0,0,0],
				[4,0,0,0,1,0,0,9,7],
				[6,0,0,7,8,0,5,3,0],
				[0,0,0,0,0,0,1,0,0],
				[0,3,4,0,0,0,0,0,0],
				[9,0,0,0,0,6,7,0,4],
				[5,0,0,0,9,0,0,0,0],
				[0,0,0,8,7,0,0,0,1]])

#Very difficult sudoku
boards.append([[0,4,0,9,2,0,0,0,0],
			   [0,2,0,0,0,0,0,0,0],
			   [0,0,0,0,0,0,0,1,3],
			   [0,0,0,4,3,0,0,0,2],
			   [2,5,8,0,0,6,0,0,0],
			   [0,0,4,1,0,0,0,0,9],
			   [0,0,0,0,0,0,5,8,0],
			   [8,0,9,0,7,3,0,0,0],
			   [0,0,0,0,0,1,0,3,0]])

r = generateR()

for board_row in boards:
	print("############################################")
	flag = 0

	start_time = time.time()

	p = relaxation_labeling(board_row, r, 500)

	end_time = time.time()

	board_p = from_p_to_board( p )

	if is_solved(board_p):
		print("SOLVED - With Relaxation labeling, %s seconds" % (end_time - start_time))
		flag = 2
	else:
		print("NOT SOLVED - With Relaxation labeling, %s seconds" % (end_time - start_time))

	board_col = board_by_col(board_row)
	board_box = board_by_box(board_row)

	start_time = time.time()

	constrain_propagation(board_row, board_col, board_box)  #first we try only with the constrain propagation

	end_time = time.time()

	if is_solved(board_row):
	   print("SUDOKU SOLVED - Only with CP, %s seconds" % (end_time - start_time))
	   flag = 1

	else:
	   print("NOT SOLVED - Only with CP")
	   print("Try with backtracking...")

	   board_res = copy.deepcopy(board_row)
	   backtracking(board_row, 0, 0, board_res)            #if only with the constrain propagation is not enough
														   #we go with the backtracking solution
	   end_time = time.time()

	   if is_solved(board_res):
		   print("SUDOKU SOLVED - With CP & Backtracking, %s seconds" % (end_time - start_time))
		   flag = 1
		   board_row = board_res

	   else:
		   print("FAIL")

	if flag == 1:
		for i in board_row:
			print(i)
	elif flag == 2:
		for i in board_p:
			print(i)
	else:
		print("FAIL")

