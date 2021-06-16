import sys

import pygame
from pygame.time import get_ticks
pygame.init()

import tetromino
import world
import gui
import sound

sound.play_music()

screen = pygame.display.set_mode([world.SCREEN_WIDTH * world.TILE_SIZE, world.SCREEN_HEIGHT * world.TILE_SIZE])

tetromino.screen = screen
tetromino.gen_tetromino_set()
t = tetromino.get_tetromino()

w = world.World(screen)

down_pressed = False
left_ressed = False
right_pressed = False
debug_mode = False

NORMAL_DOWN_SPEED = 800
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
            t = tetromino.lock_tetromino(t)
            w.check_for_filled_row()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = True
                t.move(1, 0)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_ressed = True
                t.move(-1, 0)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = True
                if debug_mode:
                    t.move(0, 1)
            elif event.key == pygame.K_z or event.key == pygame.K_LSHIFT:
                t.rotate(-1)
            elif event.key == pygame.K_x or event.key == pygame.K_LCTRL:
                t.rotate(1)
            elif event.key == pygame.K_SPACE:
                t = tetromino.hard_drop_tetronimo(t)
                w.check_for_filled_row()
                sound.play_sound("hard_drop")
            # Debug only stuff
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                if debug_mode:
                    t.move(0, -1)
            elif event.key == pygame.K_F5:
                debug_mode = not debug_mode
                sound.play_sound("pause")
                if debug_mode:
                    sound.stop_music()
                else:
                    sound.play_music()

            if (left_ressed or right_pressed):
                das_delay_ticks = pygame.time.get_ticks()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = False
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_ressed = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = False
            elif event.key == pygame.K_SPACE:
                pass # GO straihg down

            if (not left_ressed and not right_pressed):
                das_delay_ticks = sys.maxsize

    # Vertical movement
    if not debug_mode:
        curr_ticks = pygame.time.get_ticks()
        if (down_pressed and curr_ticks - y_move_ticks >= FAST_DOWN_SPEED)\
            or (curr_ticks - y_move_ticks >= NORMAL_DOWN_SPEED):
                t.move(0, 1)
                y_move_ticks = curr_ticks

    # Horizontal movement
    if not debug_mode:
        if left_ressed != right_pressed:
            if left_ressed:
                x_move = -1
            elif right_pressed:
                x_move = 1
        else:
            x_move = 0

        if curr_ticks - das_delay_ticks >= DAS_DELAY:
            if curr_ticks - x_move_ticks >= HORIZONTAL_SPEED:
                t.move(x_move, 0)
                x_move_ticks = curr_ticks

    # Rendering
    screen.fill(world.SCREEN_COLOR)
    w.render()
    t.render()
    ghost = tetromino.get_ghost_tetromino(t)
    ghost.render()
    gui.show_next_tetromino(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()