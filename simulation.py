import environment
import agent
import numpy as np  

class Simulation:
    def __init__(self):
        ## Experiment settings
        self.epochs = 1000 # How many epochs the agent should learn
        self.iterations = 1000 # How many times it should be repeated

        # Hyper parameters
        self.k = 6
        self.epsilon = 0.1
        self.c = 0.3
        self.optimistic_value = 10
        self.alpha = 0.1

    # Runs one iteration of k epochs and returns the history of rewards the agent received
    def run_iteration(self, strategy, problem_type):

        agent_instance = agent.Agent(self.k, strategy, self.epsilon, self.c, self.alpha, self.optimistic_value)
        environment_instance = environment.Environment(self.k, problem_type)

        for _ in range(self.epochs):
            action = agent_instance.take_action()
            reward, is_optimal = environment_instance.get_reward(action)
            agent_instance.reward_agent(action, reward, is_optimal)
        
        return agent_instance.get_reward_history(), environment_instance.get_actions_chosen()

    def run_experiment(self, strategy, problem_type):
        # Initialize numpy arrays with zeroes to keep track of rewards and correct action history
        rewards = np.zeros(self.epochs)
        correct_actions = np.zeros(self.epochs)
        for i in range(self.iterations):
            # Run an iteration
            reward_history, action_history = self.run_iteration(strategy, problem_type)
            # Add the rewards and correct actions to the history arrays
            rewards += reward_history
            correct_actions += action_history

        # Gets the average of the rewards and correct action history array
        rewards /= self.iterations
        correct_actions /= self.iterations 
        correct_actions *= 100 # Multiply by 100 to get percentages
        return rewards, correct_actions