from settings import *
from utils import import_assets


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, pos, enemy_type, speed, status):
        super().__init__(group)

        import_assets(self, f"/assets/enemies/{enemy_type}")

        self.frame_idx = 0

        self.status = f"run_{status}" if enemy_type == "red" else f"walk_{status}"

        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(topleft=pos)

        self.old_rect = self.rect.copy()

        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.dir.x = 1 if status == "right" else -1
        self.dir.y = 1
        self.speed = speed
        self.gravity = 0

        self.is_on_ground = False

    def move(self, dt):
        self.pos.x += self.dir.x * dt * self.speed
        self.rect.x = round(self.pos.x)

        self.pos.y += self.dir.y * dt * self.gravity
        self.rect.y = round(self.pos.y)
        self.collision()
        self.apply_gravity()

    def remove_off_screen(self):
        if self.pos.x <= -255 or self.pos.x >= WIN_WIDTH + 255:
            self.kill()

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_idx += 7 * dt

        if self.frame_idx >= len(current_animation):
            self.frame_idx = 0

        self.image = current_animation[int(self.frame_idx)]

    def apply_gravity(self):
        if not self.is_on_ground:
            self.gravity += 30
        else:
            self.gravity = 0

    def collision(self):
        for sprite in collision_tile_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if (
                    self.rect.bottom >= sprite.rect.top
                    and self.old_rect.bottom <= sprite.old_rect.top
                ):
                    self.rect.bottom = sprite.rect.top
                    self.is_on_ground = True

                self.pos.y = self.rect.y

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.remove_off_screen()
