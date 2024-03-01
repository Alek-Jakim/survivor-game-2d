from settings import *
from utils import *


class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_tiles):
        super().__init__(group)

        import_assets(self, "player")

        self.frame_idx = 0
        self.status = "idle_right"

        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(topleft=pos)

        self.old_rect = self.rect.copy()

        self.gravity = 0
        self.is_jumping = False
        self.is_on_ground = False

        # movement
        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.speed = 400
        self.gravity = 0
        self.dir.y = 1
        self.facing_dir = "right"

        self.collision_tiles = collision_tiles

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[K_a] and self.rect.left >= -85:
            self.dir.x = -1
            self.play_animation("run_left")
            self.facing_dir = "left"
        elif keys[K_d] and self.rect.right <= 1365:
            self.dir.x = 1
            self.play_animation("run_right")
            self.facing_dir = "right"
        else:
            self.dir.x = 0
            self.play_animation(f"idle_{self.facing_dir}")

        if pygame.key.get_just_pressed()[K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.is_on_ground = False
            self.gravity = -900

    def move(self, dt):

        self.pos.x += self.dir.x * dt * self.speed
        self.rect.x = round(self.pos.x)

        self.pos.y += self.dir.y * dt * self.gravity
        self.rect.y = round(self.pos.y)
        self.collision()
        self.apply_gravity()

    def play_animation(self, status):
        self.status = status

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
        for sprite in self.collision_tiles.sprites():
            if sprite.rect.colliderect(self.rect):
                if (
                    self.rect.bottom >= sprite.rect.top
                    and self.old_rect.bottom <= sprite.old_rect.top
                ):
                    self.rect.bottom = sprite.rect.top
                    self.is_jumping = False
                    self.is_on_ground = True

                self.pos.y = self.rect.y

    def update(self, dt):
        self.input()
        self.animate(dt)
        self.move(dt)
        print(self.rect.left)
