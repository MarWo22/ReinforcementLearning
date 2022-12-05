import environment
import agent
from matplotlib import pyplot as plt
import numpy as np

# USE NUMPY ARRAYS

class Simulation:
    def __init__(self):
        self.agent = agent.Agent(6, agent.Strategy.GREEDY)
        self.environment = environment.Environment(6, environment.ProblemType.GAUSSIAN)
        self.epochs = 1000
        self.iterations = 1000

    # Runs one iteration of k epochs and returns the history of rewards the agent received
    def run_iteration(self):
        for _ in range(self.epochs):
            action = self.agent.take_action()
            reward = self.environment.reward(action)
            self.agent.reward(action, reward)
        return self.agent.get_reward_history()

    def run_experiment(self):
        avg_rewards = np.zeros(self.epochs)
        for i in range(self.iterations):
            reward_history = self.run_iteration()
            avg_rewards = ((avg_rewards * i) + reward_history) / (i + 1)
            self.agent.reset()
            print("Iteration: ", i)
        return avg_rewards

def main():
    simulation = Simulation()
    avg_rewards = simulation.run_experiment()
    
    plt.plot(avg_rewards)
    plt.show()



if __name__ == "__main__":
    main()