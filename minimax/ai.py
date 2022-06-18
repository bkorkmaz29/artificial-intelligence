import copy
from numpy import Infinity


class AI:

    def __init__(self, player=2):
        self.player = player

    # Minimax algorithm with alpha-beta pruning if player starts first
    def minimax_ab_1(self, board, maximizing, alpha, beta, depth):

        # End of game state 
        state = board.final_state()

        # Depth used to find the wining move in min moves

        # Player 1 wins
        if state == 1:
            return 10 - depth, None 
                                    
        # Player 2 wins
        if state == 2:
            return depth - 10, None

        # Draw
        elif board.is_full():
            return 0, None

        if maximizing:
            max_score = -Infinity
            best_move = None
            empty_squares = board.get_empty()  # Get available squares to make a move

<<<<<<< HEAD
            for (row, col) in empty_squares: # Iterate through all available moves
                # Copy board to make it mutable
                copy_board = copy.deepcopy(board)
=======
            for (row, col) in empty_squares:
                copy_board = copy.deepcopy(board)  # Copy board to make it mutable
>>>>>>> cf7fbd3d2daec6481b8b300828c1c32ab3196995
                copy_board.fill(row, col, 1)
                score = self.minimax_ab_1(copy_board, False, alpha, beta, depth + 1)[0]  # Evaluate min for ai move

                # If the evaluation is better than previous best, it becomes new best
                if score > max_score:
                    max_score = score
                    best_move = (row, col)

                # Alpha-Beta pruning
                # If max score is not smaller than beta, doesn't check other options
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
                score = self.minimax_ab_1(copy_board, True, alpha, beta, depth + 1)[0]  # Evaluates max for player moves

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
    def minimax_ab_2(self, board, maximizing, alpha, beta, depth):

        state = board.final_state()

        if state == 1:
            return 10 - depth, None

        if state == 2:
            return depth - 10, None

        elif board.is_full():
            return 0, None

        if maximizing:
            max_score = -Infinity
            best_move = None
            empty_squares = board.get_empty()

            for (row, col) in empty_squares:
                copy_board = copy.deepcopy(board)
                copy_board.fill(row, col, self.player)
                score = self.minimax_ab_2(copy_board, False, alpha, beta, depth + 1)[0]  # Evaluates min for player moves

                if score > max_score:
                    max_score = score 
                    best_move = (row, col)
                
                if max_score >= beta:
                    return max_score, best_move

                if max_score > alpha:
                    alpha = max_score
                
            return max_score, best_move

        else:
            min_score = Infinity
            best_move = None
            empty_squares = board.get_empty()

            for (row, col) in reversed(empty_squares):
                copy_board = copy.deepcopy(board)
                copy_board.fill(row, col, 2)
                score = self.minimax_ab_2(copy_board, True, alpha, beta, depth + 1)[0] 
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
            move = self.minimax_ab_1(main_board, max, -Infinity, Infinity, 0)[1]

        elif start == 2:
            move = self.minimax_ab_2(main_board, max, -Infinity, Infinity, 0)[1]

        return move
