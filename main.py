from board import Board
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt

# We represent states as a dictionary, where each state is an entry
state_values = dict()

def main():
    results = list()
    for i in range(100000):
        #print("running", i)
        results.append(play_game())

    averages = list()
    for i in range(1000):
        averages.append(sum(results[i*100: (i+1)*100]) / len(results[i*100: (i+1)*100]))

    plt.plot(averages)
    plt.show()

def play_game():
    board = Board('8/8/8/2k5/8/2K3Q1/8/8')
    agent1 = Agent()
    agent2 = Agent()

    agent1_actions = list()
    agent2_actions = list()
    agent_1_won = 0

    while True:
        outcome = agent1.make_move(board, state_values)
        if outcome is not None:
            if outcome.winner:
                print("agent 1 won")
                agent_1_won = 1
                agent1_actions.append((board.fen_state(), 1))
                agent2_actions.append((board.fen_state(), -1))
            else:
                print("draw")
                agent1_actions.append((board.fen_state(), -0.1))
                agent2_actions.append((board.fen_state(), -0.1))
            #board.printBoard()
            break

        agent1_actions.append((board.fen_state(), 0))


        outcome = agent2.make_move(board, state_values)
        if outcome is not None:
            if outcome.winner:
                print("agent 2 won")
                agent1_actions.append((board.fen_state(), -1))
                agent2_actions.append((board.fen_state(), 1))
            else:
                print("draw")
                agent1_actions.append((board.fen_state(), -0.1))
                agent2_actions.append((board.fen_state(), -0.1))
            #board.printBoard()
            break

        agent2_actions.append((board.fen_state(), 0))

    agent1.update_state_values(state_values, agent1_actions)
    agent2.update_state_values(state_values, agent2_actions)
    return agent_1_won

if __name__ == "__main__":
    main()