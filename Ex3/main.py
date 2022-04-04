import copy
import sys
import pygame
import numpy as np

# Board Parameters

WIDTH = 600
HEIGHT = 600
ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS
LINE_WIDTH = 15
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
RADIUS = SQSIZE // 4
OFFSET = 50

# Colors

BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRC_COLOR = (255, 0, 0)
CROSS_COLOR = (0, 0, 255)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)


class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares  
        self.marked_sqrs = 0

    def final_state(self, show=False):
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class AI:

    def __init__(self, player=2):
        self.player = player

    # Minimax algorithm wit alpha-beta pruning
    def minimax_ab(self, board, maximizing, alpha, beta):  

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
                eval = self.minimax_ab(temp_board, False, alpha, beta)[0]

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
                eval = self.minimax_ab(temp_board, True, alpha, beta)[0]

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
               
                if min_eval <= alpha:
                    return min_eval, best_move

                if min_eval < beta:
                    beta = min_eval

            return min_eval, best_move       


    def evaluate(self, main_board, max):
        eval, move = self.minimax_ab(main_board, max, -100, 100)
        return move  


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 
        self.gamemode = 'player starts' 
        self.running = True
        self.show_lines()

    def show_lines(self):
        screen.fill(BG_COLOR)

        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0),
                         (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0),
                         (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE),
                         (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE),
                         (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET,
                        row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc,
                             end_desc, CROSS_WIDTH)
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc,
                             end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center,
                               RADIUS, CIRCLE_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.ai.player = game.player

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()


if __name__ == '__main__':

    # --- OBJECTS ---

    game = Game()
    board = game.board
    ai = game.ai
    max = False

    # --- MAINLOOP ---

    while True:

        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # s-change who starts
                if event.key == pygame.K_s:
                    game.change_gamemode()

                # r-restart game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        if game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.evaluate(board, max)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()
