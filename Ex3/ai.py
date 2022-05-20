import copy

from numpy import Infinity


class AI:

    def __init__(self, player=2):
        self.player = player

    # Minimax algorithm with alpha-beta pruning if player starts first
    def minimax_ab_1(self, board, maximizing, alpha, beta):

        # End of game state in visual board
        state = board.final_state()

        # Player 1 wins
        if state == 1:
            return 1, None

        # Player 2 wins
        if state == 2:
            return -1, None

        # Draw
        elif board.is_full():
            return 0, None

        if maximizing:
            max_score = -Infinity
            best_move = None
            empty_squares = board.get_empty()  # Get available squares to make a move

            for (row, col) in empty_squares: # Iterate through all available moves
                # Copy board to make it mutable
                copy_board = copy.deepcopy(board)
                copy_board.fill(row, col, 1)
                score = self.minimax_ab_1(copy_board, False, alpha, beta)[0]  # Evaluate min for ai move

                # If the evaluation is better than previous best, it becomes new best
                if score > max_score:
                    max_score = score
                    best_move = (row, col)

                # Alpha-Beta pruning
                if max_score >= beta:
                    return max_score, best_move

                if max_score > alpha:
                    alpha = max_score

            return max_score, best_move

        else:
            min_score = Infinity
            best_move = None
            empty_squares = board.get_empty()

            for (row, col) in empty_squares:
                copy_board = copy.deepcopy(board)
                copy_board.fill(row, col, self.player)
                score = self.minimax_ab_1(copy_board, True, alpha, beta)[0]  # Evaluates max for player moves

                if score < min_score:
                    min_score = score
                    best_move = (row, col)

                if min_score <= alpha:
                    return min_score, best_move

                if min_score < beta:
                    beta = min_score

            return min_score, best_move

    # Minimax algorithm with alpha-beta pruning if player starts second
    # Difference from other func is it evaluates for ai with maximizing and play with minimizing
    def minimax_ab_2(self, board, maximizing, alpha, beta):

        state = board.final_state()

        if state == 1:
            return 1, None

        if state == 2:
            return -1, None

        elif board.is_full():
            return 0, None

        if maximizing:
            max_score = -100
            best_move = None
            empty_squares = board.get_empty()

            for (row, col) in empty_squares:
                copy_board = copy.deepcopy(board)
                copy_board.fill(row, col, self.player)
                score = self.minimax_ab_2(copy_board, False, alpha, beta)[0]  # Evaluates min for player moves

                if score > max_score:
                    max_score = score
                    best_move = (row, col)

                if max_score >= beta:
                    return max_score, best_move

                if max_score > alpha:
                    alpha = max_score

            return max_score, best_move

        else:
            min_score = 100
            best_move = None
            empty_squares = board.get_empty()

            for (row, col) in empty_squares:
                copy_board = copy.deepcopy(board)
                copy_board.fill(row, col, 2)
                score = self.minimax_ab_2(copy_board, True, alpha, beta)[0]

                if score < min_score:
                    min_score = score
                    best_move = (row, col)

                if min_score <= alpha:
                    return min_score, best_move

                if min_score < beta:
                    beta = min_score

            return min_score, best_move

    def evaluate(self, main_board, max, start):
        if start == 1:
            score, move = self.minimax_ab_1(main_board, max, -100, 100)

        elif start == 2:
            score, move = self.minimax_ab_2(main_board, max, -100, 100)

        return move
