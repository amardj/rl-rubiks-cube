# This class will start playing with the Rubik's Cube.

from typing import Any
from typing import List
from typing import Tuple
from typing import Dict
from typing import Mapping
from typing import NoReturn

import time, copy, random

from agent import Agent
from q_learning_impl import perform_Q_learning


class Play:

    def __init__(self):
        agent = Agent()

        print('\n', "Performing the registration of patter database, please wait for a while ............ \n")
        agent.register_patterns()

        print("\n Printing the QValues : ")
        print("\n\t", agent.QV)

        epsilons = [i / 50 for i in range(50)]
        epsilons.reverse()

        for i in range(2):
            for j, e in enumerate(epsilons):
                print("\n\n************************************** ROUND " + str(
                    j) + " ***********************************")
                perform_Q_learning(agent, epsilon=e)

        print("\n*** there are " + str(len(agent.QV)) + " keys in Q Table", '\n')

        print(
            "\n The Play Begins : **********************************************************************************\n")
        agent.start()

        agent.display()


Play()
