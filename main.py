from agent import Agent
import matplotlib.pyplot as plt
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt

num_workers = mp.cpu_count()  

def main():
    compare_to_random_agent(epochs=25000)

def compare_hyper_parameters(epochs=10000):
    hp_1 = run_experiment(0.1, 0.05, 0.99, epochs=epochs)
    hp_2 = run_experiment(0.2, 0.1, 0.99, epochs=epochs)
    hp_3 = run_experiment(0.5, 0.2, 0.95, epochs=epochs)
    hp_4 = run_experiment(0.1, 0.1, 0.95, epochs=epochs)
    hp_5 = run_experiment(0.2, 0.05, 0.90, epochs=epochs)
    hp_6 = run_experiment(0.5, 0.2, 0.90, epochs=epochs)

    # Applying savgol filter to smooth out the graph a little.
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

def compare_decay_factors(epochs=10000):
    static = run_experiment(0.1, 0.1, 0.95, epochs=epochs)
    dynamic_099995 = run_experiment(0.1, 0.1, 0.95, epochs=epochs, decay_factor=0.99995)
    dynamic_09995 = run_experiment(0.1, 0.1, 0.95, epochs=epochs, decay_factor=0.9995)
    dynamic_0995 = run_experiment(0.1, 0.1, 0.95,  epochs=epochs, decay_factor=0.995)
    dynamic_095 = run_experiment(0.1, 0.1, 0.95,  epochs=epochs, decay_factor=0.95)
    dynamic_090 = run_experiment(0.1, 0.1, 0.95,  epochs=epochs, decay_factor=0.90)
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

def compare_to_random_agent(epochs = 10000):
    trained = run_experiment(0.1, 0.1, 0.95, epochs=epochs, decay_factor=0.9995)
    random_agent = run_experiment(0.1, 1, 0.95, epochs=epochs)

    plt.plot(trained, label="Learning agent")
    plt.plot(random_agent, label="Random agent")

    plt.legend()
    plt.title("Winrate compared to random agent")
    plt.xlabel("Game Number")
    plt.ylabel("Winrate %")
    plt.show()


def run_experiment(alpha, epsilon, gamma, epochs=20000, decay_factor=1):
    pool = mp.Pool(num_workers)
    processes = []
    for i in range(6):
        processes.append(pool.apply_async(Agent(alpha, epsilon, gamma, decay_factor).train, args=(epochs,)))
            
    results = np.zeros(epochs, float)
    pool.close()
    pool.join()

    for i in range(6):
        results += processes[i].get()
    
    return results / 6
   


if __name__ == "__main__":
    main()