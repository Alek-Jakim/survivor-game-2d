from settings import *
from utils import draw_text, get_font


class Score:
    def __init__(self, image_path, red_pos, white_pos):

        self.red = pygame.image.load(
            root_path + f"{image_path}/red.png"
        ).convert_alpha()
        self.red_rect = self.red.get_rect(topleft=red_pos)

        self.white = pygame.image.load(
            root_path + f"{image_path}/white.png"
        ).convert_alpha()

        self.white_rect = self.white.get_rect(topleft=white_pos)

        self.red_score = 0
        self.white_score = 0

    def draw(self, surf):
        surf.blit(self.red, self.red_rect)
        draw_text(
            f"X {self.white_score}",
            get_font(font_path, 60),
            "white",
            surf,
            (self.white_rect.centerx + 100, self.white_rect.centery + 25),
        )

        draw_text(
            f"X {self.red_score}",
            get_font(font_path, 60),
            "white",
            surf,
            (self.red_rect.centerx + 100, self.red_rect.centery + 25),
        )

        surf.blit(self.white, self.white_rect)

    def update_score(self, type):
        if type == "red":
            self.red_score += 1
        else:
            self.white_score += 1

    def calculate_total_score(self):
        return int(self.white_score * 5 + self.red_score * 10)

    def reset_score(self):
        self.red_score = 0
        self.white_score = 0
