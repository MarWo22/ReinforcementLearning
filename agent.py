import chess
import random

class Agent:
    def __init__(self, alpha, epsilon, gamma):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.q_values = {}

    def play_turn(self, board) -> str:
        curr_state = board.state()

        if curr_state not in self.q_values:
            self.q_values[curr_state] = {a: 0 for a in board.legal_moves()}

        move = self._get_move(board)
        outcome = board.make_move(move)
        reward = self._get_reward(board, outcome)
        self._update_q_values(board, curr_state, move, reward)
        return outcome

    
    def _update_q_values(self, board, old_state, move, reward):

        new_state = board.state()
        new_moves = board.legal_moves()
        color = old_state[1]
        if new_state not in self.q_values:
            self.q_values[new_state] = {a: 0 for a in new_moves}

        if not self.q_values[new_state]:
            q_val = 0
        else:

            if color == chess.WHITE:
                q_val = max(self.q_values[new_state].values())
            else:
                q_val = min(self.q_values[new_state].values())

        curr = self.q_values[old_state][move]
        self.q_values[old_state][move] = curr + self.alpha * (reward + self.gamma * q_val - curr)


    def _get_reward(self, board, outcome) -> int:

        if outcome == "1/2-1/2":
            return -100
        elif outcome == "1-0":
            return 100
        else:
            return (10 - (board.kings_distance() + board.black_king_border_distance())) / 10

    def _get_move(self, board) -> chess.Move:

        if random.random() < self.epsilon:
            return random.choice(board.legal_moves())
        else:
            return self._optimal_move(board)
    
    def _optimal_move(self, board) -> chess.Move:
        state = board.state()
        color = state[1]
        if state not in self.q_values or not self.q_values[state]:
            return random.choice(board.legal_moves())
        else:
            if color == chess.WHITE:
                return max(self.q_values[state], key=self.q_values[state].get)
            else:
                return min(self.q_values[state], key=self.q_values[state].get)

    def decay_epsilon(self, decay_factor):
        self.epsilon *= decay_factor