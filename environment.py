from enum import Enum
import numpy as np
import random

class ProblemType(Enum):
    GAUSSIAN = 1
    BERNOULI = 2

class Environment:
    def __init__(self, k, problem_type):
        self.problem_type = problem_type
        if problem_type == ProblemType.GAUSSIAN:
            # Generate random floats between 1 and 4 for Gaussian rewards
            self.rewards = [random.uniform(1,4) for _ in range(k)]
        elif problem_type == ProblemType.BERNOULI:
            # Generate random floats between 0 an 1 for Bernouli rewards
            self.rewards = [random.random() for _ in range(k)]

        self.best_action = np.argmax(self.rewards)
        self.actions_chosen = []

    	

    # Returns a gaussian reward, picking from the gausian distribution with the random mean and a sd of 1
    def gaussian_reward(self, action):
        return np.random.normal(self.rewards[action])

    # Returns 1 or 0, based on probability
    def bernouli_reward(self, action):
        if random.random() < self.rewards[action]:
            return 1
        return 0

    # This function returns the reward from the environment, and keeps track of the action the agent has performed
    def get_reward(self, action):
        is_optimal = (action == self.best_action)
        if is_optimal:
            self.actions_chosen.append(1)
        else:
            self.actions_chosen.append(0)

        if self.problem_type == ProblemType.GAUSSIAN:
            return self.gaussian_reward(action), is_optimal
        elif self.problem_type == ProblemType.BERNOULI:
            return self.bernouli_reward(action), is_optimal

    # Returns the list of actions the agent has done, with each element being 1 if the action was optimal, or 0 if it was sub-optimal
    def get_actions_chosen(self):
        return np.array(self.actions_chosen)