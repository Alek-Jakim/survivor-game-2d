from scripts.game_state_manager import Scene
from settings import *
import pygame
from scripts.button import Button
from utils import *


class Menu(Scene):
    def __init__(self, screen, game_state_manager, sound_manager):
        super().__init__(screen, game_state_manager)

        self.background_img = pygame.image.load(
            root_path + "/assets/background/menu_bg.png"
        ).convert()

        self.background_rect = self.background_img.get_rect(topleft=(0, 0))

        self.title_surf = pygame.Surface((500, 100))
        self.title_surf.fill("black")
        self.title_rect = self.title_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 200)
        )

        self.clicked = False

        self.sound_manager = sound_manager

        self.sound_manager.sounds["main_theme"].stop()

    def run(self):
        running = True

        if running:
            self.sound_manager.sounds["main_theme"].stop()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    close_game()

                if event.type == MOUSEBUTTONDOWN:
                    self.clicked = True

            self.screen.blit(self.background_img, self.background_rect)

            # Title
            self.screen.blit(self.title_surf, self.title_rect)

            draw_text(
                "Survivor 2D",
                get_font(font_path, 80),
                "red",
                self.screen,
                (self.screen.get_width() // 2, self.screen.get_height() // 2 - 200),
            )

            # Menu buttons
            select_btn = Button(
                [0, 0, 300, 100],
                "black",
                [WIN_WIDTH / 2, (WIN_HEIGHT / 2)],
                "Start Game",
                "white",
                get_font(font_path, 32),
            )
            select_btn.render(self.screen)

            controls_btn = Button(
                [0, 0, 300, 100],
                "black",
                [WIN_WIDTH / 2, (WIN_HEIGHT / 2) + 150],
                "Controls",
                "white",
                get_font(font_path, 32),
            )
            controls_btn.render(self.screen)

            mx, my = pygame.mouse.get_pos()

            if select_btn.btn_rect.collidepoint((mx, my)):
                if self.clicked:
                    self.game_state_manager.set_state("battle")
                    running = False

            if controls_btn.btn_rect.collidepoint((mx, my)):
                if self.clicked:
                    self.game_state_manager.set_state("controls")
                    running = False

            self.clicked = False

            pygame.display.update()
