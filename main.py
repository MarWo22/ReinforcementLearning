import chess
from board import Board
from agent import Agent
import matplotlib.pyplot as plt
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

num_workers = mp.cpu_count()  

def main():
    compare_decay_factors()

def compare_hyper_parameters():
    hp_1 = run_experiment(0.1, 0.1, 0.95)
    hp_2 = run_experiment(0.2, 0.1, 0.95)
    hp_3 = run_experiment(0.4, 0.2, 0.95)
    hp_4 = run_experiment(0.1, 0.05, 0.9)
    hp_5 = run_experiment(0.2, 0.2, 0.9)
    hp_6 = run_experiment(0.2, 0.1, 0.9)

    # Applying savgol filter to smooth out the graph a little.
    plt.plot(savgol_filter(hp_1, 51, 3), label="alpha=0.1, epsilon=0.1, gamma=0.95")
    plt.plot(savgol_filter(hp_2, 51, 3), label="alpha=0.2, epsilon=0.1, gamma=0.95")
    plt.plot(savgol_filter(hp_3, 51, 3), label="alpha=0.4, epsilon=0.2, gamma=0.95")
    plt.plot(savgol_filter(hp_4, 51, 3), label="alpha=0.1, epsilon=0.05, gamma=0.9")
    plt.plot(savgol_filter(hp_5, 51, 3), label="alpha=0.2, epsilon=0.2, gamma=0.9")
    plt.plot(savgol_filter(hp_6, 51, 3), label="alpha=0.2, epsilon=0.1, gamma=0.9")
    plt.legend()
    plt.title("Winrate of different hyperparameters")
    plt.xlabel("Game Number")
    plt.ylabel("Winrate %")
    plt.show()

def compare_decay_factors():
    static = run_experiment(0.1, 0.1, 0.95)
    dynamic_099 = run_experiment(0.1, 0.1, 0.95, 0.99)
    dynamic_095 = run_experiment(0.1, 0.1, 0.95, 0.95)
    dynamic_090 = run_experiment(0.1, 0.1, 0.95, 0.9)

    plt.plot(savgol_filter(static, 51, 3), label="Static")
    plt.plot(savgol_filter(dynamic_099, 51, 3), label="Decaying factor=0.99")
    plt.plot(savgol_filter(dynamic_095, 51, 3), label="Decaying factor=0.95")
    plt.plot(savgol_filter(dynamic_090, 51, 3), label="Decaying factor=0.90")

    plt.legend()
    plt.title("Winrate of different decaying factors")
    plt.xlabel("Game Number")
    plt.ylabel("Winrate %")
    plt.show()




def run_experiment(alpha, epsilon, gamma, decay_factor=0):
    pool = mp.Pool(num_workers)
    processes = []
    for i in range(10):
        if decay_factor != 0:
            processes.append(pool.apply_async(train_agent_decay, args=(alpha, epsilon, gamma, decay_factor)))
        else:
            processes.append(pool.apply_async(train_agent_static, args=(alpha, epsilon, gamma)))
            
    results = np.zeros(5000, int)
    pool.close()
    pool.join()

    for i in range(10):
        results += processes[i].get()
    
    return results



def train_agent_decay(alpha, epsilon, gamma, decay_factor):
    agent = Agent(alpha, epsilon, gamma)
    outcomes = np.empty(5000, int)
    for i in range(5000):
        outcomes[i] = play_game(agent)
        if outcomes[i]:
            agent.decay_epsilon(decay_factor)
    
    winrate = (sum(outcomes) / len(outcomes)) * 100
    print("Job for alpha={alpha}, decaying epsilon={epsilon}, gamma={gamma} finished with an average winrate of {winrate}%".format(alpha=alpha, epsilon=epsilon, gamma=gamma, winrate=winrate))
    outcomes *= 10 # Multiply by 10 to get percentages
    return outcomes

def train_agent_static(alpha, epsilon, gamma):
    agent = Agent(alpha, epsilon, gamma)
    outcomes = np.empty(5000, int)
    for i in range(5000):
        outcomes[i] = play_game(agent)
    
    winrate = (sum(outcomes) / len(outcomes)) * 100
    print("Job for alpha={alpha}, static epsilon={epsilon}, gamma={gamma} finished with an average winrate of {winrate}%".format(alpha=alpha, epsilon=epsilon, gamma=gamma, winrate=winrate))
    outcomes *= 10 # Multiply by 10 to get percentages
    return outcomes


def play_game(agent):
    board = Board('8/8/8/2k5/8/6R1/3K4/8')
    while True:
        result = agent.play_turn(board)
        if result == "1-0":
            return 1
        elif result == "1/2-1/2":
            return 0
   


if __name__ == "__main__":
    main()