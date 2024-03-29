import os
from pygame.locals import *
import pygame, sys
from pygame.math import Vector2

WIN_WIDTH, WIN_HEIGHT = 1280, 720

FPS = 60


root_path = os.path.dirname(__file__).replace("\\", "/")

font_path = root_path + "/assets/font/game_font.ttf"

tile_layers = ["sky", "buildings", "buildings_back", "ground"]


tile_group = pygame.sprite.Group()
flame_group = pygame.sprite.Group()
collision_tile_group = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()
