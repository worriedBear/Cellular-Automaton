from graphics import *

global USER_INPUT


# representing a single cell
class Cell:
    left_cell = False
    right_cell = False

    is_alive = False
    next_iter_alive = False
    starting_pos = Point(-1, -1)

    def __init__(self, left_cell, right_cell, is_alive, x_pos, y_pos):
        self.left_cell = left_cell
        self.right_cell = right_cell

        self.is_alive = is_alive
        self.starting_pos = Point(x_pos, y_pos)

    def output_cell(self, window):
        # output all cells one row lower - after each iteration
        self.starting_pos.y += 4
        # draw a rectangle - respective to the cell's coordinates
        cell_rec = Rectangle(self.starting_pos,
                             Point(self.starting_pos.x + 2, self.starting_pos.y + 2))
        if self.is_alive:
            cell_rec.setFill("black")
            cell_rec.setOutline("black")
        else:
            cell_rec.setFill("grey")
            cell_rec.setOutline("grey")
        cell_rec.draw(window)

    # all these methods follow the same logic - they are called by the
    # first/middle cell and then recursively iterate to the
    # rightmost/leftmost cells
    def output_all(self, window):
        self.output_cell(window)
        if self.left_cell:
            self.left_cell.output_left_cell(window)
        if self.right_cell:
            self.right_cell.output_right_cell(window)

    def output_left_cell(self, window):
        self.output_cell(window)
        if self.left_cell:
            self.left_cell.output_left_cell(window)

    def output_right_cell(self, window):
        self.output_cell(window)
        if self.right_cell:
            self.right_cell.output_right_cell(window)

    # if left-/rightmost cells are found, append new cell
    def add_left_cell(self):
        if self.left_cell:
            self.left_cell.add_left_cell()
        else:
            x_pos = self.starting_pos.x - 4
            y_pos = self.starting_pos.y
            self.left_cell = Cell(False, self, False, x_pos, y_pos)

    def add_right_cell(self):
        if self.right_cell:
            self.right_cell.add_right_cell()
        else:
            x_pos = self.starting_pos.x + 4
            y_pos = self.starting_pos.y
            self.right_cell = Cell(self, False, False, x_pos, y_pos)

    def check_iteration(self):
        self.check_single_cell()
        if self.left_cell:
            self.left_cell.check_left_cell()
        if self.right_cell:
            self.right_cell.check_right_cell()

    def check_left_cell(self):
        self.check_single_cell()
        if self.left_cell:
            self.left_cell.check_left_cell()

    def check_right_cell(self):
        self.check_single_cell()
        if self.right_cell:
            self.right_cell.check_right_cell()

    def check_single_cell(self):
        if self.is_alive:
            mid = 1
        else:
            mid = 0
        # if this very cell is the leftmost cell - act as if the left neighbor
        # was in the same state as the current cell - same applies for the
        # rightmost cell
        if not self.left_cell:
            left = mid
        elif self.left_cell.is_alive:
            left = 1
        else:
            left = 0

        if not self.right_cell:
            right = mid
        elif self.right_cell.is_alive:
            right = 1
        else:
            right = 0
        # evaluate cells with respect to the current rule
        if USER_INPUT == 30:
            self.evaluate_rule_30(left, mid, right)
        elif USER_INPUT == 57:
            self.evaluate_rule_57(left, mid, right)

    def evaluate_rule_30(self, left, mid, right):
        if left:
            if mid and right:
                self.next_iter_alive = False
            elif mid and not right:
                self.next_iter_alive = False
            elif not mid and right:
                self.next_iter_alive = False
            elif not mid and not right:
                self.next_iter_alive = True
        else:
            if mid and right:
                self.next_iter_alive = True
            elif mid and not right:
                self.next_iter_alive = True
            elif not mid and right:
                self.next_iter_alive = True
            elif not mid and not right:
                self.next_iter_alive = False

    def evaluate_rule_57(self, left, mid, right):
        if left:
            if mid and right:
                self.next_iter_alive = False
            elif mid and not right:
                self.next_iter_alive = False
            elif not mid and right:
                self.next_iter_alive = True
            elif not mid and not right:
                self.next_iter_alive = True
        else:
            if mid and right:
                self.next_iter_alive = True
            elif mid and not right:
                self.next_iter_alive = False
            elif not mid and right:
                self.next_iter_alive = False
            elif not mid and not right:
                self.next_iter_alive = True

    def update_all(self):
        self.is_alive = self.next_iter_alive
        if self.left_cell:
            self.left_cell.update_left_cell()
        if self.right_cell:
            self.right_cell.update_right_cell()

    def update_left_cell(self):
        self.is_alive = self.next_iter_alive
        if self.left_cell:
            self.left_cell.update_left_cell()

    def update_right_cell(self):
        self.is_alive = self.next_iter_alive
        if self.right_cell:
            self.right_cell.update_right_cell()


def get_user_input_():
    global USER_INPUT
    valid_input = False
    while not valid_input:
        print("Enter the rule that will be applied by the cellular automaton\n"
              "Currently, you can either enter >>30<< or >>57<< : ")
        USER_INPUT = input()
        if USER_INPUT.isnumeric() and \
                (int(USER_INPUT) == 30 or int(USER_INPUT) == 57):
            valid_input = True
            USER_INPUT = int(USER_INPUT)
        else:
            print("INVALID INPUT....try again :/")


def main():
    # set size of the appearing window
    width = 960
    height = 490

    # set number of iterations to be executed
    nr_iterations = 110

    # set position of the first cell
    starting_x = (width / 2) - 1
    starting_y = 20

    # ask user which rule should be executed
    get_user_input_()

    # create window
    win = GraphWin("Cellular Automaton", width, height)
    starting_point = Point(starting_x, starting_y)
    first_cell = Cell(False, False, True, starting_point.x, starting_point.y)

    for iteration in range(nr_iterations):
        # fill space with right number of dead cells
        first_cell.add_left_cell()
        first_cell.add_right_cell()

    for iteration in range(nr_iterations):

        # output all current cells to window
        first_cell.output_all(win)
        # check which cells are going to live in the next iterations
        first_cell.check_iteration()
        # then update them to their new state
        first_cell.update_all()

    rule_x = width - 112
    rule_y = 42

    # create text-object
    rule_text = Text(Point(rule_x, rule_y), "Rule " + str(USER_INPUT))
    rule_text.setSize(27)
    rule_text.setFace("times roman")
    rule_text.setStyle("italic")
    rule_text.draw(win)

    win.getMouse()


if __name__ == '__main__':
    main()


