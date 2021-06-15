from enum import Enum
import enum

import pygame

# Sound = Enum(
#     MOVEMENT = 1,
#     ROTATION = 2,
#     LINE_CLEAR = 3,
#     HARD_DROP = 4,
#     GAME_OVER = 5
# )

pygame.mixer.music.set_volume(0.03)

sounds = {
    "movement" : pygame.mixer.Sound("sfx/movement.wav"),
    "rotation" : pygame.mixer.Sound("sfx/rotation.wav"),
    "line_clear" : pygame.mixer.Sound("sfx/line_clear.wav"),
    "hard_drop" : pygame.mixer.Sound("sfx/hard_drop.wav"),
    "game_over" : pygame.mixer.Sound("sfx/game_over.wav"),
    "pause" : pygame.mixer.Sound("sfx/pause.wav"),
}

def play_music():
    pygame.mixer.music.load("sfx/tetris.wav")
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def play_sound(sound):
    play_sound = sounds[sound]
    play_sound.set_volume(0.5)
    pygame.mixer.Sound.play(play_sound)

