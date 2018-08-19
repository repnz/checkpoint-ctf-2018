import ast
from pprint import pprint


class Cube(object):
    TOP_INDEX = 0
    RIGHT_INDEX = 1
    BOTTOM_INDEX = 2
    LEFT_INDEX = 3

    def __init__(self, id, top, right, bottom, left):
        self.id = id
        self.rotation_index = 0
        self.free = True
        self.slices = [top, right, bottom, left]

    def rotate_clockwise(self, times=1):
        self.rotation_index += times
        self.slices = self.slices[times:] + self.slices[:times]

    def left(self):
        return self.slices[Cube.LEFT_INDEX]

    def right(self):
        return self.slices[Cube.RIGHT_INDEX]

    def top(self):
        return self.slices[Cube.TOP_INDEX]

    def bottom(self):
        return self.slices[Cube.BOTTOM_INDEX]

    def __str__(self):
        return 'Cube(id={id}, top={top}, right={right}, bottom={bottom}, left={left})'.format(
            id=self.id,
            top=self.top(),
            right=self.right(),
            bottom=self.bottom(),
            left=self.left()
        )

    def __repr__(self):
        return str(self)

    def has_combination(self, a, b):
        for i in xrange(-1, 3):
            if self.slices[i] == a and self.slices[i+1] == b:
                return True
            if self.slices[i] == b and self.slices[i+1] == a:
                return True

    def has_slice(self, slice_number):
        return slice_number in self.slices

    def has_double_slice(self, slice_number):
        return (self.top() == slice_number or self.bottom() == slice_number) and \
               (self.right() == slice_number or self.left() == slice_number)

    def is_corner(self):
        return self.has_slice(0)

    def is_double_edge(self):
        return self.has_double_slice(0)

    def to_cube_str(self):
        return "{0}, {1}".format(self.id, self.slices)

    @staticmethod
    def parse_cube(cube_str):
        id, slices = cube_str.split(',', 1)
        return Cube(int(id), *ast.literal_eval(slices))


def get_cube_set(cubes, slice_number):
    return [cube for cube in cubes if cube.has_slice(slice_number)]


class BoardSolver(object):
    def __init__(self, board_str):
        self.cubes = [Cube.parse_cube(cube_str) for cube_str in board_str.split('; ')]
        self.combination_options = {(a, b): self.get_combination_set(a, b) for b in xrange(20) for a in xrange(20)}
        self.options = {i: get_cube_set(self.cubes, i) for i in xrange(20)}
        self.double_edges = filter(Cube.is_double_edge, self.cubes)
        self.corners = filter(Cube.is_corner, self.cubes)
        self.stack = []

    def get_combination_set(self, a, b):
        return [cube for cube in self.cubes if cube.has_combination(a, b)]

    def solve_iter(self):
        current_top = 0
        current_left = 0
        current_right = None
        current_bottom = None
        stack = []

        while len(stack) != 100:
            options = self.combination_options[(current_top, current_right)]

            if not options:
                while True:
                    options, selected_option_index = stack[-1]
                    options[selected_option_index].free = True
                    selected_option_index += 1

                    if selected_option_index >= len(options) or not options[selected_option_index].free:
                        stack.pop()
                        continue

                    stack[-1] = options, selected_option_index

    def solve(self, current_top, current_left, row, col):
        if col == 10:
            if row == 10:
                end_cube = self.combination_options[0, 0]

                if end_cube:
                    return [end_cube]
                else:
                    return False
            else:
                current_right = 0
                row += 1

        for option in self.combination_options[current_top, current_left]:
            if not option.free:
                continue
            option.free = False

            index_of_top = option.slices.index(current_top)
            option.rotate_clockwise(index_of_top)

            result = self.solve(option.top(), option.right(), row, col+1)

            if result:
                return [option] + result


def main():
    board_str = open('puzzle_board.txt', 'r').read()
    solver = BoardSolver(board_str)
    solver.solve()



if __name__ == '__main__':
    main()