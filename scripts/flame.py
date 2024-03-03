from settings import *
from utils import import_assets


class Flame(pygame.sprite.Sprite):
    def __init__(self, groups, pos, facing_dir):
        super().__init__(groups)

        import_assets(self, f"/assets/flame")

        self.frame_idx = 0
        self.status = f"attack_{facing_dir}"

        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(center=pos)

        self.pos = Vector2(self.rect.center)
        self.dir = Vector2()
        self.dir.x = -1 if facing_dir == "left" else 1
        self.speed = 500

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_idx += 5 * dt

        if self.frame_idx >= len(current_animation):
            self.frame_idx = 1

        self.image = current_animation[int(self.frame_idx)]

    def move(self, dt):
        self.pos.x += self.dir.x * dt * self.speed
        self.rect.x = round(self.pos.x)

    def offscreen_kill(self):
        if self.pos.x <= -100 or self.pos.x >= WIN_WIDTH + 100:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.offscreen_kill()
