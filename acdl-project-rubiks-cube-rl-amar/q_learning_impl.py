from typing import Any
from typing import List
from typing import Tuple
from typing import Dict
from typing import Mapping
from typing import NoReturn

import time
import copy
import random

from agent import Agent

__ALPHA = .6  # .6


# explore
def perform_Q_learning(agent: Agent, discount: float = 0.99, episodes : int = 10, epsilon : float = 0.9) -> None:
    """
    This is known as exploration phase. Perform Q-Learning for a given number of episodes
    :param agent:
    :param discount: The discount factor, range is (0,1].
    :param episodes: The number of episodes need to be performed.
    :param epsilon: The value of epsilon.
    :return:
    """

    # The current state of the
    print(agent.current_state)  # six_move_state()

    for i in range(episodes):
        print("\n====== EPISODE " + str(i) + " ======")
        print("==== CURR STATE ========")
        print("========================\n")
        # initialize values in Q-State dictionary for
        # any state action pairs including current state
        # that are null
        saved_rewards = agent.current_state.__hash__() in agent.rewards.keys()
        if not saved_rewards:
            agent.rewards[agent.current_state.__hash__()] = []
        if not agent.current_state.__hash__ in agent.visit_count:
            agent.visit_count[agent.current_state.__hash__()] = 1
        else:
            agent.visit_count[agent.current_state.__hash__()] += 1
        vc = agent.visit_count[agent.current_state.__hash__()]
        # initialize Q-Values of 0 for all state action pairs
        # for the given, state, if they do not exist
        for action in agent.actions:
            if not (agent.current_state.__hash__(), action) in agent.QV.keys():
                agent.QV[(agent.current_state.__hash__(), action)] = 0
            else:
                agent.num_of_revisits += 1
                break
            if not saved_rewards:
                agent.rewards[agent.current_state.__hash__()].append(agent.compute_rewards(agent.current_state, action))
        if 100 in agent.rewards[agent.current_state.__hash__()]:
            print("REACHED GOAL, END Q-LEARN ITERATION")
            return
        follow_policy = random.uniform(0, 1.0)
        print("Random value generated is " + str(follow_policy))
        # if random number is > epsilon, we must select best move
        # by the highest q-value
        if follow_policy > epsilon:
            print("\nFOLLOWING POLICY")
            for action in agent.actions:
                print("\tq value for action " + action + "\tfrom curr state is \t" + str(
                    agent.QV[(agent.current_state.__hash__(), action)]))
            best_action = None
            best_QV = -100000000
            for action in agent.actions:
                if agent.QV[(agent.current_state.__hash__(),
                             action)] > best_QV and action != agent.last_action and action != agent.second_last_action:
                    best_action = action
                    best_QV = agent.QV[(agent.current_state.__hash__(), action)]
            if best_QV == 0:
                best_action = random.choice(agent.actions)
                while best_action == agent.last_action:
                    best_action = random.choice(agent.actions)
            print("\n\t Actions chosen = " + best_action)
            agent.move[best_action] = agent.move[best_action] + 1
            # update Q-Value for current state and action chosen based on the current policy, by taking original Q-value, and adding
            # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
            # action on the new state, minus the original Q-Value
            # reward = agent.reward(agent.current_state, best_action)
            # max_reward = agent.max_reward(agent.current_state, best_action)
            # agent.QV[(agent.current_state.__hash__(), best_action)] = best_QV + ALPHA*(reward +\
            #                                         discount*max_reward - best_QV)

            for action in agent.actions:
                curr_QV = agent.QV[(agent.current_state.__hash__(), action)]
                reward = agent.compute_rewards(agent.current_state, action)
                max_reward = agent.max_reward_from_current_state(agent.current_state, action)

                agent.QV[(agent.current_state.__hash__(), action)] = \
                    curr_QV + __ALPHA * (reward + (discount ** vc) * max_reward - curr_QV)

            print("\n\t new q value for " + best_action + " action is " + str(
                agent.QV[(agent.current_state.__hash__(), best_action)]))

            agent.current_state.move(best_action)
            agent.current_state = agent.current_state.copy()

            if agent.current_state.is_goal_state_reached():
                print("\n\n reached goal state while in Q-learning epsiode " + str(i), "\n\n")
                # time.sleep(2)
                return

            agent.second_last_action = agent.last_action
            agent.last_action = best_action

        else:
            # pick random move
            action = random.choice(agent.actions)
            agent.move[action] = agent.move[action] + 1
            while action == agent.last_action or action == agent.second_last_action:
                action = random.choice(agent.actions)

            # update Q-Value for current state and randomly chosen action, by taking original Q-value, and adding
            # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
            # action on the new state, minus the original Q-Value
            # reward = agent.reward(agent.current_state, action)
            # max_reward = agent.max_reward(agent.current_state, action)
            # print("max reward... " + str(max_reward))
            # print("reward... " + str(reward))
            # agent.QV[(agent.current_state.__hash__(), action)] = curr_QV + ALPHA*(reward +\
            # discount*max_reward - curr_QV)
            reward = 0

            for action in agent.actions:
                curr_QV = agent.QV[(agent.current_state.__hash__(), action)]
                reward = agent.compute_rewards(agent.current_state, action)
                max_reward = agent.max_reward_from_current_state(agent.current_state, action)
                agent.QV[(agent.current_state.__hash__(), action)] = \
                    curr_QV + __ALPHA * (reward + (discount ** vc) * max_reward - curr_QV)

            # print(agent.reward(agent.current_state,action))
            # print(agent.QV[(agent.current_state,action)])
            agent.current_state.move(action)
            agent.current_state = agent.current_state.copy()
            agent.second_last_action = agent.last_action
            agent.last_action = action
            if agent.current_state.is_goal_state_reached():
                print("Reached goal state while in Q-learning episode : " + str(i))
                # time.sleep(2)
                return
