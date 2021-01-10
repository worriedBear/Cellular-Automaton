from graphics import *


class Cell:
    left_cell = False
    right_cell = False

    is_alive = False
    starting_pos = Point(-1, -1)

    def __init__(self, left_cell, right_cell, is_alive, x_pos, y_pos):
        self.left_cell = left_cell
        self.right_cell = right_cell

        self.is_alive = is_alive
        self.starting_pos = Point(x_pos, y_pos)

    def output_cell(self, window):
        self.starting_pos.y += 4
        cell_rec = Rectangle(self.starting_pos,
                             Point(self.starting_pos.x + 2, self.starting_pos.y + 2))
        if self.is_alive:
            cell_rec.setFill("black")
            cell_rec.setOutline("black")
        else:
            cell_rec.setFill("grey")
            cell_rec.setOutline("grey")
        cell_rec.draw(window)

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

    def add_left_cell(self):
        if self.left_cell:
            self.left_cell.add_left_cell()
        else:
            x_pos = self.starting_pos.x - 4
            y_pos = self.starting_pos.y
            self.left_cell = Cell(False, self, True, x_pos, y_pos)

    def add_right_cell(self):
        if self.right_cell:
            self.right_cell.add_right_cell()
        else:
            x_pos = self.starting_pos.x + 4
            y_pos = self.starting_pos.y
            self.right_cell = Cell(self, False, True, x_pos, y_pos)


def main():
    width = 720
    height = 720

    starting_x = (width / 2) - 1
    starting_y = 20

    win = GraphWin("Rule 30", width, height)
    starting_point = Point(starting_x, starting_y)
    first_cell = Cell(False, False, True, starting_point.x, starting_point.y)

    for it in range(80):
        first_cell.output_all(win)

        first_cell.add_left_cell()
        first_cell.add_right_cell()

    win.getMouse()


if __name__ == '__main__':
    main()


