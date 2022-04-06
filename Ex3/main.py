import sys
import pygame
from game import Game
from constants import *

'''
 Tic-Tac-Toe game with minimax (alpha-beta pruning) AI

 Press s for play second
 Press r for restart the game
'''

if __name__ == '__main__':

    # Initial params

    game = Game()
    board = game.board
    ai = game.ai
    max = False
    player_start = 1

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # s-change who starts
                if event.key == pygame.K_s:
                    player_start = 2
                    max = True
                    game.change_starter()

                # r-restart game
                if event.key == pygame.K_r:
                    game.reset()
                    max = False
                    player_start = 1
                    board = game.board
                    ai = game.ai

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.is_finished():
                        game.running = False

        if game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.evaluate(board, max, player_start)
            game.make_move(row, col)

            if game.is_finished():
                game.running = False

        pygame.display.update()
