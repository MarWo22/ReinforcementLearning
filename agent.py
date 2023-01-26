import chess
import random

class Agent:
    def __init__(self):
        self.alpha = 0.5
        self.epsilon = 0.1
        self.gamma = 0.95
        self.q_values = {}
        self.visited = []

    def play_turn(self, board) -> str:
        curr_state = board.state()

        if curr_state not in self.q_values:
            self.q_values[curr_state] = {a: 0 for a in board.legal_moves()}

        move = self._get_move(board)
        outcome = board.make_move(move)
        reward = self._get_reward(board, outcome)
        self._update_q_values(board, curr_state, move, reward)
        self.visited.append(board.state())
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
            return 10 - (board.kings_distance() + board.black_king_border_distance())

        if outcome == "*": # Game still going on
            if color == chess.WHITE:
                return -1 # -1 reward for WHITE, since he wants to checkmate as fast as possible
            else:
                return 1 # 1 reward for BLACK, since he wants to delay the checkmate as long as possible

        elif outcome == "1-0": # WHITE won
            return 100 # Only achievable if WHITE is at play, returns high reward
        elif outcome == "1/2-1/2": # draw
            if color == chess.WHITE:
                return -100 # -100 reward for WHITE, since he needs (and can) win
            else:
                return 100 # 100 reward for BLACK, since he wants to draw (which should be impossible)

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

    def get_q_values(self):
        return self.q_values


