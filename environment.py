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
            self.rewards = [random.uniform(1,4) for _ in range(k)]
        elif problem_type == ProblemType.BERNOULI:
            self.rewards = [random.random() for _ in range(k)]

        self.best_action = np.argmax(self.rewards)
        self.actions_chosen = []

    	


    def gaussian_reward(self, action):
        return np.random.normal(self.rewards[action])

    def bernouli_reward(self, action):
        if random.random() < self.rewards[action]:
            return 1
        return 0

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
        print("Invalid problem type")

    def get_actions_chosen(self):
        return np.array(self.actions_chosen)