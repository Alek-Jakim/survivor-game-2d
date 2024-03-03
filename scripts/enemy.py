from settings import *
from utils import import_assets
from math import sin


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, pos, enemy_type, speed, status, health, score):
        super().__init__(group)

        import_assets(self, f"/assets/enemies/{enemy_type}")

        self.frame_idx = 0
        self.animation_speed = 7

        self.beginning_status = status

        self.score = score

        self.status = f"run_{status}" if enemy_type == "red" else f"walk_{status}"

        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(topleft=pos)
        self.enemy_type = enemy_type

        self.hitbox = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height)

        self.old_rect = self.rect.copy()

        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.dir.x = 1 if status == "right" else -1
        self.dir.y = 1
        self.speed = speed
        self.gravity = 0

        self.is_on_ground = False

        # Damage
        self.is_hit = False
        self.hit_time = 0
        self.health = health

    def wave_value(self):
        value = sin(pygame.time.get_ticks())

        if value >= 0:
            return True
        else:
            return False

    def blink(self):
        if self.is_hit:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0, 0, 0))
                self.image = white_surf

    def damage_timer(self):
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 1000:
                self.is_hit = False
                self.dir.x = 1 if self.beginning_status == "right" else -1

    def play_animation(self, status):
        self.status = status

    def take_damage(self):
        self.is_hit = True
        self.dir.x = 0
        self.health -= 1
        self.hit_time = pygame.time.get_ticks()

        if self.health == 0:
            self.score.update_score(self.enemy_type)
            self.kill()
        else:
            self.play_animation(f"hurt_{self.beginning_status}")

    def move(self, dt):
        self.pos.x += self.dir.x * dt * self.speed
        self.rect.x = round(self.pos.x)

        self.pos.y += self.dir.y * dt * self.gravity
        self.rect.y = round(self.pos.y)
        self.hitbox.center = (round(self.rect.centerx), round(self.rect.centery))

        self.collision()
        self.apply_gravity()

    def remove_off_screen(self):
        if self.pos.x <= -255 or self.pos.x >= WIN_WIDTH + 255:
            self.kill()

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_idx += self.animation_speed * dt

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

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, "green", self.hitbox)

    def update(self, dt):
        self.move(dt)
        self.damage_timer()
        self.animate(dt)
        self.blink()
        self.remove_off_screen()


class RedWerewolf(Enemy):
    def __init__(self, group, pos, speed, status, health, score):
        super().__init__(
            group,
            pos,
            enemy_type="red",
            speed=speed,
            status=status,
            health=health,
            score=score,
        )

        self.status = f"run_{status}"

        self.hitbox = pygame.Rect(
            0, 0, self.rect.width // 2 + 100, self.rect.height - 100
        )

    def move(self, dt):
        self.pos.x += self.dir.x * dt * self.speed
        self.rect.x = round(self.pos.x)

        self.pos.y += self.dir.y * dt * self.gravity
        self.rect.y = round(self.pos.y)
        self.hitbox.center = (round(self.rect.centerx), round(self.rect.centery) + 100)

        self.collision()
        self.apply_gravity()

    # def take_damage(self):
    #     self.is_hit = True
    #     self.dir.x = 0
    #     self.health -= 1
    #     self.hit_time = pygame.time.get_ticks()

    #     if self.health == 0:
    #         self.score.update_score(self.enemy_type)
    #         self.kill()
    #     else:
    #         self.play_animation(f"hurt_{self.beginning_status}")

    def damage_timer(self):
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 1500:
                self.is_hit = False
                self.dir.x = 1 if self.beginning_status == "right" else -1
                self.play_animation(f"run_{self.beginning_status}")


class WhiteWerewolf(Enemy):
    def __init__(self, group, pos, speed, status, health, score):
        super().__init__(
            group,
            pos,
            enemy_type="white",
            speed=speed,
            status=status,
            health=health,
            score=score,
        )

        self.status = f"walk_{status}"

        self.hitbox = pygame.Rect(0, 0, self.rect.width // 2, self.rect.height)

    # def take_damage(self):
    #     self.is_hit = True
    #     self.dir.x = 0
    #     self.health -= 1
    #     self.hit_time = pygame.time.get_ticks()

    #     if self.health == 0:
    #         self.score.update_score(self.enemy_type)
    #         self.kill()
    #     else:
    #         self.play_animation(f"hurt_{self.beginning_status}")

    def damage_timer(self):
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 1500:
                self.is_hit = False
                self.dir.x = 1 if self.beginning_status == "right" else -1
                self.play_animation(f"walk_{self.beginning_status}")
