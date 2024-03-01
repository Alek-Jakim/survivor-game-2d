from settings import pygame, sys, os, root_path


def close_game():
    pygame.quit()
    sys.exit()


def get_font(font_path, font_size):
    return pygame.font.Font(font_path, font_size)


def draw_text(text, font, color, surface, pos=(0, 0)):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=pos)
    surface.blit(textobj, textrect)


def import_assets(self, path):
    self.animations = {}

    for index, folder in enumerate(os.walk(root_path + path)):
        if index == 0:
            for name in folder[1]:
                if name not in self.animations:
                    left_direction = name + "_left"
                    right_direction = name + "_right"

                    self.animations[right_direction] = []
                    self.animations[left_direction] = []

        else:
            for file_name in sorted(folder[2], key=lambda string: string.split(".")[0]):
                path = folder[0].replace("\\", "/") + "/" + file_name
                surf = pygame.image.load(path).convert_alpha()
                surf = pygame.transform.scale_by(surf, 2).convert_alpha()
                surf_left = pygame.transform.flip(surf, True, False)
                key_left = folder[0].split("\\")[1] + "_left"
                key_right = folder[0].split("\\")[1] + "_right"

                self.animations[key_right].append(surf)
                self.animations[key_left].append(surf_left)
