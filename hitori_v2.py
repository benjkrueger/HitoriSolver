from pprint import pprint

from cell import Cell
from puzzle_file import hitori_example_easy2, hitori_example_easy, hitori_example, hitori_example2


def find_2_and_1_pattern(processed_line3):
    dct, circleds, numbers, blackeds, nums_to_check, length = processed_line3

    if not nums_to_check:
        return False

    to_black = []
    for num in nums_to_check:
        flag = (False, None)
        for i in range(length - 1):
            if numbers[i] == num and numbers[i + 1] == num and not blackeds[i] and not blackeds[i + 1]:
                flag = (True, i)
                break
        if flag[0]:
            for i in range(length):
                if numbers[i] == num and i != flag[1] and i != flag[1] + 1:
                    to_black.append(i)
    return to_black


def find_sandwich_pattern(processed_line2):
    dct, circleds, numbers, blackeds, nums_to_check, length = processed_line2

    if not nums_to_check:
        return False

    to_circle = []
    for num in nums_to_check:
        for i in range(length - 2):
            if num == numbers[i] and num == numbers[i + 2]:
                to_circle.append(i + 1)
    return to_circle


def find_elementary_black_outs(processed_line2):
    dct, circleds, numbers, blackeds, nums_to_check, length = processed_line2
    if not nums_to_check:
        return False

    to_black = []
    for num in nums_to_check:
        flag = (False, None)
        for i in range(length):

            if numbers[i] == num and dct[num] == 2 and circleds[i]:
                flag = (True, i)
                break
        if flag[0]:
            for i in range(length):
                if numbers[i] == num and i != flag[1]:
                    to_black.append(i)
    return to_black


def process_line(line, x):
    circleds = []
    numbers = []
    blackeds = []
    dct = {}
    nums_to_check = []
    for cell in line:
        if dct.get(cell.number, False):
            if not cell.black:
                dct[cell.number] += 1
            if dct[cell.number] == x:
                nums_to_check.append(cell.number)
        else:
            if not cell.black:
                dct[cell.number] = 1
        numbers.append(cell.number)
        circleds.append(cell.circled)
        blackeds.append(cell.black)
    return dct, circleds, numbers, blackeds, nums_to_check, len(line)


def find_consecutive_black_outs(line):
    last_black_out = False
    for cell in line:
        if cell.black and last_black_out:
            return True
        elif cell.black:
            last_black_out = True
        else:
            last_black_out = False
    return False


def find_all_multiples_circled(line):
    circled_numbers = {}
    numbers = {}
    for cell in line:
        if cell.circled:
            if circled_numbers.get(cell.number, False):
                circled_numbers[cell.number] += 1
            else:
                circled_numbers[cell.number] = 1
        if numbers.get(cell.number, False):
            numbers[cell.number] += 1
        else:
            numbers[cell.number] = 1
    for n in circled_numbers:
        if circled_numbers[n] > 1:
            return True
    return False


class Hitori:
    def __init__(self, size, table=None):
        self.size = size
        self.n2 = size * size
        self.array = [[Cell(0, i, j) for i in range(size)] for j in range(size)]
        self.row_values = []
        self.col_values = []
        for i in range(size):
            self.row_values.append({'x': 0})
            self.col_values.append({'x': 0})
            for j in range(self.size):
                self.row_values[i][j + 1] = 0
                self.col_values[i][j + 1] = 0
        self.moves_made = []
        self.branch = []
        if table is not None:
            self.import_table(table)

    def print_table(self):
        print("------------------------")
        for row in self.array:
            s = ""
            for col in row:
                if col.black:
                    s += " " + str(col) + ", "
                elif col.number < 10:
                    s += " " + str(col) + ", "
                else:
                    s += str(col) + ", "
            print(s)
        print("------------------------")
        print()

    def import_table(self, table):
        assert len(table) == self.size
        for i, row in enumerate(table):
            for j, col in enumerate(row):
                self.array[i][j] = Cell(col, i, j)
                if i == 0:
                    self.array[i][j].up = -1
                if j == 0:
                    self.array[i][j].left = -1
                if i == self.size - 1:
                    self.array[i][j].down = -1
                if j == self.size - 1:
                    self.array[i][j].right = -1
        self.update_row_values()
        self.update_col_values()
        self.initial_circle_cells()

    def black_out_cell(self, i, j, ab_choice=False):
        if not self.array[i][j].black:
            self.array[i][j].black_out(True, ab_choice)
            self.moves_made.append(('b', i, j))
            l, r, u, d = self.get_surrounding_cells(i, j)
            lb, rb, ub, db = True, True, True, True
            if l is not None:
                lb = l.change_surrounding('l', -1)
                self.circle_single_cell(i, j - 1)
            if r is not None:
                rb = r.change_surrounding('r', -1)
                self.circle_single_cell(i, j + 1)
            if u is not None:
                ub = u.change_surrounding('u', -1)
                self.circle_single_cell(i - 1, j)
            if d is not None:
                db = d.change_surrounding('d', -1)
                self.circle_single_cell(i + 1, j)
            return lb and rb and ub and db

    def un_black_out_cell(self, i, j):
        if self.array[i][j].black:
            self.array[i][j].black_out(False)
            # Remove moves_made?
            l, r, u, d = self.get_surrounding_cells(i, j)
            if l is not None:
                l.change_surrounding('l', 0)
            if r is not None:
                r.change_surrounding('r', 0)
            if u is not None:
                u.change_surrounding('u', 0)
            if d is not None:
                d.change_surrounding('d', 0)

    def circle_single_cell(self, i, j):
        if not self.array[i][j].circled:
            self.array[i][j].circle()
            self.moves_made.append(('c', i, j))
            l, r, u, d = self.get_surrounding_cells(i, j)
            if l is not None:
                l.change_surrounding('l', 1)
            if r is not None:
                r.change_surrounding('r', 1)
            if u is not None:
                u.change_surrounding('u', 1)
            if d is not None:
                d.change_surrounding('d', 1)

    def uncircle_single_cell(self, i, j):
        if self.array[i][j].circled:
            self.array[i][j].circle(False)
            # Change moves_made?
            l, r, u, d = self.get_surrounding_cells(i, j)
            if l is not None:
                l.change_surrounding('l', 0)
            if r is not None:
                r.change_surrounding('r', 0)
            if u is not None:
                u.change_surrounding('u', 0)
            if d is not None:
                d.change_surrounding('d', 0)

    def get_row(self, i):
        return self.array[i]

    def get_col(self, i):
        return list(map(lambda x: x[i], self.array))

    def update_single_row_values(self, i):
        dct = {'x': 0}
        for j in range(self.size):
            dct[j + 1] = 0
        for cell in self.array[i]:
            if cell.black:
                dct['x'] += 1
            else:
                dct[cell.number] += 1
        self.row_values[i] = dct

    def update_single_col_values(self, j):
        dct = {'x': 0}
        for x in range(self.size):
            dct[x + 1] = 0
        for row in self.array:
            if row[j].black:
                dct['x'] += 1
            else:
                dct[row[j].number] += 1
        self.col_values[j] = dct

    def update_row_values(self):
        for i in range(self.size):
            self.update_single_row_values(i)

    def update_col_values(self):
        for i in range(self.size):
            self.update_single_col_values(i)

    def get_cell_value(self, row, col):
        cell = self.array[row][col]
        if cell.black:
            return 'x'
        else:
            return cell.number

    def initial_circle_cells(self):
        for i in range(self.n2):
            row = i // self.size
            col = i % self.size
            cell = self.get_cell_value(row, col)
            if cell == 'x':
                continue
            else:
                if self.row_values[row][cell] == 1 and self.col_values[col][cell] == 1:
                    self.circle_single_cell(row, col)

    def get_surrounding_cells(self, i, j):
        left, right, up, down = None, None, None, None
        if i != 0:
            up = self.array[i - 1][j]
        if i != self.size - 1:
            down = self.array[i + 1][j]
        if j != 0:
            left = self.array[i][j - 1]
        if j != self.size - 1:
            right = self.array[i][j + 1]
        return left, right, up, down

    def make_chains(self):
        def single_chain(pos, acc):
            nonlocal explored
            i, j = pos
            if self.array[i][j].circled and explored[pos]:
                return acc
            elif self.array[i][j].circled:
                acc.append(pos)
                explored[pos] = True
                for n in self.get_neighbors_ij(i, j):
                    acc = single_chain(n, acc)
            return acc

        explored = {}
        chains = []
        open_spots = []
        for i, row in enumerate(self.array):
            for j, col in enumerate(row):
                if not self.array[i][j].black and self.array[i][j].circled:
                    explored[(i, j)] = False
                elif not self.array[i][j].black:
                    explored[(i, j)] = True
                    open_spots.append((i, j))
                else:
                    explored[(i, j)] = True
        for i, row in enumerate(self.array):
            for j, col in enumerate(row):
                if not explored[(i, j)]:
                    chains.append(single_chain((i, j), []))
        return chains, open_spots

    def get_neighbors_ij(self, i, j):
        lst = []
        if i != 0:
            lst.append((i - 1, j))
        if i != self.size - 1:
            lst.append((i + 1, j))
        if j != 0:
            lst.append((i, j - 1))
        if j != self.size - 1:
            lst.append((i, j + 1))
        return lst

    def find_liberties(self):
        to_circle = []
        chains, open_spots = self.make_chains()
        for chain in chains:
            liberties = set()
            for member in chain:
                neighbors = self.get_neighbors_ij(member[0], member[1])
                for n in neighbors:
                    if n in open_spots:
                        liberties.add(n)
            if len(liberties) == 1:
                to_circle.append(list(liberties)[0])
        return to_circle

    def check_for_closures(self):
        chains, open_spots = self.make_chains()
        total_liberties = []
        for chain in chains:
            liberties = set()
            for member in chain:
                neighbors = self.get_neighbors_ij(member[0], member[1])
                for n in neighbors:
                    if n in open_spots:
                        liberties.add(n)
            total_liberties.append(len(liberties))
        if len(chains) > 1:
            for elem in total_liberties:
                if elem == 0:
                    return True
        return False

    def chain_lookup(self):
        to_circle = self.find_liberties()
        if to_circle:
            for spot in to_circle:
                self.circle_single_cell(spot[0], spot[1])
            return True
        return False

    def check_if_solved(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.array[i][j].circled and not self.array[i][j].black:
                    return False
        return True

    def get_neighbor_cell(self, i, j, direction):
        if direction == 'l':
            return i, j - 1
        elif direction == 'r':
            return i, j + 1
        elif direction == 'u':
            return i - 1, j
        elif direction == 'd':
            return i + 1, j
        else:
            raise AssertionError

    def find_binary_choice(self):
        def find_in_line(line):
            dct = {}
            for cell in line:
                if not cell.circled and not cell.black:
                    if dct.get(cell.number, False):
                        dct[cell.number].append((cell.i, cell.j))
                    else:
                        dct[cell.number] = [(cell.i, cell.j)]
            for num in dct:
                if len(dct[num]) == 2:
                    return dct[num]
            return False
        for i in range(self.size):
            c = find_in_line(self.get_col(i))
            if c:
                return c
            r = find_in_line(self.get_row(i))
            if r:
                return r
        return False


    def make_ab_choice(self):
        lst = self.find_binary_choice()
        if lst:
            self.branch.append((len(self.moves_made), lst[0], lst[1]))
            self.black_out_cell(lst[0][0], lst[0][1], True)
            return True
        else:
            return False

    def rollback_last_branch(self):
        last_branch = self.branch.pop()
        for i in range(len(self.moves_made) - last_branch[0]):
            last_move = self.moves_made.pop()
            self.undo_move(last_move)
        self.black_out_cell(last_branch[2][0], last_branch[2][1])

    def undo_move(self, move_made):
        m, i, j = move_made
        if m == 'c':
            self.uncircle_single_cell(i, j)
        elif m == 'b':
            self.un_black_out_cell(i, j)

    def first_pass_at_solving(self):
        for i in range(self.size):
            plr2 = process_line(self.get_row(i), 2)
            plr3 = process_line(self.get_row(i), 3)
            plc2 = process_line(self.get_col(i), 2)
            plc3 = process_line(self.get_col(i), 3)
            row_21 = find_2_and_1_pattern(plr3)
            row_s = find_sandwich_pattern(plr2)
            row_e = find_elementary_black_outs(plr2)
            col_21 = find_2_and_1_pattern(plc3)
            col_s = find_sandwich_pattern(plc2)
            col_e = find_elementary_black_outs(plc2)
            if row_21:
                for j in row_21:
                    self.black_out_cell(i, j)
            if row_s:
                for j in row_s:
                    self.circle_single_cell(i, j)
            if row_e:
                for j in row_e:
                    self.black_out_cell(i, j)
            if col_21:
                for j in col_21:
                    self.black_out_cell(j, i)
            if col_s:
                for j in col_s:
                    self.circle_single_cell(j, i)
            if col_e:
                for j in col_e:
                    self.black_out_cell(j, i)

    def check_for_single_openings(self):
        for i in range(self.size):
            for j in range(self.size):
                if not self.array[i][j].black:
                    if self.array[i][j].number_of_open_surroundings() == 1:
                        open_direction = self.array[i][j].get_single_opening()
                        ic, jc = self.get_neighbor_cell(i, j, open_direction)
                        self.circle_single_cell(ic, jc)

    def no_change_made(self, starting_moves_length):
        return len(self.moves_made) == starting_moves_length

    def check_for_validity(self):
        for i in range(self.size):
            if find_consecutive_black_outs(self.get_row(i)) or find_consecutive_black_outs(self.get_col(i)):
                return False
            if find_all_multiples_circled(self.get_row(i)) or find_all_multiples_circled(self.get_col(i)):
                return False
        if self.check_for_closures():
            return False
        return True

    def solve_hitori_round(self):
        for i in range(self.size):
            plr2 = process_line(self.get_row(i), 2)
            plc2 = process_line(self.get_col(i), 2)
            row_e = find_elementary_black_outs(plr2)
            col_e = find_elementary_black_outs(plc2)
            if row_e:
                for j in row_e:
                    if not self.array[i][j].black:
                        try:
                            self.black_out_cell(i, j)
                        except AssertionError:
                            print("INVALID BLACK_OUT", i, j)
                            self.rollback_last_branch()
            if col_e:
                for j in col_e:
                    if not self.array[j][i].black:
                        try:
                            self.black_out_cell(j, i)
                        except AssertionError:
                            print("INVALID BLACK_OUT", j, i)
                            self.rollback_last_branch()
        self.check_for_single_openings()

    def solve_hitori(self):
        self.first_pass_at_solving()
        print("First Pass")
        self.print_table()
        while True:
            if self.branch:
                if not self.check_for_validity():
                    print("INVALID")
                    self.rollback_last_branch()
            if self.check_if_solved():
                if self.check_for_validity():
                    print("YOU DID IT")
                    self.print_table()
                    break
            starting_moves_length = len(self.moves_made)
            self.solve_hitori_round()
            if self.no_change_made(starting_moves_length):
                print("NO CHANGES")
                to_circle = self.find_liberties()
                if to_circle:
                    print("SUCCESSFUL CHAIN LOOKUP")
                    for pos in to_circle:
                        self.circle_single_cell(pos[0], pos[1])
                else:
                    print("BINARY CHOICE")
                    choice_made = self.make_ab_choice()
                    self.print_table()
                    if not choice_made:
                        print("FAILURE TO FIND BINARY CHOICE")
                        break

