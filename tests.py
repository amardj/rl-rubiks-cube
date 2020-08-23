# first test, test front turn
# test that original first row of front is same as
# new bot row of front in reverse, same for original
# last row and new

import unittest
from puzzle import State, num_pieces_correct_side, num_solved_sides


def compareReverse(l1, l2):
    for i in range(len(l1)):
        if l1[i] != l2[len(l1) - 1 - i]:
            print("lists from compareReverse... " + str(l1) + "  " + str(l2))
            return False
    return True


def compare(l1, l2):
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            print(" lists from compare... " + str(l1) + "  " + str(l2))
            return False
    return True


class TestRotations(unittest.TestCase):

    def test_front_rotation(self):
        cube = State()
        # get three rows of front
        up_row = cube.front()[0]
        bot_row = cube.front()[2]
        mid_row = cube.front()[1]
        up_first_row = cube.up()[0]
        bot_first_row = cube.down()[0]
        left_third_col = [cube.left()[0][2], cube.left()[1][2], cube.left()[2][2]]
        right_first_col = [cube.right()[0][0], cube.right()[1][0], cube.right()[2][0]]
        cube.turn_front()
        up_row2 = cube.front()[0]
        up_first_row2 = cube.up()[0]
        bot_first_row2 = cube.down()[0]
        mid_row2 = cube.front()[1]
        bot_row2 = cube.front()[2]
        left_third_col2 = [cube.left()[0][2], cube.left()[1][2], cube.left()[2][2]]
        right_first_col2 = [cube.right()[0][0], cube.right()[1][0], cube.right()[2][0]]
        # check up row inverted and at down
        self.assertTrue(compareReverse(up_row, bot_row2))
        # check bot row inverted and at up
        self.assertTrue(compareReverse(bot_row, up_row2))
        # check mid row inverted in place
        self.assertTrue(compareReverse(mid_row, mid_row2))
        # check first up row move to first bot row
        self.assertTrue(compare(up_first_row, bot_first_row2))
        # check first bot row move to first up row
        self.assertTrue(compare(bot_first_row, up_first_row2))
        # check third col of left move to first col of right
        self.assertTrue(compare(left_third_col, right_first_col2))
        # check first col of right move to third col of left
        self.assertTrue(compare(right_first_col, left_third_col2))

    # test 90 degree counter clockwise cube rotation works
    def test_cube_rotation(self):
        cube = State()
        left = cube.left()
        right = cube.right()
        back = cube.back()
        front = cube.front()
        up = cube.up()
        up_r1 = up[0]
        up_r2 = up[1]
        up_r3 = up[2]
        down = cube.down()
        bot_r1 = down[0]
        bot_r2 = down[0]
        bot_r3 = down[0]
        print(cube)
        cube.rotate_cube()
        # check each original side is equal to what is now 90 degrees CC
        self.assertTrue(left == cube.front())
        self.assertTrue(front == cube.right())
        self.assertTrue(right == cube.back())
        self.assertTrue(back == cube.left())
        print(cube)
        self.assertTrue(compareReverse(up_r1, [cube.up()[0][0], cube.up()[1][0], cube.up()[2][0]]))
        self.assertTrue(compareReverse(up_r2, [cube.up()[0][1], cube.up()[1][1], cube.up()[2][1]]))
        self.assertTrue(compareReverse(up_r3, [cube.up()[0][2], cube.up()[1][2], cube.up()[2][2]]))


class TestGoalState(unittest.TestCase):

    # check that goal state returns true when we call isGoalState    
    def testIsSolvedState(self):
        c = {"front": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "back": [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
             "up": [[3, 3, 3], [3, 3, 3], [3, 3, 3]], "down": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
             "left": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "right": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]}
        cube = State(c=c)
        self.assertTrue(cube.isGoalState())

    # check that non goal state returns false when we call isGoalState
    def testIsNotSolvedState(self):
        c = {"front": [[1, 1, 1], [1, 2, 1], [1, 2, 1]], "back": [[2, 2, 3], [2, 3, 2], [2, 2, 3]],
             "up": [[3, 3, 3], [3, 3, 3], [3, 3, 3]], "down": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
             "left": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "right": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]}
        cube = State(c=c)
        self.assertFalse(cube.isGoalState())


class TestEquality(unittest.TestCase):

    def testAreEqual(self):
        c = {"front": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "back": [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
             "up": [[3, 3, 3], [3, 3, 3], [3, 3, 3]], "down": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
             "left": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "right": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]}
        cube1 = State(c=c)
        cube2 = State(c=c)
        self.assertTrue(cube1.eq(cube2))

    def testAreNotEqual(self):
        c1 = {"front": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "back": [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
              "up": [[3, 3, 3], [3, 3, 3], [3, 3, 3]], "down": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
              "left": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "right": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]}
        c2 = {"front": [[1, 1, 1], [1, 2, 1], [1, 2, 1]], "back": [[2, 2, 3], [2, 3, 2], [2, 2, 3]],
              "up": [[3, 3, 3], [3, 3, 3], [3, 3, 3]], "down": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
              "left": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "right": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]}
        cube1 = State(c=c1)
        cube2 = State(c=c2)
        self.assertFalse(cube1.eq(cube2))


class TestRewardHelpers(unittest.TestCase):
    def testCountSolvedSides(self):
        c1 = {"front": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "back": [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
              "up": [[3, 3, 3], [3, 3, 3], [3, 3, 3]], "down": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
              "left": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "right": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]}
        cube = State(c=c1)
        self.assertTrue(num_solved_sides(cube) == 6)

    def testNumPiecesCorrectSide(self):
        c1 = {"front": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "back": [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
              "up": [[3, 3, 3], [3, 3, 3], [3, 3, 3]], "down": [[4, 4, 4], [4, 4, 4], [4, 4, 4]],
              "left": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "right": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]}
        cube = State(c=c1)
        self.assertTrue(num_pieces_correct_side(cube) == 48)


if __name__ == "__main__":
    unittest.main()
