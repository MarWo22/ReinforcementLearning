import environment
import agent
import simulation
from matplotlib import pyplot as plt


# Main function that starts the simulation, runs an experiment for all strategies, and plots the average rewards and optimal action percentages
# Hyper parameters can be found in Simulation and altered there
# To run the simulation for different problem types, change problem_type_to_run
def main():
    simulation_instance = simulation.Simulation()

    # Change to use Guassian or Bernouli
    problem_type_to_run = environment.ProblemType.BERNOULI

    # Run the experiment for each strategy
    rewards_greedy, actions_greedy = simulation_instance.run_experiment(agent.Strategy.GREEDY, problem_type_to_run)
    rewards_epsilon, actions_epsilon = simulation_instance.run_experiment(agent.Strategy.EPSILON_GREEDY, problem_type_to_run)
    rewards_optimistic, actions_optimistic = simulation_instance.run_experiment(agent.Strategy.OPTIMISTIC_INITIAL_VALUE, problem_type_to_run)
    rewards_ucb, actions_ucb = simulation_instance.run_experiment(agent.Strategy.UPPER_CONFIDENCE_BOUND, problem_type_to_run)
    rewards_preference, actions_preference = simulation_instance.run_experiment(agent.Strategy.ACTION_PREFERENCE, problem_type_to_run)
    
    # Plot the rewards and correct action trajectory 
    plt.subplot(1, 2, 1)
    plt.plot(rewards_greedy, label="Greedy")
    plt.plot(rewards_epsilon, label="Epsilon Greedy")
    plt.plot(rewards_optimistic, label="Optimistic Initial Value")
    plt.plot(rewards_ucb, label="Upper Bound Confidence")
    plt.plot(rewards_preference, label="Action Preference")
    plt.title("Average rewards gained through time")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(actions_greedy, label="Greedy")
    plt.plot(actions_epsilon, label="Epsilon Greedy")
    plt.plot(actions_optimistic, label="Optimistic Initial Value")
    plt.plot(actions_ucb, label="Upper Bound Confidence")
    plt.plot(actions_preference, label="Action Preference")
    plt.title("Percentage of optimal actions taken through time")
    plt.legend()

    plt.show()



if __name__ == "__main__":
    main()