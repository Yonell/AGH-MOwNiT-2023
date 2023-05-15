from math import sqrt
import numpy as np
import multiprocessing as mp
import random as rd
import matplotlib.pyplot as plt


class Sudoku:
    def __init__(self, file_name):
        f = open(file_name, "r")
        self.board_size = int(f.readline())
        if self.board_size != int(sqrt(self.board_size)) ** 2:
            raise ValueError("Board size must be a square number")
        self.board = np.array(
            [[int(i) if i != 'x' else 0 for i in f.readline().split()] for j in range(self.board_size)])
        self.is_editable = np.array([[True if self.board[j][i] == 0 else False for i in range(self.board_size)] for j in
                                     range(self.board_size)])
        f.close()

    get_board_size = lambda self: self.board_size
    get_board = lambda self: self.board

    def __str__(self):
        return str(self.board)

    def __repr__(self):
        return str(self.board)

    def is_solved(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return False
        for i in range(self.board_size):
            if not self.check_row(i):
                return False
            if not self.check_column(i):
                return False
        for i in range(0, self.board_size, int(sqrt(self.board_size))):
            for j in range(0, self.board_size, int(sqrt(self.board_size))):
                if not self.check_square(i, j):
                    return False
        return True

    def check_row(self, row):
        return self.check_list(self.board[row])

    def check_column(self, column):
        return self.check_list([self.board[i][column] for i in range(self.board_size)])

    def check_square(self, row, column):
        return self.check_list([self.board[i][j] for i in range(row, row + int(sqrt(self.board_size))) for j in
                                range(column, column + int(sqrt(self.board_size)))])

    def check_list(self, lst):
        return np.unique(lst).size == self.board_size

    def get_is_editable(self):
        return self.is_editable

    def set_value(self, row, column, value):
        if self.is_editable[row][column]:
            self.board[row][column] = value
        else:
            raise ValueError("This cell is not editable")

    def get_cost(self):
        cost = 0
        result = []
        for i in range(self.board_size):
            result.append(self.check_row_cost(i))
        for i in range(self.board_size):
            result.append(self.check_column_cost(i))
        for i in range(0, self.board_size, int(sqrt(self.board_size))):
            for j in range(0, self.board_size, int(sqrt(self.board_size))):
                result.append(self.check_square_cost(i, j))
        for i in result:
            cost += i
        return cost

    def check_row_cost(self, row):
        return self.check_list_cost(self.board[row])

    def check_column_cost(self, column):
        return self.check_list_cost([self.board[i][column] for i in range(self.board_size)])

    def check_square_cost(self, row, column):
        return self.check_list_cost([self.board[i][j] for i in range(row, row + int(sqrt(self.board_size))) for j in
                                     range(column, column + int(sqrt(self.board_size)))])

    def check_list_cost(self, lst):
        return self.board_size - np.unique(lst).size

    def set_board(self, board):
        self.board = board


def find_coords_to_change(sudoku):
    coords_to_change = (rd.randint(0, sudoku.get_board_size() - 1), rd.randint(0, sudoku.get_board_size() - 1))
    while not sudoku.get_is_editable()[coords_to_change[0]][coords_to_change[1]]:
        coords_to_change = (rd.randint(0, sudoku.get_board_size() - 1), rd.randint(0, sudoku.get_board_size() - 1))
    return coords_to_change


def sudoku_AS(sudoku, max_iter=1000, temp_func=lambda x, max_iter: (1 / (x + 1)) ** (1 / 2), y=None):
    if sudoku.is_solved():
        return sudoku
    if sum([sum(i) for i in sudoku.get_is_editable()]) == 0:
        raise ValueError("Sudoku is not editable")
    if y is None:
        y = []

    iter_to_solve = 0

    for i in range(sudoku.board_size):
        for j in range(sudoku.board_size):
            if sudoku.is_editable[i][j]:
                sudoku.set_value(i, j, rd.randint(1, sudoku.board_size))
    best_sudoku = sudoku.board.copy()
    best_cost = sudoku.get_cost()
    for iter in range(max_iter):
        if sudoku.is_solved():
            return sudoku, iter_to_solve
        coords_to_change = find_coords_to_change(sudoku)

        cost_old = sudoku.get_cost()

        old_value = sudoku.get_board()[coords_to_change[0]][coords_to_change[1]]
        sudoku.set_value(coords_to_change[0], coords_to_change[1], rd.randint(1, sudoku.board_size))

        cost_new = sudoku.get_cost()

        if cost_new < cost_old:
            if cost_new < best_cost:
                best_cost = cost_new
                best_sudoku = sudoku.board.copy()
        else:
            if rd.random() < temp_func(iter, max_iter):
                pass
            else:
                sudoku.set_value(coords_to_change[0], coords_to_change[1], old_value)

        iter_to_solve += 1
        y.append(sudoku.get_cost())
        if (iter % 1000 == 0):
            print(iter, best_cost, temp_func(iter, max_iter))
    for i in range(sudoku.board_size):
        for j in range(sudoku.board_size):
            if sudoku.is_editable[i][j]:
                sudoku.set_value(i, j, best_sudoku[i][j])
    sudoku.set_board(best_sudoku)
    return sudoku, iter_to_solve


def temp2(iteration, it=700):
    it = it * 4 / 5
    result = 1 - (iteration / it)
    if result <= 0:
        return 0
    if result > 1:
        return 1
    return result


def temp3(iteration, it=700):
    if iteration > it * 4 / 5:
        return 0
    return (999996 / 1000000) ** iteration


if __name__ == '__main__':
    s = Sudoku("sudoku7.txt")
    fig, (ax, bx) = plt.subplots(2, 1)
    y = []
    temp = [temp3(i, 1600000) for i in range(1600000)]
    s, i = sudoku_AS(s, max_iter=1600000, temp_func=temp3, y=y)
    ax.plot(y)
    bx.plot(temp)
    fig.show()
    print(s)
    print(s.is_solved(), i, s.get_cost())
