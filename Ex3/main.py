import sys
import pygame
from game import Game
from constants import *

if __name__ == '__main__':

    # --- OBJECTS ---

    game = Game()
    board = game.board
    ai = game.ai
    max = False
    starts = 1

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
                    starts = 2
                    max = True
                    game.change_gamemode()
                    
                # r-restart game
                if event.key == pygame.K_r:
                    game.reset()
                    max = False
                    starts = 1
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
            row, col = ai.evaluate(board, max, starts)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()