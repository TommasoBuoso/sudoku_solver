# Sudoku Solver
### Ca' Foscari University -  Buoso Tommaso, Tintari Nicanor
#### Assignment for the AI course

## Introduction
A  sudoku  is  a  logic-based,  combinatorial  number-placement  puzzle.   Theobjective is to fill a 9×9 grid with digits so that each column, each row, andeach of the nine 3×3 box that compose the grid contain all of the digits from1 to 9.  The puzzle setter provides a partially completed grid,  which for awell-posed puzzle has a single solution.  [1]
In  this  report,  we  will  analyze  the  library  [3],  written  in  python,  thatsolves the sudoku problem.
The library provide 2 solvers for sudoku puzzles:
- constraint propagation and backtracking:  use constraint propagationon  the  properties  of  the  sudoku  problem,  and,  if  this  is  not  enough,combine it with backtracking in order to solve the problem;
- relaxation labeling: solution of a labeling problem, in which the objectsbirepresent the values of the sudoku, and the labelsλiis the probabilityof that object to be represent the valuei.The library also provide a main of testing, that works on sudoku boardin form of matrix where empty cells are represented by zeros and known cellscontain their corresponding value between 1 and 9.

## Constraint propagation and Backtracking
This solver works in two different phases:
1.  constraint propagation:  tries to solve the sudoku only by applying the direct and indirect constraints;
2.  backtracking with forward checking: solves the sudoku by searching the state-space for solutions with a backtracking approach, combined with constraint  propagation  in  order  to  propagate  effect  of  this  tentative assignment.

Notice that the constraint propagation only method can’t guarantee the solution  of  the  sudoku,  while  the  backtracking  approach  will  lead  us  to  the solution for sure, assuming that the sudoku given as input is solvable.

### Constraint propagation
In order to simplify the comprehension of the solution, given that the algo-rithm takes as input a python list of lists, and each of them represent a rowof the sudoku board, we have implemented two functions called board_by_col and board_by_box.  They take the initial sudoku board as input and return thesudoku board as a python list of lists, and each of them represent respectivelya column/box of the board.The constraint propagation method consists in an iterative process thatpropagates two constraints [5]:
- direct  constraints:  no  two  equal  digits  appear  for  each  row,  column,and box;
- indirect constrains:  each digit must appear in each row, column, andbox.

The main idea is to generates, from the initial board, a new sudoku board that  maintains  the  already  known  values,  and  substitutes  the  zeros  with a list that contains all the values that respect the indirect constraint, if the list contains only one value, then directly substitute the zero with that value.This is implemented in the function constraint_propagation.
```
if board_row[i][j] == 0: #if the element is empty
	n = []

	#assign to the element a list that contains all the number between 1 and 9 that could be part of a consistent solution
	#so all the number that are not already in the same row, column or box
	for k in range(1,10):
		if not(k in board_row[i]) and not(k in board_col[j]) and not(k in board_box[(i//3)*3 + j//3]):
			n.append(k)

	if len(n) == 1:
		n = n[0]

	board_row[i][j] = n
```
From that board we start to propagate the direct constraint.  For each list in the matrix, going from the first to the last position, for each element of the list, if that value is already in the same row, column or box, then we remove that value from the list.  If after that loop the list contains only one element,as before, we substitute the list with that value.  This is implemented in the function iterative_cp.
```
if isinstance(board_row[i][j], list): #if the element is a list

	for k in board_row[i][j]: #for each element of the list
		#if the element could not be part of a consistent solution delete it
		#i.e. if there is already the same number in the same row, column or box, delete the number in the list
		if (k in board_row[i]) or (k in board_col[j]) or (k in board_box[(i//3)*3 + j//3]):
			board_row[i][j].remove(k)
			flag = True

	if len(board_row[i][j]) == 1:
		board_row[i][j] = board_row[i][j][0]
```
Then we iterate this procedure until the board changes.
Thanks to this algorithm we can solve the easy version of the sudoku problem, but when it is not enough we need to apply also the backtracking algorithm.

### Backtracking
In this phase of the solution, we are going to explore the state-space for the solution. In order to do that, we will follow a backtracking approach by implementing a depth-first algorithm. Given that the solution exist and it's unique, in this case the depth-first search is complete and optimal.
The recursive part of the depth-first search is implemented in the function backtracking. It takes as input the sudoku board returned by the constrain propagation phase, the current position on which we are searching, in the form of row/column, and the pointer to the result board. The base case arrives after the last position of the board, then, if in the current position we don't find a list of elements we simply proceed with the recursion, otherwise, for each element of the list that we try to explore, we keep track of the current state by saving a copy of the board, then the algorithm proceed with the forward checking phase. After the forward checking, if it succeed, then proceed with the recursion, otherwise go back on the path with the previous version of the board saved.
```
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
```
As mentioned in the previous paragraph, when the current position on the board coincides with a list, we perform a forward checking, thanks to the function called delete_forward(). This method takes as input a digit of the sudoku, the board and the current position, and delete that number from the other lists on the same row, column and box of that number. If at some point, by deleting this number, we obtain an empty list, then return False, so go back on the path, otherwise return True, so proceed with the recursion.
```
for j in range(c, len(board[r])):

    if (not isinstance(board[r][j], int)) and (x in board[r][j]):
    	board[r][j].remove(x)
    
    	if len(board[r][j]) == 0 and j != c:
    		return False
```
At the end of the recursion, the board solved will be pointed by the initial board_res pointer.
### Complexity
The complexity both temporal and spacial it's dominated by the depth-first algorithm used in the backtracking phase. So, if we simplify the problem by assuming that the tree search has a constant branching factor $b$, and we assume that the goal node is at depth $d$, the average search time is <img src="https://render.githubusercontent.com/render/math?math=O(b^d)">. Instead, the spacial complexity, i.e. maximum memory required, is $`O(db)`$.

## Relaxation labeling
The solver that we are going to analyze in this section is based on the labeling problem, where we have:
- a set on n object $B=\{b_1,...,b_n\}$, in our sudoku problem each $b_i$ object represent a cell of the board;
- a set of m labels $L = \{1,...,m\}$, for the sudoku problem m is equal to 9.

In order to solve the labeling problem, so assigning to each object the right label, for each object, first we generate an m-dimensional (probability) vector $p^{(0)}_i$ that represents the initial, noncontextual degree of confidence in the hypothesis “$b_i$ is labeled $\lambda$”, and the matrix (in our case tensor) of compatibility coefficients $R = \{r_{ij}(\lambda,\mu)\}$ [4]; then we iteratively update $p^{(t)}$ based on the compatibility model R, until the board changes or we reach a certain number of iteration.

### Generation phase
The first phase of generation, thanks to the functions generateP and generateR, initialize:
- the probability vector $p$ with a numpy [2] array of dimension $9\times 9 \times 10$, that, starting from the sudoku board, substitute each number with an array of size 10 (necessary for matrix operations) with all the values equal to 0, except two cases:
        -  if the initial value is equal to $i$, with $i \neq 0$, assign 1 at the $i$-th position in the new sub-array;
        -  otherwise, if the initial value is equal to 0, then, for each position $i$, such that $i$ meets the indirect constraint of the previous section, assign for each position the same probability value (between 0 and 1).
- a dictionary that keeps track of the board position that will change during the iteration phase (useful to optimize the execution time);
- the compatibility matrix $r$ with a numpy tensor of dimension $9\times 9 \times 10 \times 9\times 9 \times 10$, that for all possible pair of position on the board, and for all possible pair of values that these these positions can assume, assign at the respective position of $r$: 0 if the combination of value/position of the pairs does not meet the direct constraint of the previous section, 1 otherwise. $r$ can be computed a priori because itś equal for all the sudoku problems.

### Iterative phase
In this second and last phase of the solution, starting from $p$ and $r$, we iteratively update $p$ following the update rule:

$$
p^{(t+1)}_i(\lambda) = \frac{p^{(t)}_i(\lambda) q^{(t)}_i(\lambda)}{\sum_{\mu} p^{(t)}_i(\mu) q^{(t)}_i(\mu)}
$$

where

$$
q^{(t)}_i(\lambda) = \sum_{j}\sum_{\mu} r_{ij}(\lambda,\mu) p^{(t)}_j(\mu)
$$

In our library, the support $q$ is computed by the function generateQ, that takes advantage of the dictionary previously generated and the numpy operation dot, in order to optimize the time execution of the computation.
```
for label in range(1, 10):
		for i, j in dict_non_zeros.keys():
			q[label] += np.dot(r[row, col, label, i, j, :], p[i, j, :])
```
For the update of $p$ we have a function called updateP, that, for each element of $p^{(t)}$, if in that position there is already a 1 then don't do anything, otherwise generate $q$ and compute $p^{(t+1)}_i$ using the numpy's operations multiply and dot for optimizing the time execution. Then, in our version of the solver, when a value of $p^{(t+1)}_i$ is $\geq 0.9$, we choose to approximate it to 1 and set all the other elements to 0, in order to simplify the future computations.
```
if not (1 in res[row][col]):
	q = generateQ(p, r, row, col, dict_non_zeros)

	res[row, col, :] = np.multiply(p[row, col, :], q[:]) / np.dot(p[row, col, :], q[:])

	if np.amax(res[row][col]) >= 0.9:
		tmp = 1
		tmp_index = np.where(res[row][col] == np.amax(res[row][col]))
		res[row][col] = np.zeros(10)
		res[row][col][tmp_index] = tmp
```
For concluding, thanks to the function relaxation_labeling, we iterate the update of $p$ until it changes or until we don't reach a certain number of iteration.

### Complexity
If we look at the time complexity of this solver at high level, we can exclude the computation of $r$, given that it's done a priori, and we can also ignore the initial generation of $p$, because it is done only at the start of the algorithm. The time complexity is dominated by the computation of the support coefficient $q$, because for each element of $p$ that we have to update, we must generate a new $q$, that adds another two nested for loops and the access to $p$ and $r$, so the computation is heavily affected by this.
At the same time, for the spacial complexity, we maintain at most the three different copy of the $p$ vector and the tensor $r$ in memory simultaneously, so we have a constant complexity. 

## Solvers comparison
For comparing the to solver, the library provide a main of testing that proposes different sudoku boards, ordered from the easiest to the most difficult. For each board, the program tests it first with the relaxation labeling solver, with an iteration stop number equal to 500, then with the constraint propagation and backtracking solver. For both the solver , the program measures the execution time and checks if the result board is a correct solution for the sudoku problem.
As said before, in this phase we have tested different problems for difficulty, including:
- easy boards: for the easy boards we arrive at the solution for both the solvers. With the first solver we get the solution only with the constraint propagation phase in less than 0.001 seconds, at the same time, for the relaxation labeling solver we get a solution in about 6 seconds and less than 400 iteration;
$$
\begin{vmatrix}
3 & 7 & 0& 5 & 0 & 0 & 0 & 0 & 6 \\
0 & 0 & 0& 3 & 6 & 0 & 0 & 1 & 2 \\
0 & 0 & 0& 0 & 9 & 1 & 7 & 5 & 0 \\
0 & 0 & 0& 1 & 5 & 4 & 0 & 7 & 0 \\
0 & 0 & 3& 0 & 7 & 0 & 6 & 0 & 0 \\
0 & 5 & 0& 6 & 3 & 8 & 0 & 0 & 0 \\
0 & 6 & 4& 9 & 8 & 0 & 0 & 0 & 0 \\
5 & 9 & 0& 0 & 2 & 6 & 0 & 0 & 0 \\
2 & 0 & 0& 0 & 0 & 5 & 0 & 6 & 4
\end{vmatrix}
\Rightarrow
\begin{vmatrix}
3 & 7 & 1 & 5 & 4 & 2 & 8 & 9 & 6 \\
9 & 8 & 5 & 3 & 6 & 7 & 4 & 1 & 2 \\
6 & 4 & 2 & 8 & 9 & 1 & 7 & 5 & 3 \\
8 & 2 & 6 & 1 & 5 & 4 & 3 & 7 & 9 \\
4 & 1 & 3 & 2 & 7 & 9 & 6 & 8 & 5 \\
7 & 5 & 9 & 6 & 3 & 8 & 2 & 4 & 1 \\
1 & 6 & 4 & 9 & 8 & 3 & 5 & 2 & 7 \\
5 & 9 & 7 & 4 & 2 & 6 & 1 & 3 & 8 \\
2 & 3 & 8 & 7 & 1 & 5 & 9 & 6 & 4
\end{vmatrix}
$$
- medium board: for this type of sudoku problems, the relaxation labeling solver even after 15 seconds of execution and 500 iterations does not converges to the solution. At the same time, not even only the constraint propagation solver is enough to get the solution, but combined with the backtracking (with forward checking) approach, the algorithm provides a solution in less than 0.01 seconds;
- difficult board: when we arrive to difficult sudoku boards, obviously the relaxation labeling solver does not reach the solution (after about 20 seconds), but the constraint propagation and backtracking solver provides the solution in about 3 seconds.

We can observe from that results that the constrain propagation and backtracking solver arrives always at the solution (if it exists), while the relaxation labeling problem can only solve easy sudoku problems. Simultaneously, if we look at the execution time, the only solution reached by the relaxation labeling solver took us about 6 seconds, while the same solution by the constraint propagation and backtracking solver took us less than 0.001 seconds, and for the most difficult sudoku tested took us about 3 seconds.
So, despite the constant spacial complexity of the relaxation labeling solver is better than the linear complexity of the constraint propagation and backtracking solver, the second one is up to 10000 faster than the first one. At the same time, the constraint propagation and backtracking solver is complete and optimal, while the relaxation labeling solver is neither complete nor optimal.

## Conclusion
After the comparison, we can conclude that the constraint propagation and backtracking solver is better than the relaxation labeling solver, because the spacial complexity is acceptable, the execution time is the best, and it always reach the solution.
With this library we can solve all the sudoku problem in a very good time for the easy/medium difficulty boads, and a reasonable time for the most difficult porblems.

### Future developments

The future developments could be:
- for the constraint propagation and backtracking solver, we can speed up the operations by using a different data structure, for example a numpy object;
- for the relaxation labeling solver, we can imporve the speed of the operation by implementing further the vectorization of the operations, and by introducing some kind of randomness in the initialization of $p$ in order to avoid the non-convergence of the algorithm.

## References
[1]url:https://en.wikipedia.org/wiki/Sudoku.

[2]url:https://numpy.org/.

[3]    Tintari  Nicanor  Buoso  Tommaso.Sudoku  solver.  2021.url:https ://github.com/TommasoBuoso/sudoku_solver.

[4]    Prof. Andrea Torsello.Artificial Intelligence: Knowledge representationand planning - Relaxation labeling. 2021.

[5]    Prof. Andrea Torsello.Assignment 1: Sudoku Solver. 2021.url:https://moodle.unive.it/mod/page/view.php?id=294982.
