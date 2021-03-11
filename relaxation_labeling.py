import numpy as np
import copy
from cp_backtracking import board_by_col, board_by_box

#-----------RELAXATION LABELING-----------###################################################################################################

#Fuction that takes the final vector of probabilities p and generates a sudoku board
def from_p_to_board(p):
	p = np.round(p)
	print(p)
	board = np.zeros((9,9))

	for i in range(9):
		for j in range(9):
			for k in range(1,10):
				if p[i][j][k] == 1:
					board[i][j] = k
			if board[i][j] == 0:
				print("FAIL")

	return board

#Function that generates the matrix of compatibility coefficients R
def generateR():
	r = np.empty((9,9,10,9,9,10))

	for b_i_row in range(9):
		for b_i_col in range(9):
			for l in range(1,10):
				for b_j_row in range(9):
					for b_j_col in range(9):
						for m in range(1,10):

							if l == m:

								if b_i_row == b_j_row or b_i_col == b_j_col or ((b_i_row//3)*3 + b_i_col//3) == ((b_j_row//3)*3 + b_j_col//3):

									r[b_i_row][b_i_col][l][b_j_row][b_j_col][m] = 0
								else:
									r[b_i_row][b_i_col][l][b_j_row][b_j_col][m] = 1
							else:
								r[b_i_row][b_i_col][l][b_j_row][b_j_col][m] = 1

	return r


#Function that computes the quantifiers that support the context of a certain p
def generateQ(p, r, row, col):
	q = np.zeros(10)

	r1 = r[row][col]

	for label in range(1,10):

		r2 = r1[label]

		for i in range(9):
			for j in range(9):
				for mu in range(1,10):

					q[label] += r2[i][j][mu] * p[i][j][mu]

	return q

#Function that computes the quantifiers that support the context of a certain p
#def generateQ2(p, r, row, col):
#	q = np.zeros(10)
#
#	for label in range(1,10):
#
#		q[label] = np.sum( np.dot(p, r[row][label][col]) )
#
#	return q


#Function that generates the initial vector of probability p_0
def generateP(board):
	p = np.zeros((9,9,10))

	for r in range(9):
		for c in range(9):
			x = np.zeros(10)

			if board[r][c] != 0:
				x[board[r][c]] = 1

			else:
				count = 0
				board_col = board_by_col(board)
				board_box = board_by_box(board)

				for i in range(1,10):

					if not(i in board[r]) and not(i in board_col[c]) and not(i in board_box[(r//3)*3 + c//3]):
						x[i] = 1
						count = count + 1

				for i in range(1,len(x)):
					x[i] = x[i] / count

			p[r][c] = x

	return p


#Function that updates the vector p^{t} -> p^{t+1}
def updateP(p, r):
	res = np.empty((9,9,10))


	for row in range(9):
		for col in range(9):
			q = generateQ(p, r, row, col)

			for label in range(1,10):

			 	num = p[row][col][label] * q[label]
			 	den = np.sum( np.dot(p[row][col], q) )

			 	k = num / den
			 	if np.round(k, 1) == 1:
			 		k = 1
			 		res[row][col] = np.zeros(10)

			 	res[row][col][label] = k

	return res



def relaxation_labeling(board, r, iteration_limit):
	p = generateP(board)
	count = 0
	p_prev = np.zeros((9,9,10))

	while count < iteration_limit and not( np.array_equal(p, p_prev)):
		p_prev = copy.deepcopy(p)
		p = updateP(p, r)
		count += 1
		if count % 100 == 0:
			print(count)

	return p