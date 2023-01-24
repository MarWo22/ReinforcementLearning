from enum import Enum
import chess
import random

class Type(Enum):
        MDP = 1
        RANDOM = 2

class Agent:

    def __init__(self) -> None:
        self.alpha = 0.1
        self.epsilon = 0.1
        self.gamma = 0.99
        pass

    def make_move(self, board, state_values):
        moves = board.legalMoves()
        if random.random() < self.epsilon:
            choice = random.choice(list(moves))
        else:
            choice =  self._get_optimal_action(board, state_values)

        return board.makeMove(choice)

    def _get_optimal_action(self, board, state_values):
        optimal_action = None
        optimal_value = -10000

        for action in board.legalMoves():
            state_after_move = board.get_next_fen_state(action)

            if state_after_move in state_values:
                value = state_values[state_after_move]
            else:
                value = 0

            if value > optimal_value:
                optimal_action = action
                optimal_value = value
        
        if optimal_action is not None:
            return optimal_action

        return optimal_action

    def update_state_values(self, state_values, actions):
        gained_reward = actions[-1][1]
        for i, action in enumerate(reversed(actions)):
            if action[0] not in state_values:
                state_values[action[0]] = 0

            state_values[action[0]] = state_values[action[0]] + self.alpha * ((self.gamma**i) * gained_reward - state_values[action[0]])

