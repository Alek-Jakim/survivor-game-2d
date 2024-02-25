from scripts.game_state_manager import Scene
from settings import *
import pygame, sys


class Menu(Scene):
    def __init__(self, screen, game_state_manager, clock):
        super().__init__(screen, game_state_manager, clock)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    close_game()
                if event.type == KEYDOWN:
                    if event.key == K_l:
                        self.game_state_manager.set_state("character_select")
                        running = False

            self.screen.fill("purple")

            pygame.display.update()
