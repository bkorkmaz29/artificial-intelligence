import pygame
import numpy as np
from ai import AI
from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC-TAC-TOE')
screen.fill(BG_COLOR)


class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS)) # Logical board
        self.empty_squares = self.squares 
        self.filled_squares = 0

    # Checks if board is in its final state and drawing lines over triples
    def final_state(self, draw=False):

        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if draw:
                    pos_x = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    pos_y = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    pygame.draw.line(screen, color, pos_x, pos_y, LINE_WIDTH)
                return self.squares[0][col]

        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if draw:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    pos_x = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pos_y = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, pos_x, pos_y, LINE_WIDTH)
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if draw:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                pos_x = (20, 20)
                pos_y = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, pos_x, pos_y, CROSS_WIDTH)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if draw:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                pos_x = (20, HEIGHT - 20)
                pos_y = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, pos_x, pos_y, CROSS_WIDTH)
            return self.squares[1][1]

        return 0

    # Checks if all squares are filled
    def is_full(self):
        return self.filled_squares == 9

    # Checks if all squares are empty
    def is_empty(self):
        return self.filled_squares == 0

    # Fills a square on logical board when a player makes move
    def fill(self, row, col, player):
        self.squares[row][col] = player
        self.filled_squares += 1

    # Returns empty square
    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    # Returns all empty squares
    def get_empty(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'player starts'
        self.running = True
        self.draw_board()

    # Draws the visual board
    def draw_board(self):
        screen.fill(BG_COLOR)

        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0),
                         (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0),
                         (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE),
                         (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE),
                         (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT),
                         (WIDTH, HEIGHT), LINE_WIDTH)

    # Draws the circle or X
    def draw_figure(self, row, col):
        if self.player == 1:
            diag_down_start = (col * SQUARE_SIZE + OFFSET,
                               row * SQUARE_SIZE + OFFSET)
            diag_down_end = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET,
                             row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, diag_down_start,
                             diag_down_end, CROSS_WIDTH)
            diag_up_start = (col * SQUARE_SIZE + OFFSET, row *
                             SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            diag_up_end = (col * SQUARE_SIZE + SQUARE_SIZE -
                           OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, diag_up_start,
                             diag_up_end, CROSS_WIDTH)

        elif self.player == 2:
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                      row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center,
                               RADIUS, CIRCLE_WIDTH)

    # Makes a move in visual and logical board
    def make_move(self, row, col):
        self.board.fill(row, col, self.player)
        self.draw_figure(row, col)
        self.next_turn()

    # Switches player turn
    def next_turn(self):
        self.player = self.player % 2 + 1

    # Switches the player starting first
    def change_starter(self):
        self.ai.player = self.player

    # Checks if the game is finished
    def is_finished(self):
        return self.board.final_state(draw=True) != 0 or self.board.is_full()

    def reset(self):
        self.__init__()
