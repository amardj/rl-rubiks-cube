# This class defines the Agent for our Rubik's  Cube.

from typing import Any
from typing import List
from typing import Tuple
from typing import Dict
from typing import Mapping
from typing import NoReturn

import time, copy, random

from cube import Cube
import utils


class Agent:
    """
    Class level document block

    A cube is an instance of the class State()
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, QValues: Dict = None, cube: Cube = None):

        self.QV = QValues if QValues is not None else {}

        # initialize a cube state,
        # else create an initial random cube state by scrambling cube up 6 moves.

        print("\nThe current state of the Cube is : \t", cube, "\n")
        self.start_state = cube if cube is not None \
            else utils.initial_n_move_state(n=6)
        print("\nInitial state of the Cube is : ", self.start_state)

        # Initialize the rewards for the Agent. It maps a cube state to multiple
        # rewards possible for performing every possible outcome.
        self.rewards = {}

        # Save the current and previous states.
        self.current_state = self.start_state
        self.previous_state = None

        # Store all possible actions along with last action and second last action of the Agent.
        self.actions = self.start_state.actions
        self.last_action = None
        self.second_last_action = None

        # Maintain visited list, visited count, and number of revisits.
        self.visited = []
        self.visit_count = {}
        self.num_of_revisits = 0

        # Initialize all the moves to zero, 0.
        self.move = {"front": 0, "back": 0, "left": 0, "right": 0, "up": 0, "down": 0}

        # Pattern lists for associating the weights with the nodes
        # that are closer to the goal state.
        self.moves_away_1 = []
        self.moves_away_2 = []
        self.moves_away_3 = []
        self.moves_away_4 = []
        self.moves_away_5 = []
        self.moves_away_6 = []

    # ------------------------------------------------------------------------------------------------------------------
    def display(self):
        """ Display the current state of the Agent."""

        print("=============")
        x = 0
        y = 0

        for key in self.QV.keys():
            if self.QV[key] != 0:
                x += 1
            else:
                y += 1

        print("Number of Q values in dictionary is : " + str(x + y))
        print("Number of zero Q values are : " + str(y))
        print("Number of non-zero Q values are : " + str(x))
        print("Number of revisited states are : " + str(self.num_of_revisits))

        print(self.move)

    # ------------------------------------------------------------------------------------------------------------------
    def max_reward_from_current_state(self, cube: Cube, action) -> float:
        """
        Compute the maximum reward that the current state of the cube can get for any possible next single move.
        :param cube: The Cube.
        :param action: One of the action from the list of possible actions
        ['front', 'back', 'left', 'right', 'up', 'down']
        :return: The maximum reward possible from the current state for the next posible move.
        """
        next_cube_state = utils.move(cube, action)

        if not next_cube_state in self.rewards.keys():
            self.rewards[next_cube_state] = []

            for action in self.actions:
                self.rewards[next_cube_state].append(self.compute_rewards(next_cube_state, action))

        return max(self.rewards[next_cube_state])

    # ------------------------------------------------------------------------------------------------------------------
    def compute_rewards(self, cube: Cube, action) -> float:
        """
        The reward function for this Agent.

        The property of the reward function are :
        # this reward function should be a function approximation made up of
        # a set of features, these features should be in decreasing order of priority:
        # 1. solved faces ()
        # use next state to get value for next state vs. self.curr_state, to determine
        # if feature values should be 1 or 0, e.g. if solved_sides(next_state) > solved_sides(self.curr_state)
        # then the solved sides feature is 1, else 0
        """

        next_cube_state = utils.move(cube, action)

        if next_cube_state.is_goal_state_reached():
            print(cube)
            print(next_cube_state)
            print("REWARD IS GOAL")
            return 100

        reward = -0.1

        solved_faces = 2 * (utils.num_of_solved_faces(next_cube_state) < utils.num_of_solved_faces(cube))
        solved_facelets = 0.5 * (
                utils.num_of_solved_facelets(next_cube_state) < utils.num_of_solved_facelets(next_cube_state))

        if (next_cube_state.__hash__(), action) in self.QV.keys():
            reward -= 0.2

        reward -= solved_faces
        reward -= solved_facelets

        return reward

    # ------------------------------------------------------------------------------------------------------------------
    def register_patterns(self):
        """

        :return:
        """

        cube = Cube()

        # get list of goal successors
        for action in self.actions:
            next_cube_state = utils.move(cube, action)
            self.moves_away_1.append(next_cube_state)
            # Creating the QValues for the first move
            for temp_action in self.actions:
                self.QV[(next_cube_state.__hash__(), temp_action)] = -10 if temp_action != action else 10

        # get list of successors of goal successors
        for cube in self.moves_away_1:
            for action in self.actions:
                next_cube_state = utils.move(cube, action)
                self.moves_away_2.append(next_cube_state)
                for temp_action in self.actions:
                    self.QV[(next_cube_state.__hash__(), temp_action)] = -6 if temp_action != action else 6

        # get list of successors-successors of goal successors
        for cube in self.moves_away_2:
            for action in self.actions:
                next_cube_state = utils.move(cube, action)
                self.moves_away_3.append(next_cube_state)
                for temp_action in self.actions:
                    self.QV[(next_cube_state.__hash__(), temp_action)] = -5 if temp_action != action else 5

        # get list of successors-successors-successors of goal successors
        for cube in self.moves_away_3:
            for action in self.actions:
                next_cube_state = utils.move(cube, action)
                self.moves_away_4.append(next_cube_state)
                for temp_action in self.actions:
                    self.QV[(next_cube_state.__hash__(), temp_action)] = -4 if temp_action != action else 4

        # get list of successors-successors-successors-successors of goal successors
        for cube in self.moves_away_4:
            for action in self.actions:
                next_cube_state = utils.move(cube, action)
                self.moves_away_5.append(next_cube_state)
                for temp_action in self.actions:
                    self.QV[(next_cube_state.__hash__(), temp_action)] = -3 if temp_action != action else 3

        # get list of successors-successors-successors-successors-successors of goal successors
        for cube in self.moves_away_5:
            for action in self.actions:
                next_cube_state = utils.move(cube, action)
                self.moves_away_6.append(next_cube_state)
                for temp_action in self.actions:
                    self.QV[(next_cube_state.__hash__(), temp_action)] = -1 if temp_action != action else 1

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        """
        This will invoke the agent to solve the cube.
        :return:
        """

        # Get the start state for this agent
        self.current_state = self.start_state
        print("\n The Current state of the Cube : \n\t", self.current_state)

        self.second_last_action = None
        self.last_action = None

        for i in range(20):
            best_action = None
            best_QValue = -100000000

            if not (self.current_state.__hash__(), self.actions[0]) in self.QV.keys():

                best_action = random.choice(self.actions)

                while (best_action == self.second_last_action) or (best_action == self.last_action):
                    best_action = random.choice(self.actions)

                for action in self.actions:
                    self.QV[(self.current_state.__hash__(), action)] = 0

                best_QValue = 0

            else:

                for action in self.actions:

                    if (self.QV[(self.current_state.__hash__(), action)] > best_QValue) \
                            and (action != self.last_action and action != self.second_last_action):

                        best_action = action
                        best_QValue = self.QV[(self.current_state.__hash__(), action)]

                # if best_QV == 0:
                #    best_action = random.choice(self.actions)
                #    while best_action == self.last_action or best_action == self.second_last_action:
                #        best_action = random.choice(self.actions)

            print("Actions chosen : " + best_action)
            print("Last action : " + (self.last_action if self.last_action is not None  else "None"))
            print("Q value is : " + str(self.QV[(self.current_state.__hash__(), best_action)]))

            print('Sleeping for a second ............. ')
            #time.sleep(1)
            print('Awoke from the sleep!')

            self.current_state.move(best_action)
            self.second_last_action = self.last_action
            self.last_action = best_action

            print(self.current_state)

            if self.current_state.is_goal_state_reached():
                print("\n\n\n              The Agent has reached a Goal State !!!\n\n")

                # time.sleep(5)

                return

