from graphics import *


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
        # a neighbor being "False" is the same is the neighbor being dead
        if not self.left_cell or not self.left_cell.is_alive:
            left = 0
        else:
            left = 1
        if not self.right_cell or not self.right_cell.is_alive:
            right = 0
        else:
            right = 1

        if self.is_alive:
            mid = 1
        else:
            mid = 0
        self.evaluate_single_cell(left, mid, right)

    def evaluate_single_cell(self, left, mid, right):
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


def main():
    # set size of the appearing window
    width = 960
    height = 500

    # set number of iterations to be executed
    nr_iterations = 110

    # set position of the first cell
    starting_x = (width / 2) - 1
    starting_y = 20

    # create window
    win = GraphWin("Rule 30", width, height)
    starting_point = Point(starting_x, starting_y)
    first_cell = Cell(False, False, True, starting_point.x, starting_point.y)

    for iteration in range(nr_iterations):
        # add two new cells at each step (those new cells could only
        # have been dead until now, so we can just construct them and
        # set them to "dead" at each iteration)
        first_cell.add_left_cell()
        first_cell.add_right_cell()

        # output all current cells to window
        first_cell.output_all(win)
        # check which cells are going to live in the next iterations
        first_cell.check_iteration()
        # then update them to their new state
        first_cell.update_all()

    # set coordinates of the rule-text
    rule_x = width - 95
    rule_y = 40

    # create text-object
    rule_text = Text(Point(rule_x, rule_y), "Rule 30")
    rule_text.setSize(27)
    rule_text.setFace("times roman")
    rule_text.setStyle("italic")
    rule_text.draw(win)

    win.getMouse()


if __name__ == '__main__':
    main()


