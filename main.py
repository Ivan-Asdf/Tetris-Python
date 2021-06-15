import sys

import pygame
from pygame.time import get_ticks

import tetromino
import world
import gui

pygame.init()

screen = pygame.display.set_mode([world.SCREEN_WIDTH * world.TILE_SIZE, world.SCREEN_HEIGHT * world.TILE_SIZE])

tetromino.screen = screen
tetromino.gen_tetromino_set()
t = tetromino.get_tetromino();
t.move(0, 1)

w = world.World(screen)

upPressed = False
downPressed = False
leftPressed = False
rightPressed = False

NORMAL_DOWN_SPEED = 1000
FAST_DOWN_SPEED = 50
HORIZONTAL_SPEED = 70
DAS_DELAY = 250
x_move_ticks = pygame.time.get_ticks()
y_move_ticks = pygame.time.get_ticks()
das_delay_ticks = sys.maxsize

x_move = 0

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == tetromino.REACHED_FLOOR:
            print("reached floor")
            t = tetromino.lock_tetromino(t)
            w.check_for_filled_row()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                rightPressed = True
                t.move(1, 0)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                leftPressed = True
                t.move(-1, 0)
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                upPressed = True
                t.move(0, -1)
            elif event.key == pygame.K_z or event.key == pygame.K_LSHIFT:
                t.rotate(-1)
            elif event.key == pygame.K_x or event.key == pygame.K_LCTRL:
                t.rotate(1)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                downPressed = True
            elif event.key == pygame.K_SPACE:
                t = tetromino.hard_drop_tetronimo(t)
                w.check_for_filled_row()

            if (leftPressed or rightPressed):
                das_delay_ticks = pygame.time.get_ticks()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                rightPressed = False
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                leftPressed = False
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                upPressed = False 
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                downPressed = False
            elif event.key == pygame.K_SPACE:
                pass # GO straihg down

            if (not leftPressed and not rightPressed):
                das_delay_ticks = sys.maxsize

    # Vertical movement
    curr_ticks = pygame.time.get_ticks()
    if (downPressed and curr_ticks - y_move_ticks >= FAST_DOWN_SPEED)\
        or (curr_ticks - y_move_ticks >= NORMAL_DOWN_SPEED):
            t.move(0, 1)
            y_move_ticks = curr_ticks

    # Horizontal movement
    if leftPressed != rightPressed:
        if leftPressed:
            x_move = -1
        elif rightPressed:
            x_move = 1
    else:
        x_move = 0

    if curr_ticks - das_delay_ticks >= DAS_DELAY:
        if curr_ticks - x_move_ticks >= HORIZONTAL_SPEED:
            t.move(x_move, 0)
            x_move_ticks = curr_ticks

    # Rendering
    screen.fill(world.SCREEN_COLOR)
    ghost = tetromino.getGhostTetromino(t)
    w.render()
    t.render()
    ghost.render()
    gui.show_next_tetromino(screen)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()