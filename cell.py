from termcolor import colored


class Cell:
    def __init__(self, number, i, j, black=False, circled=False):
        self.number = number
        self.black = black
        self.circled = circled
        self.i = i
        self.j = j
        self.left = 0
        self.right = 0
        self.down = 0
        self.up = 0
        self.ab_choice = False

    def __str__(self):
        if self.black:
            if self.ab_choice:
                return colored('x', 'magenta')  # colored(str(self.number), 'grey')
            else:
                return colored('x', 'red')
        elif self.circled:
            return colored(str(self.number), 'blue')
        return str(self.number)

    def __repr__(self):
        if self.black:
            if self.ab_choice:
                return colored('x','magenta')  # colored(str(self.number), 'grey')
            else:
                return colored('x', 'red')
        elif self.circled:
            return colored(str(self.number), 'blue')
        return str(self.number)

    def black_out(self, val=True, ab_choice=False):
        assert self.circled == False
        self.black = val
        self.ab_choice = ab_choice

    def circle(self, val=True):
        assert self.black == False
        self.circled = val

    def change_surrounding(self, direction, value):
        if direction == 'l':
            self.right = value
        elif direction == 'r':
            self.left = value
        elif direction == 'u':
            self.down = value
        elif direction == 'd':
            self.up = value
        return not self.all_surroundings_blocked()

    def all_surroundings_blocked(self):
        return self.left == -1 and self.right == -1 and self.down == -1 and self.up == -1

    def number_of_open_surroundings(self):
        n = 0
        if self.left != -1:
            n += 1
        if self.right != -1:
            n += 1
        if self.down != -1:
            n += 1
        if self.up != -1:
            n += 1
        return n

    def get_single_opening(self):
        if self.left != -1:
            return 'l'
        elif self.right != -1:
            return 'r'
        elif self.up != -1:
            return 'u'
        elif self.down != -1:
            return 'd'
        else:
            return False
