import numpy as np
import random
from enum import Enum

class Strategy(Enum):
        GREEDY = 1
        EPSILON_GREEDY = 2
        OPTIMISTIC_INITIAL_VALUE = 3
        UPPER_CONFIDENCE_BOUND = 4
        ACTION_PREFERENCE = 5 

class Agent:
    
    def __init__(self, k, strategy, epsilon = 0.3):
        self.k = k
        self.strategy = strategy
        self.q_t = [0] * k
        self.actions_taken = [0] * k
        self.epsilon = epsilon

        self.rewards_received = []
        self.q_t_base = self.q_t.copy()
        self.actions_taken_base = self.actions_taken.copy()


    
    def greedy(self):
        return np.argmax(self.q_t)

    def epsilon_greedy(self):
        # Generate random digit [0-1]
        random_int = random.random()

        # Take a random action if that random value is lower or equal than epsilon
        if random_int <= self.epsilon:
            return random.randint(0, self.k - 1)

        return np.argmax(self.q_t)

    def optimistic_initial_value(self):
        return np.argmax(self.q_t)

    def upper_confidence_bound(self):
        pass

    def action_preference(self):
        pass

    # take_action returns the action of the agent using the strategy it was initialized with
    # A user should only use this function, unless they want to use a different strategy than it was initialized with,
    # in that case the individual strategy functions can be called
    def take_action(self):
        match self.strategy:
            case Strategy.GREEDY:
                return self.greedy()
            case Strategy.EPSILON_GREEDY:
                return self.epsilon_greedy()
            case Strategy.OPTIMISTIC_INITIAL_VALUE:
                return self.optimistic_initial_value()
            case Strategy.UPPER_CONFIDENCE_BOUND:
                return self.upper_confidence_bound()
            case Strategy.ACTION_PREFERENCE:
                return self.action_preference()
            case _:
                print("Unkown strategy")


    def reward(self, action, reward):
        sum_rewards = self.q_t[action] * self.actions_taken[action]
        self.q_t[action] = (sum_rewards + reward) / (self.actions_taken[action] + 1)
        self.actions_taken[action]  = self.actions_taken[action] + 1

        self.rewards_received.append(reward)

    # This function can be used to reset the agents internal representation back to the basic value
    def reset(self):
        self.q_t = self.q_t_base.copy()
        self.actions_taken = self.actions_taken_base.copy()
        self.rewards_received = []

    def get_reward_history(self):
        return np.array(self.rewards_received)