import os
from pygame.locals import *
import pygame, sys

WIN_WIDTH, WIN_HEIGHT = 1280, 720

FPS = 60


root_path = os.path.dirname(__file__).replace("\\", "/")

font_path = root_path + "/assets/font/game_font.ttf"
