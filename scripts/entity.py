# from settings import *
# from utils import import_assets


# class Entity(pygame.sprite.Sprite):
#     def __init__(self, group, pos, collision_tiles, default_status, speed, asset_path):
#         super().__init__(group)

#         import_assets(self, asset_path)

#         self.frame_idx = 0
#         self.status = default_status

#         self.image = self.animations[self.status][self.frame_idx]
#         self.rect = self.image.get_rect(topleft=pos)
#         self.old_rect = self.rect.copy()

#         self.pos = Vector2(self.rect.topleft)
#         self.dir = Vector2()
#         self.speed = speed
#         self.gravity = 0

#         self.collision_tiles = collision_tiles
#         self.is_on_ground = False
#         self.facing_dir = "right"

#     def move(self, dt):

#         self.pos.x += self.dir.x * dt * self.speed
#         self.rect.x = round(self.pos.x)

#         self.pos.y += self.dir.y * dt * self.gravity
#         self.rect.y = round(self.pos.y)
#         self.collision()
#         self.apply_gravity()

#     def animate(self, dt):
#         current_animation = self.animations[self.status]

#         self.frame_idx += 7 * dt

#         if self.frame_idx >= len(current_animation):
#             self.frame_idx = 0

#         self.image = current_animation[int(self.frame_idx)]

#     def apply_gravity(self):
#         if not self.is_on_ground:
#             self.gravity += 30
#         else:
#             self.gravity = 0
#             self.dir.y = 0

#     def play_animation(self, status):
#         self.status = status

#     def collision(self):
#         for sprite in self.collision_tiles.sprites():
#             if sprite.rect.colliderect(self.rect):
#                 if (
#                     self.rect.bottom >= sprite.rect.top
#                     and self.old_rect.bottom <= sprite.old_rect.top
#                 ):
#                     self.rect.bottom = sprite.rect.top
#                     self.is_jumping = False
#                     self.is_on_ground = True

#                 self.pos.y = self.rect.y

#     def update(self, dt):
#         self.move(dt)
