

"""
class Type(Enum):
        MDP = 1
        RANDOM = 2

class Agent:

    def __init__(self, color) -> None:
        self.alpha = 0.1
        self.epsilon = 0.2
        self.gamma = 0.95
        self.color = color
        self.index = 0
        pass


    


    def make_move(self, board, state_values):
        current_actions = board.legalMoves()
        current_state = board.fen_state()
        if random.random() < self.epsilon * 0.5**self.index:
            if len(list(current_actions)) > 0:
                action = random.choice(list(current_actions))
            else:
                action = chess.Move.null()

            if current_state not in state_values:
                state_values[current_state] = dict()
                for action in current_actions:
                    state_values[current_state][action.uci()] = 0
        else:
            action =  self._get_optimal_action(board, state_values)

        if action == None:
            action = chess.Move.null()

        outcome = board.makeMove(action)

        self.index += 1
        reward = self._get_reward(board, outcome)
        self.update_state_values(board, state_values, current_state, action.uci(), reward)
        return outcome
        
    def _get_q_after_oponent(self, board, state_values):
        actions = board.legalMoves()
        max_q_values = list()
        for action in actions:
            state = board.get_next_fen_state(action)
            max_next_q = 0
            if state in state_values:
                for _, val in state_values[state].items():
                    max_next_q = max(max_next_q, val)

            max_q_values.append(max_next_q)
        if len(max_q_values) == 0:
            return 0
        return min(max_q_values)

    def _get_reward(self, board, outcome):
        a, b = 1, 1
        
        if outcome == None:
            king_distance = board.kings_distance()
            black_king_border_distance = board.black_king_border_distance()
            return ((6 - king_distance) * 100000 + (3 - black_king_border_distance)) * self.color
        else:
            if outcome.winner:
                return 100 * self.color
            else:
                return -100 * self.color

    def _get_action(self, state, actions, q_values):

        if len(actions) == 0:
            return chess.Move.null()

        if random.random() < self.epsilon:
            return random.choice(actions)

        best_action = None
        best_value = -10000
        if state in q_values:
            for action in actions:
                q_values[state][action] = 0

        for action in q_values[state]:
            if q_values[action] > best_value:
                best_value = q_values[action]
                best_action = action

        return best_action


    # (action, reward)
    def update_state_values(self, board, state_values, state, action, reward):

        if action == "0000":
            state_values[state][action] = 0
                
        state_values[state][action] = state_values[state][action] + self.alpha * (reward + self.gamma * self._get_q_after_oponent(board, state_values) - state_values[state][action])



# (black king distance from edge * A + distance between kings * B) * side
# wit side = 1, zwart side = -1
"""

import chess
import random

class Agent:
    def __init__(self, color):
        self.alpha = 0.1
        self.epsilon = 0.1
        self.gamma = 0.95
        self.color = color
        self.state_values = {}

    def make_move(self, board):
        current_actions = list(board.legal_moves)
        if not current_actions:
            current_actions = [chess.Move.null()]
        current_state = board.fen()

        if random.random() < self.epsilon:
            action = random.choice(current_actions)
        else:
            action = self._get_optimal_action(current_actions, current_state)

        board.push(action)
        outcome = board.result()
        reward = self._get_reward(current_state, board.fen(), outcome)
        self.update_state_values(current_state, action, reward)

        return outcome

    def _get_optimal_action_verbose(self, actions, state):
        best_action = None
        best_value = -1000000

        if state not in self.state_values:
            self.state_values[state] = {a: 0 for a in actions}

        for action in actions:
            print(action)
            if self.state_values[state][action] > best_value:
                best_action = action
                best_value = self.state_values[state][action]
                print(best_value)

        print("\n\n")
        print(best_action)
        return best_action

    def _get_optimal_action(self, actions, state):

        if state not in self.state_values:
            self.state_values[state] = {a: 0 for a in actions}

        return max(self.state_values[state], key=self.state_values[state].get)

    def _get_reward(self, old_state, new_state, outcome):
        if outcome == "1/2-1/2":
            if self.color == chess.BLACK:
                return 100
            return -100
        elif (outcome == "1-0" and self.color == chess.WHITE):
            return 100
        elif (outcome == "0-1" and self.color == chess.BLACK):
            return -100
        elif (self.color == chess.BLACK):
            return -1 * self.intermediate_reward(chess.Board(old_state), chess.Board(new_state))
        else:
            return self.intermediate_reward(chess.Board(old_state), chess.Board(new_state))

    def update_state_values(self, state, action, reward):
        if state not in self.state_values:
            self.state_values[state] = {a: 0 for a in chess.Board(state).legal_moves}

        if action == chess.Move.null() and chess.Move.null() not in self.state_values[state]:
            self.state_values[state][chess.Move.null()] = 0
        

        next_state_values = list()
        for a in chess.Board(state).legal_moves:
            next_state_value = self.state_values.get(self.get_next_fen(state, a))
            if next_state_value:
                next_state_values.append(max(next_state_value.values()))

        max_next_value = max(next_state_values) if next_state_values else 0
        self.state_values[state][action] += self.alpha * (reward + self.gamma * max_next_value - self.state_values[state][action])
        
    
    def get_next_fen(self, state, action):
        board = chess.Board(state)
        board.push(action)
        return board.fen()

    def intermediate_reward(self, old_board, new_board):
        return self.kings_distance(old_board) - self.kings_distance(new_board) + self.black_king_border_distance(old_board) - self.black_king_border_distance(new_board)

    def kings_distance(self, board):
        white_king_pos = board.pieces(6, True).pop()
        black_king_pos = board.pieces(6, False).pop()
        return chess.square_distance(white_king_pos, black_king_pos)

    def black_king_border_distance(self, board):
        black_king_pos = board.pieces(6, True).pop()
        black_king_file = chess.square_file(black_king_pos)
        black_king_rank = chess.square_rank(black_king_pos)
        return min(7-black_king_file, 7+black_king_file, 7+black_king_rank, 7-black_king_rank)

    def q_values(self):
        return self.state_values