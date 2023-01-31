import chess
import random
from board import Board
import numpy as np

class Agent:
    def __init__(self, alpha, epsilon, gamma, decay_factor = 1):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.decay_factor = decay_factor
        self.q_values = {}

    # Trains the agent using q-learning for 'epoch' games
    def train(self, epochs):
        print("Started process with {epochs} epochs with epsilon={epsilon}, alpha={alpha}, gamma={gamma}, decay_factor={decay_factor}".format(epochs=epochs, epsilon=self.epsilon, alpha=self.alpha, gamma=self.gamma, decay_factor=self.decay_factor))
        wins = 0
        winrates = np.empty(epochs)
        for epoch in range(epochs):
            # Create new board
            board = Board()
            result = "*"
            # Keep playing untill the game is over
            while result == "*":
                result = self.play_turn(board)

            # Decay if result is a win
            if result == "1-0":
                self.decay_epsilon(self.decay_factor)
                wins += 1

            # Calculate the winrate for this epoch
            winrates[epoch] = (wins / (epoch + 1)) * 100
        print("Finished process with {epochs} epochs with epsilon={epsilon}, alpha={alpha}, gamma={gamma}, decay_factor={decay_factor} with a average winrate of {winrate}%".format(epochs=epochs, epsilon=self.epsilon, alpha=self.alpha, gamma=self.gamma, decay_factor=self.decay_factor, winrate=winrates[epochs-1]))
        return winrates

    # Chooses an action, plays the turn, and updates the q-values
    def play_turn(self, board) -> str:
        curr_state = board.state()
        
        # Makes sure to add the actions if they aren't in the dictionary
        if curr_state not in self.q_values:
            self.q_values[curr_state] = {a: 0 for a in board.legal_moves()}

        # Choose a move
        move = self._get_move(board)
        # Play the move
        outcome = board.make_move(move)
        # Calculate the reward
        reward = self._get_reward(board, outcome)
        # Update the q-values with said reward and move
        self._update_q_values(board, curr_state, move, reward)
        return outcome

    # Updates the q-value of the agent based on the state, move and reward
    def _update_q_values(self, board, old_state, move, reward):

        new_state = board.state()
        new_moves = board.legal_moves()
        color = old_state[1]

        # Makes sure to add the actions to the dict if they aren't present
        if new_state not in self.q_values:
            self.q_values[new_state] = {a: 0 for a in new_moves}

        # Q-value is 0 if there are no available moves
        if not self.q_values[new_state]:
            q_val = 0
        else:
            # Get the max q_value for white, and the min q_value for black
            if color == chess.WHITE:
                q_val = max(self.q_values[new_state].values())
            else:
                q_val = min(self.q_values[new_state].values())

        # Updates the q-value of that state
        curr = self.q_values[old_state][move]
        self.q_values[old_state][move] = curr + self.alpha * (reward + self.gamma * q_val - curr)


    # Calculates the reward based on the outcome
    def _get_reward(self, board, outcome) -> int:

        if outcome == "1/2-1/2":
            return -100
        elif outcome == "1-0":
            return 100
        else:
            return (10 - (board.kings_distance() + board.black_king_border_distance()))

    # Returns the move the agent will play
    def _get_move(self, board) -> chess.Move:

        if random.random() < self.epsilon:
            return random.choice(board.legal_moves())
        else:
            return self._optimal_move(board)
    
    # Returns the optimal move the agent can play
    def _optimal_move(self, board) -> chess.Move:
        state = board.state()
        color = state[1]

        # Chose a random move if the q-values aren't known yet
        if state not in self.q_values or not self.q_values[state]:
            return random.choice(board.legal_moves())
        else:
            # Otherwise, select the max move for white, and the min move for black
            if color == chess.WHITE:
                return max(self.q_values[state], key=self.q_values[state].get)
            else:
                return min(self.q_values[state], key=self.q_values[state].get)

    # Reduces epsilon by decay_factor
    def decay_epsilon(self, decay_factor):
        self.epsilon *= decay_factor