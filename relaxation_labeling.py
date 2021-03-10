import numpy as np
from cp_backtracking import board_by_col, board_by_box

#-----------RELAXATION LABELING-----------###################################################################################################

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


#Function that generates the initial vector of probability p_0
def generateP(board):
	p = np.empty((9,9,9))

	for r in range(9):
		for c in range(9):
			x = np.zeros(9)

			if board[r][c] != 0:
				x[board[r][c] - 1] = 1

			else:
				count = 0
				board_col = board_by_col(board)
				board_box = board_by_box(board)

				for i in range(1,10):

					if not(i in board[r]) and not(i in board_col[c]) and not(i in board_box[(r//3)*3 + c//3]):
						x[i - 1] = 1
						count = count + 1

				for i in range(0,len(x)):
					x[i] = x[i] / count

			p[r][c] = x

	return p


#Function that computes the quantifiers that support the context of a certain p
def generateQ(p, r, row, col):
	q = np.zeros(10)

	for label in range(1,10):

		for i in range(9):
			for j in range(9):
				for mu in range(1,10):

					q[label] += r[row][col][label][i][j][mu] * p[i][j][mu - 1]

	return q