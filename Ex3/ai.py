import pygame
import copy

class AI:

    def __init__(self, player=2):
        self.player = player

   
    def minimax_ab_1(self, board, maximizing, alpha, beta):  

        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax_ab_1(temp_board, False, alpha, beta)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

                if max_eval >= beta:
                    return max_eval, best_move

                if max_eval > alpha:
                    alpha = max_eval

            return max_eval, best_move

        else:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax_ab_1(temp_board, True, alpha, beta)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
               
                if min_eval <= alpha:
                    return min_eval, best_move

                if min_eval < beta:
                    beta = min_eval

            return min_eval, best_move     



             # Minimax algorithm wit alpha-beta pruning
    def minimax_ab_2(self, board, maximizing, alpha, beta):  

        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax_ab_2(temp_board, False, alpha, beta)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                if max_eval >= beta:
                    return max_eval, best_move
                if max_eval > alpha:
                    alpha = max_eval
            return max_eval, best_move

        else:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 2)
                eval = self.minimax_ab_2(temp_board, True, alpha, beta)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
               
                if min_eval <= alpha:
                    return min_eval, best_move

                if min_eval < beta:
                    beta = min_eval

            return min_eval, best_move       
  

    def evaluate(self, main_board, max, starts):
        if starts == 1:
            eval, move = self.minimax_ab_1(main_board, max, -100, 100)
        elif starts == 2:
            eval, move = self.minimax_ab_2(main_board, max, -100, 100)
        return move  
