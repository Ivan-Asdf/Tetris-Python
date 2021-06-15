# from enum import Enum
import random
import copy

import pygame
import world

# class TetrominoType(Enum):
#     I = 1,
#     T = 2,
#     J = 3,
#     L = 4,
#     Z = 5,
#     S = 6,
#     O = 7

spawns = [
    [(1, 1), (2, 1), (0, 1), (3, 1)],   # I
    [(1, 1), (0, 1), (1, 0), (2, 1)],   # T
    [(1, 1), (0, 1), (0, 0), (2, 1)],   # J
    [(1, 1), (0, 1), (2, 1), (2, 0)],   # L
    [(1, 1), (0, 1), (1, 0), (2, 0)],   # Z
    [(1, 1), (1, 0), (0, 0), (2, 1)],   # S
    [(1, 1), (2, 0), (1, 0), (2, 1)],   # O
]

colors = [
    (15, 65, 214),
    (196, 18, 199),
    (230, 44, 44),
    (212, 146, 15),
    (205, 212, 15),
    (15, 212, 38),
    (171, 173, 147)
]

REACHED_FLOOR = pygame.USEREVENT + 3

screen = None
# current tetromino set until new are generated
tetromino_set = []

def get_tetromino():
    t = tetromino_set.pop(0)
    if len(tetromino_set) == 0:
        gen_tetromino_set()

    return t

def gen_tetromino_set():
    type_list = list(range(0, 7))
    # random.shuffle(type_list)

    
    for type in type_list:
        t = Tetromino(type)
        t.move(3, -2)
        # tetromino_set.append(t)
        tetromino_set.insert(0,t)

def lock_tetromino(tetromino):
    for tile in tetromino.tiles:
        if tile[1] < 0:
            print("GAME OVER")
            exit(0)
        world.grid[tile[1]][tile[0]] = tetromino.color;
    return get_tetromino()

def getGhostTetromino(t):
    t = copy.deepcopy(t)
    t.is_ghost = True
    while not t.check_collision():
        t.move_no_coll(0, 1)
    
    t.move_no_coll(0, -1)

    return t

def hard_drop_tetronimo(t):
    t = getGhostTetromino(t)
    return lock_tetromino(t)

class Tetromino:
    def __init__(self, type):
        # print(spawns)
        self.color = colors[type]
        self.tiles = spawns[type].copy()
        self.is_ghost = False
        self.type = type
        self.rotation_state = 0

    def move_no_coll(self, x, y):
         for i in range(0, len(self.tiles)):
            self.tiles[i] = (self.tiles[i][0] + x, self.tiles[i][1] + y)

    def move(self, x, y):
        prev_tiles = self.tiles.copy()
        self.move_no_coll(x, y)
        
        if self.check_collision():
            self.tiles = prev_tiles
            # print("new", self.tiles)
            # raised reached floor event
            if (y >= 1):
                pygame.event.post(pygame.event.Event(REACHED_FLOOR))

    def render(self):
        for tile in self.tiles:
            r = pygame.Rect((world.game_start_x + 32*tile[0], world.game_start_y + 32*tile[1]), (32, 32))
            if (not self.is_ghost):
                pygame.draw.rect(screen, self.color, r)
            else:
                pygame.draw.rect(screen, self.color, r, 3)

    def check_collision(self):
        for tile in self.tiles:
            # Reach floor
            if tile[1] > world.GAME_HEIGHT - 1:
                return True
            # Reach side walls
            if tile[0] < 0 or world.GAME_WIDTH - 1 < tile[0]:
                return True

            # Reach locked tetrominos solid grid
            if (tile[0] >= 0 and tile[1] >= 0):
                if world.grid[tile[1]][tile[0]] != world.GRID_COLOR_FILL:
                    return True

        return False

    def rotate(self, rotation):
        # https:#tetris.fandom.com/wiki/SRS?file=SRS-pieces.png
        # Special shift for when rotation "I" tetromino
        if self.type == 0:
            shift_x = 0
            shift_y = 0
        
            # If vertical before rotation
            if self.tiles[0][0] == self.tiles[1][0]:
                # If centertile above geometric center
                if self.tiles[0][1] < self.tiles[1][1]:
                    shift_y = rotation
                else:
                    shift_y = -rotation
            # If horizontal before rotation
            else:
                # If center to the left of geometric center
                if self.tiles[0][0] < self.tiles[1][0]:
                    shift_x = rotation
                else:
                    shift_x = -rotation

            self.move_no_coll(shift_x, shift_y)

        center_tile_index = 0
        # Different centertile for rotation of "I" for to not go beyond the "bounding rectangle"
        if self.type == 0 and rotation == -1:
            center_tile_index = 1

        for i in range(len(self.tiles)):
            if i == center_tile_index:
                continue

            center_tile = self.tiles[center_tile_index]
            outer_tile = self.tiles[i]
            delta_x = (center_tile[0] - outer_tile[0]) * rotation
            delta_y = (center_tile[1] - outer_tile[1]) * rotation

            self.tiles[i] = (center_tile[0] + delta_y, center_tile[1] - delta_x)

        # Wallkicks https://tetris.fandom.com/wiki/SRS go to "Wall Kicks" secton
        rotate_from = self.rotation_state
        rotate_to = self.rotation_state + rotation
        # Like a clock logic
        if rotate_to > 3:
            rotate_to = 0
        elif rotate_to < 0:
            rotate_to = 3

        # The offsets to be tried to avoid collision
        offsets = get_wallkick_offsets(rotate_from, rotate_to, type)
        orig_tiles = self.tiles.copy()
        for offset in offsets:
            self.move_no_coll(offset[0], offset[1])
            if self.check_collision():
                self.tiles = orig_tiles
            else:
                # Succefully rotated with no collision
                self.rotation_state = rotate_to
                return
        
        print("ERROR: ROTATION FAILED")
        

def get_wallkick_offsets(rotate_from, rotate_to, type):
    # You can ignore this logic it basicly returns the proper sublist in "kickData" below where "from -> to"
    index_base = rotate_from * 2
    index_add = 0
    if rotate_to > rotate_from and not (rotate_from == 0 and rotate_to == 3):
        index_add = 1
    
    index = index_base + index_add
    if type == 0:
        return kickDataI[index]

    return kickData[index]

kickData = [
    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],      # 0 -> 3
    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],   # 0 -> 1
    [(0, 0), (1, 0), (1, 1), (0, -2), (1, -1)],     # 1 -> 0
    [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],     # 1 -> 2
    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],   # 2 -> 1
    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],      # 2 -> 3 
    [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],  # 3 -> 2
    [(0, 0), (-1, 0), (-1, -1), (0, -2), (-1, -2)]  # 3 -> 0
]

# Special kickdata from "I" tetromino
kickDataI =[
    [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],    # 0 -> 4
    [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],    # 0 -> 1
    [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],    # 1 -> 0
    [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, -1)],   # 1 -> 2
    [(0, 0), (1, 0), (2, 0), (1, 2), (-2, 1)],      # 2 -> 1
    [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],    # 2 -> 3 
    [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],    # 3 -> 2
    [(0, 0), (1, 0), (2, 0), (1, -2), (-2, 1)]      # 3 -> 0
]