import pygame

import tetromino
import world

GUI_PLACEMENT = (world.GAME_WIDTH + 2, world.GAME_PLACEMENT[1])
gui_start_x = GUI_PLACEMENT[0] * world.TILE_SIZE
gui_start_y = GUI_PLACEMENT[1] * world.TILE_SIZE

def show_next_tetromino(screen):
    if len(tetromino.tetromino_set) > 0:
        type = tetromino.tetromino_set[0].type

        # Render a grid
        for y in range(0, 4):
            for x in range(0, 4):
                r = pygame.Rect((gui_start_x + world.TILE_SIZE*x, gui_start_y + world.TILE_SIZE*y)\
                ,(world.TILE_SIZE, world.TILE_SIZE))

                pygame.draw.rect(screen, world.GRID_COLOR_FILL, r)
                pygame.draw.rect(screen, world.GRID_COLOR_BORDER, r, 2)

        # Render tetromino
        tiles = tetromino.spawns[type]
        for tile in tiles:
            r = pygame.Rect((gui_start_x + world.TILE_SIZE*tile[0], gui_start_y + world.TILE_SIZE*tile[1])\
                ,(world.TILE_SIZE, world.TILE_SIZE))

            pygame.draw.rect(screen, tetromino.colors[type], r)
            pygame.draw.rect(screen, tetromino.BORDER_COLOR, r, 2)
