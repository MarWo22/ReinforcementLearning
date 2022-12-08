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
    
    # Initializes the agents with its hyperparameters
    def __init__(self, k, strategy, epsilon = 0.1, c = 0.1, alpha = 0.1, optimistic_value = 10):
        # Hyper parameters, all are initialized but only the ones related to the strategy are used
        self.k = k
        self.strategy = strategy
        self.epsilon = epsilon
        self.c = c
        self.alpha = alpha

        # Internal representations of policies/expected rewards
        if strategy == Strategy.OPTIMISTIC_INITIAL_VALUE:
            self.q_t = [optimistic_value] * k
        else:   
            self.q_t = [0] * k
        self.pi_t = [0] * k
        self.h_t = [0] * k

        # Other needed internal values
        self.rewards_received = []
        self.average_rewards = 0
        self.epoch = 0
        self.actions_taken = [0] * k
    
    # Uses Greedy to select an action
    def greedy(self):
        return np.argmax(self.q_t)

    # Uses Epsilon Greedy to select an action
    def epsilon_greedy(self):

        # Take a random action if that random value is lower or equal than epsilon
        if random.random() <= self.epsilon:
            return random.randint(0, self.k - 1)

        return np.argmax(self.q_t)

    # Uses Optimistic Initial Value to select an action
    def optimistic_initial_value(self):
        return np.argmax(self.q_t)

    # Uses Upper Confidence Bound to select an action
    def upper_confidence_bound(self):

        max_val = 0 
        max_idx = 0

        for i in range(self.k):
            val = self.q_t[i]
            # Calculate the uncertainty and add them to the value
            # If the action has not been taken before, the uncertainty is infinite, so it is set to high number
            if self.actions_taken[i] != 0:
                val += self.c * np.sqrt(np.log(self.epoch) / self.actions_taken[i])
            else:
                val += 10000
            
            if val > max_val:
                max_val = val
                max_idx = i

        return max_idx

    # Used Action Preference to select an action
    def action_preference(self):
        exp =  np.exp(self.h_t)
        self.pi_t = exp/np.sum(exp)
        # Selects a random index based on the probability
        return np.random.choice(a=range(len(self.pi_t)), p=self.pi_t)

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

    # Rewards the agent for its action
    def reward_agent(self, action, reward, is_optimal):
        
        # Update h_t if the strategy is action preference
        if self.strategy == Strategy.ACTION_PREFERENCE:
            if is_optimal:
                self.h_t[action] = self.h_t[action] + self.alpha * (reward - self.average_rewards) * (1 - self.pi_t[action])
            else:
                self.h_t[action] = self.h_t[action] - self.alpha * (reward - self.average_rewards) * self.pi_t[action]
        # Otherwise q_t is updated
        else:
            self.q_t[action] = self.q_t[action] + (1 / (self.actions_taken[action] + 1)) * (reward - self.q_t[action])
            self.actions_taken[action]  += 1

        # Keep track of the rewards the agent received and the average reward
        self.rewards_received.append(reward)
        self.average_rewards = (self.average_rewards * self.epoch + reward) / (self.epoch + 1)
        self.epoch += 1

    # Returns all rewards the agent has received
    def get_reward_history(self):
        return np.array(self.rewards_received)