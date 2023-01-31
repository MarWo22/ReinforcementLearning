from agent import Agent
import matplotlib.pyplot as plt
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt

num_workers = mp.cpu_count()  

def main():
    #compare_hyper_parameters(epochs=100000)
    #compare_decay_factors(epochs=100000)
    compare_to_random_agent(epochs=250000)

# Function to compare 6 different sets of hyperparameters
def compare_hyper_parameters(epochs=10000):
    hp_1, winrate1 = run_experiment(0.1, 0.05, 0.99, epochs=epochs)
    hp_2, winrate2 = run_experiment(0.2, 0.1, 0.99, epochs=epochs)
    hp_3, winrate3 = run_experiment(0.5, 0.2, 0.95, epochs=epochs)
    hp_4, winrate4 = run_experiment(0.1, 0.1, 0.95, epochs=epochs)
    hp_5, winrate5 = run_experiment(0.2, 0.05, 0.90, epochs=epochs)
    hp_6, winrate6 = run_experiment(0.5, 0.2, 0.90, epochs=epochs)

    # Saving the winrates to a txt file for later use in e.g. statistical tests
    winrates = {
        "alpha=0.1,epsilon=0.05,gamma=0.99": winrate1,
        "alpha=0.2,epsilon=0.1,gamma=0.99": winrate2,
        "alpha=0.5,epsilon=0.2,gamma=0.95": winrate3,
        "alpha=0.1,epsilon=0.1,gamma=0.95": winrate4,
        "alpha=0.2,epsilon=0.05,gamma=0.90": winrate5,
        "alpha=0.5,epsilon=0.2,gamma=0.90": winrate6
    }

    save_dict_to_file("comparing_hyperparameters", winrates)


    # Plotting the graph
    plt.plot(hp_1, label="alpha=0.1, epsilon=0.05, gamma=0.99")
    plt.plot(hp_2, label="alpha=0.2, epsilon=0.1, gamma=0.99")
    plt.plot(hp_3, label="alpha=0.5, epsilon=0.2, gamma=0.95")
    plt.plot(hp_4, label="alpha=0.1, epsilon=0.1, gamma=0.95")
    plt.plot(hp_5, label="alpha=0.2, epsilon=0.05, gamma=0.90")
    plt.plot(hp_6, label="alpha=0.5, epsilon=0.2, gamma=0.90")
    plt.legend()
    plt.title("Winrate of different hyperparameters")
    plt.xlabel("Game Number")
    plt.ylabel("Winrate %")
    plt.show()

# Function to compare static epsilon-greedy to 5 decay variants
def compare_decay_factors(epochs=10000):
    static, winrate_static = run_experiment(0.2, 0.1, 0.99, epochs=epochs)
    dynamic_099995, winrate_dynamic_099995 = run_experiment(0.2, 0.1, 0.99, epochs=epochs, decay_factor=0.99995)
    dynamic_09995, winrate_dynamic_09995 = run_experiment(0.2, 0.1, 0.99, epochs=epochs, decay_factor=0.9995)
    dynamic_0995, winrate_0995 = run_experiment(0.2, 0.1, 0.99,  epochs=epochs, decay_factor=0.995)
    dynamic_095, winrate_095 = run_experiment(0.2, 0.1, 0.99,  epochs=epochs, decay_factor=0.95)
    dynamic_090, winrate_090 = run_experiment(0.2, 0.1, 0.99,  epochs=epochs, decay_factor=0.90)

    # Saving the winrates to a file for later use in e.g. statistical tests
    winrates = {
        "static": winrate_static,
        "0.99995": winrate_dynamic_099995,
        "0.9995": winrate_dynamic_09995,
        "0.995": winrate_0995,
        "0.95": winrate_095,
        "0.90": winrate_090,
    }

    save_dict_to_file("comparing_decay_factors", winrates)

    # Plotting the graph
    plt.plot(static, label="Static")
    plt.plot(dynamic_099995, label="Decaying factor=0.9995")
    plt.plot(dynamic_09995, label="Decaying factor=0.9995")
    plt.plot(dynamic_0995, label="Decaying factor=0.995")
    plt.plot(dynamic_095, label="Decaying factor=0.95")
    plt.plot(dynamic_090, label="Decaying factor=0.9")

    plt.legend()
    plt.title("Winrate of different decaying factors")
    plt.xlabel("Game Number")
    plt.ylabel("Winrate %")
    plt.show()

# Function to compare the optimal agent with a random agent
def compare_to_random_agent(epochs = 10000):
    trained, winrate_trained = run_experiment(0.2, 0.1, 0.99, epochs=epochs, decay_factor=0.9995)
    random_agent, winrate_random = run_experiment(0.1, 1, 0.95, epochs=epochs)

    # Saving the winrates to a file for later use in e.g. statistical tests
    winrates = {
        "trained": winrate_trained,
        "random": winrate_random,
    }

    save_dict_to_file("comparing_to_random", winrates)

    # Plotting the graph
    plt.plot(trained, label="Learning agent")
    plt.plot(random_agent, label="Random agent")

    plt.legend()
    plt.title("Winrate compared to random agent")
    plt.xlabel("Game Number")
    plt.ylabel("Winrate %")
    plt.show()


# Runs 6 agents in parallel, and returns the numpy array with the mean winrate over time, together with the winrate at the final game
def run_experiment(alpha, epsilon, gamma, epochs=20000, decay_factor=1):
    pool = mp.Pool(num_workers)
    processes = []
    final_winrates = []
    # Start all workers
    for i in range(6):
        processes.append(pool.apply_async(Agent(alpha, epsilon, gamma, decay_factor).train, args=(epochs,)))
            
    results = np.zeros(epochs, float)
    # Wait for the workers to finish
    pool.close()
    pool.join()

    # Get all results
    for i in range(6):
        single_run_result = processes[i].get()
        final_winrates.append(single_run_result[-1])
        results += single_run_result
    
    return results / 6, final_winrates
   
#Simple function to save a dictionary to a file
def save_dict_to_file(name, dict):
    f = open(name,'w')
    f.write(str(dict))
    f.close()


if __name__ == "__main__":
    main()