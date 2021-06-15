import pygame

import sound
import tetromino

TILE_SIZE  = 40

SCREEN_WIDTH = 20
SCREEN_HEIGHT = 22
SCREEN_COLOR = (100, 100, 100)

GAME_PLACEMENT = (1, 1)
GAME_WIDTH = 10
GAME_HEIGHT = 20

GRID_COLOR_BORDER = (50, 0, 170)
GRID_COLOR_FILL = (0, 0, 0)

game_start_x = GAME_PLACEMENT[0] * TILE_SIZE
game_start_y = GAME_PLACEMENT[1] * TILE_SIZE

# 0 value empty
# 1 value filled with tetronimo type(used for color)
grid = [[GRID_COLOR_FILL for i in range(GAME_WIDTH)] for j in range(GAME_HEIGHT)]

class World:
    screen = None
    def __init__(self, screen):
        self.screen = screen

    def check_for_filled_row(self):
        for y in range(0, GAME_HEIGHT):
            filled_row = True
            for x in range(0, GAME_WIDTH):
                if grid[y][x] == GRID_COLOR_FILL:
                    filled_row = False
            if filled_row:
                for y1 in range(y - 1, -1, -1):
                    for x1 in range(0, GAME_WIDTH):
                        grid[y1 + 1][x1] = grid[y1][x1]
                sound.play_sound("rotation")

    def render(self):
        for y in range(0, GAME_HEIGHT):
            for x in range(0, GAME_WIDTH):
                r = pygame.Rect((game_start_x + TILE_SIZE*x, game_start_y + TILE_SIZE*y), (TILE_SIZE, TILE_SIZE))
                color = grid[y][x]
                pygame.draw.rect(self.screen, color, r)
                if color != GRID_COLOR_FILL:
                    pygame.draw.rect(self.screen, tetromino.BORDER_COLOR, r, 2)
                else:
                    pygame.draw.rect(self.screen, GRID_COLOR_BORDER, r, 2)
