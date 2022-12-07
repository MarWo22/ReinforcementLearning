import environment
import agent
from matplotlib import pyplot as plt
import numpy as np

class Simulation:
    def __init__(self):
        ## Experiment settings
        self.epochs = 1000
        self.iterations = 1000

        # Hyper parameters
        self.k = 6
        self.epsilon = 0.3 # only used if EPSILON_GREEDY strategy is used
        self.c = 0.3 # only used if ACTION_PREFERENCE strategy is used
        self.optimistic_value = 10 # only used if OPTIMISTIC_INITIAL_VALUE strategy is used
        self.alpha = 0.1

    # Runs one iteration of k epochs and returns the history of rewards the agent received
    def run_iteration(self, strategy, problem_type):

        agent_instance = agent.Agent(self.k, strategy, self.epsilon, self.c, self.alpha, self.optimistic_value)
        environment_instance = environment.Environment(self.k, problem_type)

        for _ in range(self.epochs):
            action = agent_instance.take_action()
            reward, is_optimal = environment_instance.get_reward(action)
            agent_instance.reward(action, reward, is_optimal)
        
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
        rewards /= self.epochs
        correct_actions /= self.epochs
        return rewards, correct_actions

def main():
    simulation = Simulation()

    rewards_greedy, actions_greedy = simulation.run_experiment(agent.Strategy.GREEDY, environment.ProblemType.GAUSSIAN)
    rewards_epsilon, actions_epsilon = simulation.run_experiment(agent.Strategy.EPSILON_GREEDY, environment.ProblemType.GAUSSIAN)
    rewards_optimistic, actions_optimistic = simulation.run_experiment(agent.Strategy.OPTIMISTIC_INITIAL_VALUE, environment.ProblemType.GAUSSIAN)
    rewards_ucb, actions_ucb = simulation.run_experiment(agent.Strategy.UPPER_CONFIDENCE_BOUND, environment.ProblemType.GAUSSIAN)
    rewards_preference, actions_preference = simulation.run_experiment(agent.Strategy.ACTION_PREFERENCE, environment.ProblemType.GAUSSIAN)
    # Plot the rewards and correct action trajectory 
    plt.subplot(1, 2, 1)
    plt.plot(rewards_greedy, label="Greedy")
    plt.plot(rewards_epsilon, label="Epsilon Greedy")
    plt.plot(rewards_optimistic, label="Optimistic Initial Value")
    plt.plot(rewards_ucb, label="Upper Bound Confidence")
    plt.plot(rewards_preference, label="Action Preference")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(actions_greedy, label="Greedy")
    plt.plot(actions_epsilon, label="Epsilon Greedy")
    plt.plot(actions_optimistic, label="Optimistic Initial Value")
    plt.plot(actions_ucb, label="Upper Bound Confidence")
    plt.plot(actions_preference, label="Action Preference")
    plt.legend()

    plt.show()



if __name__ == "__main__":
    main()