from settings import pygame, sys


def close_game():
    pygame.quit()
    sys.exit()


def get_font(font_path, font_size):
    return pygame.font.Font(font_path, font_size)


def draw_text(text, font, color, surface, pos=(0, 0)):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=pos)
    surface.blit(textobj, textrect)
