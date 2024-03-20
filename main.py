import pygame
from pygame.locals import *
import sys
import numpy as np
import classes

BLACK = (30, 30, 30)
WHITE = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
SCREEN = None


def draw_grid(game_grid, game_over, turns):
    block_size = 50  # Set the size of the grid block

    if game_grid == []:
        game_grid = [[" " for j in range(16)] for i in range(12)]
    elif len(game_grid) != 12 or len(game_grid[0]) != 16:
        print("Wrong size for grid. Grid must have 12 rows and 16 columns.")
        sys.exit()

    for x in range(len(game_grid)):
        for y in range(len(game_grid[0])):
            rect = pygame.Rect(y * block_size, x * block_size, block_size, block_size)
            if game_grid[x][y] == "#":
                pygame.draw.rect(SCREEN, BLACK, rect, 0)
            elif game_grid[x][y] == "P":
                pygame.draw.circle(SCREEN, WHITE, (y * block_size + block_size // 2, x * block_size + block_size // 2),
                                   block_size // 2)
                if game_over == 2:
                    temp_y = y * block_size
                    temp_x = x * block_size
                    pygame.draw.line(SCREEN, RED, (temp_y + 15, temp_x + 10), (temp_y + 35, temp_x + 30), 3)
                    pygame.draw.line(SCREEN, RED, (temp_y + 35, temp_x + 10), (temp_y + 15, temp_x + 30), 3)
            elif game_grid[x][y] == "E":
                pygame.draw.rect(SCREEN, BLUE, rect, 15)
            elif game_grid[x][y] == "G":
                pygame.draw.circle(SCREEN, RED, (y * block_size + block_size // 2, x * block_size + block_size // 2),
                                   block_size // 2)

            pygame.draw.rect(SCREEN, WHITE, rect, 1)

    turns_text = font.render('Turn: ' + str(turns), True, WHITE, BLACK)
    SCREEN.blit(turns_text, (5, 5))

    if game_over == 1:
        end_text = font.render('You escaped!!', True, WHITE, BLACK)
        SCREEN.blit(end_text, (310, 250))
    elif game_over == 2:
        end_text = font.render('You lost.', True, WHITE, BLACK)
        SCREEN.blit(end_text, (350, 250))


# create the current map object
current_map = classes.game_map("map.txt", "guards.txt")

# Initialize pygame
pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
SCREEN.fill(BLACK)
pygame.display.set_caption("Prison Escape - CPSC 231 Fall 2022 University of Calgary")
font_color = (0, 150, 250)
font = pygame.font.SysFont("Segoe UI", 30)

print("\nUse WASD or the arrow keys to move. Press Esc to quit the game.\n")
done = False
game_over = 0
turns = 1

while not done:
    SCREEN.fill((255, 255, 255))
    draw_grid(current_map.get_grid(), game_over, turns)

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        # when a key is pressed and the game is not over
        elif event.type == KEYDOWN and not game_over:
            # now is the player's turn
            turn = True
            if event.key == K_RIGHT or event.key == K_d:
                current_map.update_player("R")
                turn = False
                turns += 1
            elif event.key == K_LEFT or event.key == K_a:
                current_map.update_player("L")
                turn = False
                turns += 1
            elif event.key == K_UP or event.key == K_w:
                current_map.update_player("U")
                turn = False
                turns += 1
            elif event.key == K_DOWN or event.key == K_s:
                current_map.update_player("D")
                turn = False
                turns += 1

            if current_map.player_wins():
                game_over = 1
            if turn == False:
            # now is the guards' turn
                if current_map.player_loses():
                    game_over = 2
                else:
                    current_map.update_guards()
                    if current_map.player_loses():
                        game_over = 2


    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        done = True

    pygame.display.update()

pygame.display.quit()
pygame.quit()
sys.exit()
