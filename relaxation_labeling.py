import numpy as np
import copy
from cp_backtracking import board_by_col, board_by_box


# Fuction that takes the final vector of probabilities p and generates a sudoku board
def from_p_to_board(p):
	board = np.zeros((9, 9))

	for i in range(9):
		for j in range(9):
			tmp = np.amax(p[i][j])
			for k in range(1, 10):
				if p[i][j][k] == tmp:
					board[i][j] = k

	return board.tolist()


# -----------RELAXATION LABELING-----------###################################################################################################


# Function that generates the matrix of compatibility coefficients R
def generateR():
	r = np.empty((9, 9, 10, 9, 9, 10))

	for b_i_row in range(9):
		for b_i_col in range(9):
			for l in range(1, 10):
				for b_j_row in range(9):
					for b_j_col in range(9):
						for m in range(1, 10):

							if l == m:

								# if the assignments does not satisfy direct constraints, the compatibility r_{ij}(λ,μ) is equal to 0
								if b_i_row == b_j_row or b_i_col == b_j_col or ((b_i_row // 3) * 3 + b_i_col // 3) == (
										(b_j_row // 3) * 3 + b_j_col // 3):

									r[b_i_row][b_i_col][l][b_j_row][b_j_col][m] = 0
							# 1 otherwise
								else:
									r[b_i_row][b_i_col][l][b_j_row][b_j_col][m] = 1
							else:
								r[b_i_row][b_i_col][l][b_j_row][b_j_col][m] = 1

	return r


# Function that computes the quantifiers that support the context of a certain p
def generateQ(p, r, row, col, dict_non_zeros):
	q = np.zeros(10)
	r1 = r[row][col]

	for label in range(1, 10):

		r2 = r1[label]

		for i, j in dict_non_zeros.keys():

			q[label] += np.dot(r2[i, j, :], p[i, j, :])

	return q


# Function that generates the initial vector of probability p_0
def generateP(board):
	p = np.zeros((9, 9, 10))
	dict_non_zeros = {}

	for r in range(9):
		for c in range(9):
			x = np.zeros(10)

			if board[r][c] != 0:
				x[board[r][c]] = 1

			else:
				count = 0
				board_col = board_by_col(board)
				board_box = board_by_box(board)

				dict_non_zeros[(r, c)] = []

				for i in range(1, 10):

					if not (i in board[r]) and not (i in board_col[c]) and not (i in board_box[(r // 3) * 3 + c // 3]):
						x[i] = 1
						count = count + 1

						dict_non_zeros[(r, c)].append(i)

				for i in range(1, len(x)):
					x[i] = x[i] / count

			p[r][c] = x

	return p, dict_non_zeros


# Function that updates the vector p^{t} -> p^{t+1}
def updateP(p, r, dict_non_zeros):
	res = copy.deepcopy(p)

	for row in range(9):
		for col in range(9):

			if not (1 in res[row][col]):
				q = generateQ(p, r, row, col, dict_non_zeros)

				res[row, col, :] = np.multiply(p[row, col, :], q[:]) / np.dot(p[row, col, :], q[:])

				if np.amax(res[row][col]) >= 0.9:
					tmp = 1
					tmp_index = np.where(res[row][col] == np.amax(res[row][col]))
					res[row][col] = np.zeros(10)
					res[row][col][tmp_index] = tmp

	return res


# Function that, starting from the initial the probability vector p0, iterates the update of p until it changes or a stop number of iteration is reached
def relaxation_labeling(board, r, iteration_limit):
	p, dict_non_zeros = generateP(board)
	count = 0
	p_prev = np.zeros((9, 9, 10))

	while count < iteration_limit and not (np.array_equal(p, p_prev)):
		p_prev = copy.deepcopy(p)
		p = updateP(p, r, dict_non_zeros)
		count += 1

	return p