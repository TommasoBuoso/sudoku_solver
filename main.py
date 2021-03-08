import copy
from datetime import datetime


def is_solved(board_row, board_col, board_box):
	solved = True

	for i in range(0, 9):
		for j in range(0, 9):
			k = board_row[i][j]

			if isinstance(board_row[i][j], list) or (board_row[i].count(k) > 1) or (board_col[j].count(k) > 1) or (
					board_box[(i // 3) * 3 + j // 3].count(k) > 1):
				solved = False
				break

	if solved:
		print("SUDOKU SOLVED!!")
	else:
		print("NOT SOLVED =(")

def define_ris(board):
	ris = [[0 for y in range(9)]
		   for _ in range(9)]
	for i in range(9):
		for j in range(9):
			if isinstance(board[i][j], int):
				ris[i][j] = board[i][j]
	return ris


def scorri_riga(riga, x, y, bohZ, bohR, bohC, ris):
	if x == 0 and y == 9:
		return True
	else:
		if x == 9:
			return scorri_riga(riga, 0, y + 1, (bohZ), (bohR), (bohC), ris)
		else:

			if isinstance(riga[y][x], int):
				bohR[y].append(riga[y][x])
				bohC[x].append(riga[y][x])
				bohZ[(3 * (y // 3)) + (x // 3)].append(riga[y][x])
				k = scorri_riga(riga, x + 1, y, (bohZ), (bohR), (bohC), ris)
				if k == False:
					bohR[y].pop()
					bohC[x].pop()
					bohZ[(3 * (y // 3)) + (x // 3)].pop()
				return k
			else:
				for i in riga[y][x]:
					print(i, y , x, "bohZ", bohZ, "bohR", bohR, "bohC", bohC)
					if (i not in bohZ[(3 * (y // 3)) + (x // 3)]) and (i not in bohR[y]) and (i not in bohC[x]):
						bohR[y].append(i)
						bohC[x].append(i)
						bohZ[(3 * (y // 3)) + (x // 3)].append(i)
						if scorri_riga(riga, x + 1, y, (bohZ), (bohR), (bohC), ris):
							print("ris", y, x, i)
							ris[y][x] = i
							return True
						bohR[y].pop()
						bohC[x].pop()
						bohZ[(3 * (y // 3)) + (x // 3)].pop()
				return False


if __name__ == '__main__':
	from cp_backtracking import constrain_propagation, board_by_col, board_by_box

	# -----------MAIN-----------###################################################################################################

	# Solved only with constrain propagation
	# board_row = [[3, 7, 0, 5, 0, 0, 0, 0, 6],
	# 			 [0, 0, 0, 3, 6, 0, 0, 1, 2],
	# 			 [0, 0, 0, 0, 9, 1, 7, 5, 0],
	# 			 [0, 0, 0, 1, 5, 4, 0, 7, 0],
	# 			 [0, 0, 3, 0, 7, 0, 6, 0, 0],
	# 			 [0, 5, 0, 6, 3, 8, 0, 0, 0],
	# 			 [0, 6, 4, 9, 8, 0, 0, 0, 0],
	# 			 [5, 9, 0, 0, 2, 6, 0, 0, 0],
	# 			 [2, 0, 0, 0, 0, 5, 0, 6, 4]]

	# Not solved only with constrain propagation
	board_row = [[0, 0, 0, 0, 2, 0, 0, 4, 0],
				 [0, 0, 8, 0, 3, 5, 0, 0, 0],
				 [0, 0, 0, 0, 7, 0, 6, 0, 2],
				 [0, 3, 1, 0, 4, 6, 9, 7, 0],
				 [2, 0, 0, 0, 0, 0, 0, 0, 0],
				 [0, 0, 0, 5, 0, 1, 2, 0, 3],
				 [0, 4, 9, 0, 0, 0, 7, 3, 0],
				 [0, 0, 0, 0, 0, 0, 0, 1, 0],
				 [8, 0, 0, 0, 0, 4, 0, 0, 0]]

	board_col = board_by_col(board_row)
	board_box = board_by_box(board_row)

	constrain_propagation(board_row, board_col, board_box)

	for i in board_row:
		print(i)
	print('\n')
	board_ris = define_ris(board_row[:])
	print(scorri_riga(board_row, 0, 0, [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []],
					  [[] for y in range(9) for _ in range(9)], board_ris))
	print(board_ris)
