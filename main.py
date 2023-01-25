import chess
from agent import Agent
import matplotlib.pyplot as plt


def main():
    agents = (Agent(1), Agent(-1))
    for i in range(1000):
        play_game(agents)
    print(agents[0].q_values())


def play_game(agents):
    board = chess.Board('8/8/8/2k5/8/2K3Q1/8/8')

    idx = 0
    while True:
        outcome1 = agents[idx % 2].make_move(board)
        outcome2 = agents[idx % 2].make_move(board)
        #print(board)
        if outcome1 != '*':
            if outcome1 == "1/2-1/2":
                print("draw")
            else:
                print("white won")
                print(board)
            break

        idx+=1


if __name__ == "__main__":
    main()