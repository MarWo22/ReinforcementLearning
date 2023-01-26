import chess
from board import Board
from agent import Agent
import matplotlib.pyplot as plt


def main():
    agent = Agent()
    outcomes = list()
    for _ in range(5000):
        outcomes.append(play_game(agent))
        agent.visited = []
    print(sum(outcomes) / len(outcomes))
    q_values = agent.q_values
    board = Board('8/8/8/2k5/8/6R1/3K4/8')
    board.print_board()
    result = "*"
    while result == "*":
        state = board.state()
        if state[1] == chess.WHITE:
            move = max(q_values[state], key=q_values[state].get)
        else:
            move = min(q_values[state], key=q_values[state].get)
        result = board.make_move(move)
        board.print_board()
        
    print(result)





def play_game(agent):
    board = Board('8/8/8/2k5/8/6R1/3K4/8')
    while True:
        result = agent.play_turn(board)
        if result == "1-0":
            print("White won")
            return 1
        elif result == "1/2-1/2":
            print("Draw")
            return 0
   


if __name__ == "__main__":
    main()