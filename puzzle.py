import copy

SIDES = 6
import time


# state object
class State:

    # Define the size of the Rubik's cube in parameter "size", where 3, means 3x3
    def __init__(self, size=3, c=None):
        self.size = size

        self.actions = ['front', 'back', 'left', 'right', 'up', 'down']

        if c:
            self.d = c
            self.__front__ = c["front"]
            self.__back__  = c["back"]
            self.__left__  = c["left"]
            self.__right__ = c["right"]
            self.__up__    = c["up"]
            self.__down__  = c["down"]

            self.__sides__ = [self.front(), self.back(), self.left(), self.right(), self.up(), self.down()]

            return

        # create and array of values 1-6 for different colors for cube faces
        # and multiply by number of pieces per size to get
        # equal amount of each color (white, blue, red, orange, green, yellow)

        '''nums = ['W','B','R','O','G','Y']*(size**2)
        
        # shuffle numbers

        shuffle(nums)

        front, nums = nums[0:size**2],nums[size**2:]
        self.__front__ = [front[i:i + size] for i in range(0,len(front), size)]

        back, nums = nums[0:size**2],nums[size**2:]
        self.__back__ = [back[i:i + size] for i in range(0,len(front), size)]

        left, nums = nums[0:size**2],nums[size**2:]
        self.__left__ = [left[i:i + size] for i in range(0,len(front), size)]

        right, nums = nums[0:size**2],nums[size**2:]
        self.__right__ = [right[i:i + size] for i in range(0,len(front), size)]

        up, nums = nums[0:size**2],nums[size**2:]
        self.__up__ = [up[i:i + size] for i in range(0,len(front), size)]

        down, nums = nums[0:size**2],nums[size**2:]
        self.__down__ = [down[i:i + size] for i in range(0,len(front), size)]'''

        self.__front__  = [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']]
        self.__back__   = [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        self.__up__     = [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']]
        self.__down__   = [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']]
        self.__left__   = [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']]
        self.__right__  = [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']]

        self.__sides__ = [self.front(), self.back(), self.left(), self.right(), self.up(), self.down()]

        self.d = {"front": self.front(), "back": self.back(), "left": self.left(), \
                  "right": self.right(), "up": self.up(), "down": self.down()}

    # return new copy of State using the copy library and a deep copy functionality
    def copy(self):
        # d = copy.deepcopy(self.d)
        copied_state = copy.deepcopy(self)
        return copied_state

    # equality tested for the cube
    def eq(self, other):
        return self.__left__ == other.left() and self.__right__ == other.right() \
               and self.__up__ == other.up() and self.__down__ == other.down() \
               and self.__front__ == other.front() and self.__back__ == other.back()

    # getters and setters for cube sides
    def left(self):
        return self.__left__

    def set_left(self, l):
        self.__left__ = l

    def right(self):
        return self.__right__

    def set_right(self, r):
        self.__right__ = r

    def up(self):
        return self.__up__

    def set_up(self, t):
        self.__up__ = t

    def down(self):
        return self.__down__

    def set_down(self, b):
        self.__down__ = b

    def front(self):
        return self.__front__

    def set_front(self, f):
        self.__front__ = f

    def back(self):
        return self.__back__

    def set_back(self, b):
        self.__back__ = b

    # randomly shuffle cube (applies n moves)

    # stringify a cube
    def __str__(self):
        return "\n\tFRONT\t" + str(self.__front__) + \
               "\n\tBACK\t"  + str(self.__back__)  + \
               "\n\tLEFT\t"  + str(self.__left__)  + \
               "\n\tRIGHT\t" + str(self.__right__) + \
               "\n\tUP\t\t"  + str(self.__up__)    + \
               "\n\tDOWN\t"  + str(self.__down__)

    def __hash__(self):
        return hash(self.__str__())

    # execute a 180 degreee rotation of a given side
    def rotate_side(self, side):
        new_side = [[], [], []]
        for i in reversed(range(self.size)):
            for y in range(self.size):
                new_side[self.size - 1 - i].append(side[i][self.size - 1 - y])
        return new_side

    # modify a side, rotating its rows to columns, either in left to right
    # or right to left order, depending on the reverse parameter
    def columns_to_rows(self, side, reverse=False):
        new_side = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # left to right order
                if not reverse:
                    row.append(side[self.size - 1 - j][i])
                # right to left order
                else:
                    row.append(side[j][self.size - 1 - i])
            new_side.append(row)
        return new_side

    # rotate the cube 90 degrees counter clockwise
    def rotate_cube(self):
        left_side = self.__left__
        self.__left__ = self.replace_side(self.__back__)
        front_side = self.__front__
        self.__front__ = self.replace_side(left_side)
        right_side = self.__right__
        self.__right__ = self.replace_side(front_side)
        self.__back__ = self.replace_side(right_side)
        self.__up__ = self.columns_to_rows(self.__up__, reverse=True)
        self.__down__ = self.columns_to_rows(self.__down__)

    # swap the first row of two given sides, in place
    def swap_first_row(self, side1, side2):
        s1_1 = side1[0]
        s2_1 = side2[0]
        # get rest of rows of side1
        new_side1 = [s2_1] + list(side for side in side1[1:])
        # get rest of rows of side2
        new_side2 = [s1_1] + list(side for side in side2[1:])
        return new_side1, new_side2

    # take the last element of each row of side 1, swap in place with
    # first element of reach row of side 2
    def swap_first_last_col(self, side1, side2):
        for i in range(len(side1)):
            side1[i][self.size - 1], side2[i][0] = side2[i][0], side1[i][self.size - 1]
        return side1, side2

    # given a new side, return a copy of this side,
    # to replace a given side of a cube
    def replace_side(self, side):
        new_side = []
        for row in side:
            new_side.append(row)
        return new_side

    # flip cube forward, from perspective of user looking at front
    # flipping such that front goes to down and up comes to front
    def flip_forward(self):
        front = self.__front__
        self.__front__ = self.replace_side(self.__up__)
        down = self.__down__
        self.__down__ = self.replace_side(front)
        back = self.__back__
        self.__back__ = self.replace_side(down)
        self.__up__ = self.replace_side(back)

    # flip cube backward, from perspective of user looking at front
    # flipping such that front goes to up and down goes to front
    def flip_backward(self):
        front = self.__front__
        self.__front__ = self.replace_side(self.__down__)
        up = self.__up__
        self.__up__ = self.replace_side(front)
        back = self.__back__
        self.__back__ = self.replace_side(up)
        self.__down__ = self.replace_side(back)

    # flip cube, either forward or backward, and invert
    # sides that must be inverted as a result
    def flip_cube(self, forward=False):
        # if flipping forward, we set front to be up
        # up to be back, back to be down, and down
        # to be front, we must then invert the back and front

        # if flipping backward, we set front to be down
        # up to be front, back to be up, and down to be
        # back, we must then invert the up and down
        if forward:
            self.flip_forward()
            self.__front__ = self.rotate_side(self.__front__)
            self.__back__ = self.rotate_side(self.__back__)
            self.__left__ = self.columns_to_rows(self.__left__)
            self.__right__ = self.columns_to_rows(self.__right__, reverse=True)
        else:
            self.flip_backward()
            self.__up__ = self.rotate_side(self.__up__)
            self.__down__ = self.rotate_side(self.__down__)
            self.__left__ = self.columns_to_rows(self.__left__, reverse=True)
            self.__right__ = self.columns_to_rows(self.__right__)

    # current move constraints: can only move clockwise
    # and can only turn the cube 180 degrees,
    # turn the front side to the right, causes the first
    # row of up/down to be swapped, and the first row of
    # left/right to be swapped, and the front face to be inverted
    # when we rotate a side, we are implementing it assuming that the
    # user turns their face to that side of the rubik's cube, then
    # does a 180 degree left rotation, this simplifies the implementation

    def turn_front(self):
        # invert the front side
        self.__front__ = self.rotate_side(self.__front__)
        # swap the first row of the left/right side, and swap
        # the last column of the left side with the first column of the right side
        self.__up__, self.__down__ = self.swap_first_row(self.__up__, self.__down__)
        self.__left__, self.__right__ = self.swap_first_last_col(self.__left__, self.__right__)

    def turn_back(self):
        # swap the last row of the left/right sides, and the first
        # row of the up/down sides
        # must rotate 90 degress twice
        self.rotate_cube()
        self.rotate_cube()
        self.turn_front()
        self.rotate_cube()
        self.rotate_cube()

    def turn_left(self):
        # left become front, front becomes right, right becomes back, back becomes left
        # up gets rotated 90 degrees counter clockwise
        # (3 6 9 -> 1 2 3) (2 5 8 -> 4 5 6) (1 4 7 -> 7 8 9)

        # must turn the cube 90 degrees counter clockwise to face the
        # left side of the cube, now as the front, then turn_front
        self.rotate_cube()
        self.turn_front()
        self.rotate_cube()
        self.rotate_cube()
        self.rotate_cube()

    def turn_right(self):
        # must make 3 90 degree rotations of the cube for the right
        # side to face front
        self.rotate_cube()
        self.rotate_cube()
        self.rotate_cube()
        self.turn_front()
        self.rotate_cube()

    def turn_up(self):
        self.flip_cube(forward=True)
        self.turn_front()
        self.flip_cube()

    def turn_down(self):
        self.flip_cube()
        self.turn_front()
        self.flip_cube(forward=True)

    def isGoalState(self):
        # check if all 3 lists that make up a side are equal
        # for every side, return false if this is not the case
        # e.g. side = [[1,1,1], [1,1,1], [1,1,2]]
        for side in self.__sides__:
            char = side[0][0]
            # check if all values in each row are equal
            # to the first value
            for row in side:
                if not char == row[0] == row[1] == row[2]:
                    return False
        return True

    def move(self, action):
        if action == 'left':
            self.turn_left()
        elif action == 'right':
            self.turn_right()
        elif action == 'front':
            self.turn_front()
        elif action == 'back':
            self.turn_back()
        elif action == 'up':
            self.turn_up()
        elif action == 'down':
            self.turn_down()
        self.__sides__ = [self.front(), self.back(), self.left(), self.right(), self.up(), self.down()]


# check number of pieces on each side of cube that match color
# of the middle piece of that side
def num_pieces_correct_side(state):
    correct = 0
    for side in state.__sides__:
        # get middle piece
        color = side[int(state.size / 2)][int(state.size / 2)]
        # subtract 1 to ignore middle cube
        correct -= 1
        for row in side:
            # filter items in each row that equal middle color
            # and add length of filtered list to total sum
            correct += row.count(color)
    return correct


def num_solved_sides(state):
    solved = 0
    for side in state.__sides__:
        color = side[0][0]
        # if number of pieces on this side equal to first square
        # is number of total pieces, side is solved
        if sum(row.count(color) for row in side) == state.size ** 2:
            solved += 1

    return solved


def num_crosses(state):
    crosses = 0
    for side in state.__sides__:
        color = side[1][1]
        if side[0][1] == color and side[1][0] == color and side[1][2] == color and side[2][1] == color:
            crosses += 1
    return crosses


def num_xs(state):
    xs = 0
    for side in state.__sides__:
        color = side[1][1]
        if side[0][0] == color and side[0][2] == color and side[2][0] == color and side[2][2] == color:
            xs += 1
    return xs


import random

def n_move_state(n=5):
    cube = State()
    return shuffle(cube, n=n)


def one_move_state():
    cube = State()
    cube.move(cube.actions[0])
    return cube


def shuffle(cube, n=5):
    new_cube = cube.copy()
    for _ in range(n):
        new_cube = random_move(new_cube)
    return new_cube


def random_move(cube):
    action = random.choice(cube.actions)
    print("executing " + action + " 180 rotation")
    cube = move(cube, action)
    return cube


def move(s, action):
    new_state = s.copy()
    if action == 'left':
        new_state.turn_left()
    elif action == 'right':
        new_state.turn_right()
    elif action == 'front':
        new_state.turn_front()
    elif action == 'back':
        new_state.turn_back()
    elif action == 'up':
        new_state.turn_up()
    elif action == 'down':
        new_state.turn_down()
    new_state.__sides__ = [new_state.front(), new_state.back(), new_state.left(), new_state.right(), new_state.up(),
                           new_state.down()]
    return new_state

# important features of a rubiks cube
# num. solved sides, highest priority
# num. of crosses
# num. of x's
# num. of pieces on correct sides
# num. of vertical/horizontal lines
