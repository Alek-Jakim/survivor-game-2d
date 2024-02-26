from settings import *
from utils import *


class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)

        import_assets(self, "player")

        self.frame_idx = 0
        self.status = "idle_right"

        self.image = self.animations[self.status][self.frame_idx]

        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect(center=pos)

        # movement
        self.pos = Vector2(self.rect.center)
        self.dir = Vector2()
        self.speed = 400
        self.facing_dir = "right"

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[K_a]:
            self.dir.x = -1
            self.play_animation("run_left")
            self.facing_dir = "left"
        elif keys[K_d]:
            self.dir.x = 1
            self.play_animation("run_right")
            self.facing_dir = "right"
        else:
            self.dir.x = 0
            self.play_animation(f"idle_{self.facing_dir}")

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_idx += 7 * dt

        if self.frame_idx >= len(current_animation):
            self.frame_idx = 0

        self.image = current_animation[int(self.frame_idx)]

    def play_animation(self, status):
        self.status = status

    def move(self, dt):
        self.pos.x += self.dir.x * dt * self.speed
        self.rect.x = round(self.pos.x)

        self.pos.y += self.dir.y * dt * self.speed
        self.rect.y = round(self.pos.y)

    def update(self, dt):
        self.input()
        self.animate(dt)
        self.move(dt)
