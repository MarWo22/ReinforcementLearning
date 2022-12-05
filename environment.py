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
            self.rewards = [random.uniform(1,2) for _ in range(k)]
        elif problem_type == ProblemType.BERNOULI:
            self.rewards = [random.random() for _ in range(k)]
        else:
            print("Invalid problem type")
        print(self.rewards)
        print("testing")
    	


    def gaussian_reward(self, action):
        return np.random.normal(self.rewards[action])

    def bernouli_reward(self, action):
        if random.random < self.rewards[action]:
            return 1
        return 0

    def reward(self, action):
        if self.problem_type == ProblemType.GAUSSIAN:
            return self.gaussian_reward(action)
        elif self.problem_type == ProblemType.BERNOULI:
            return self.bernouli_reward(action)
        print("Invalid problem type")