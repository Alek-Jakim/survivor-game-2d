import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class CollisionTile(Tile):
    def __init__(self, groups, surf, pos):
        super().__init__(groups, surf, pos)

        self.old_rect = self.rect.copy()
