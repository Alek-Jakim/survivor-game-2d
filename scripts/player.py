from settings import *
from utils import *
from scripts.flame import Flame
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_tiles, sound_manager):
        super().__init__(group)

        import_assets(self, "/assets/player")

        self.frame_idx = 0
        self.animation_speed = 10
        self.status = "idle_right"

        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(
            0, 0, self.rect.width // 2 - 75, self.rect.height - 75
        )

        self.old_rect = self.rect.copy()

        # Jumping
        self.gravity = 0
        self.is_jumping = False
        self.is_on_ground = False

        # Attacking
        self.attack_time = 0
        self.is_attacking = False
        self.can_attack = True

        # Get damage
        self.is_hit = False
        self.hit_time = 0
        self.sound_manager = sound_manager
        self.health = 3
        self.health_icon = pygame.transform.scale_by(
            pygame.image.load(root_path + "/assets/heart.png").convert_alpha(), 1.5
        )
        self.health_rect = self.health_icon.get_rect(center=(75, 60))
        self.is_dead = False
        self.stop_animation = False

        # movement
        self.pos = Vector2(self.rect.topleft)
        self.dir = Vector2()
        self.speed = 400
        self.gravity = 0
        self.dir.y = 1
        self.facing_dir = "right"

        self.collision_tiles = collision_tiles

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

    def movement_input(self, key):
        if not self.is_dead:
            if key[K_a] and self.rect.left >= -85:
                self.dir.x = -1
                self.play_animation("run_left")
                self.facing_dir = "left"
            elif key[K_d] and self.rect.right <= 1365:
                self.dir.x = 1
                self.play_animation("run_right")
                self.facing_dir = "right"
            else:
                self.dir.x = 0
                self.play_animation(f"idle_{self.facing_dir}")

    def health_bar(self, surf):
        surf.blit(self.health_icon, self.health_rect)
        draw_text(
            f"{self.health}/3",
            get_font(font_path, 60),
            "white",
            surf,
            (150, 60),
        )

    def jump_input(self, key):
        if key[K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.is_on_ground = False
            self.gravity = -900

    def attack_input(self, key):
        if key[K_p] and not self.is_jumping:
            self.frame_idx = 0
            self.can_attack = False
            self.play_animation(f"attack_{self.facing_dir}")
            self.is_attacking = True
            self.dir.x = 0
            self.attack_time = pygame.time.get_ticks()

    def flame_attack(self):

        if (
            len(self.animations[self.status]) - 3 == int(self.frame_idx)
            and self.is_attacking
            and len(flame_group) < 1
        ):
            right_flame_pos = self.rect.centerx, self.rect.centery + 50
            left_flame_pos = self.rect.centerx - 100, self.rect.centery + 50
            self.sound_manager.stop_sound("flame_attack")
            self.sound_manager.play_sound("flame_attack", 0.5, 0)

            Flame(
                flame_group,
                right_flame_pos if self.facing_dir == "right" else left_flame_pos,
                self.facing_dir,
            )
            self.is_attacking = False

    def input(self):
        key = pygame.key.get_pressed()
        key_pressed = pygame.key.get_just_pressed()

        if not self.is_attacking:
            # Move
            self.movement_input(key)

            # Jump
            self.jump_input(key_pressed)

            # Attack
            self.attack_input(key_pressed)

    def move(self, dt):

        self.pos.x += self.dir.x * dt * self.speed
        self.rect.x = round(self.pos.x)

        self.pos.y += self.dir.y * dt * self.gravity
        self.rect.y = round(self.pos.y)
        self.hitbox.center = (round(self.rect.centerx), round(self.rect.centery) + 75)

        self.tile_collision()
        self.apply_gravity()

    def play_animation(self, status):
        self.status = status

    def flame_timer(self):
        if self.is_attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time > 1500:
                self.can_attack = True

    def damage_timer(self):
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 1000:
                self.is_hit = False

    def animate(self, dt):
        current_animation = self.animations[self.status]

        if not self.stop_animation:
            self.frame_idx += self.animation_speed * dt

        if self.status.split("_")[0] == "attack" and not self.is_dead:
            if self.frame_idx >= len(current_animation):
                self.frame_idx = 0
                self.is_attacking = False
                self.play_animation(f"idle_{self.facing_dir}")

        if self.frame_idx >= len(current_animation):
            self.frame_idx = 0

        self.image = current_animation[int(self.frame_idx)]

    def apply_gravity(self):
        if not self.is_on_ground:
            self.gravity += 30
        else:
            self.gravity = 0

    def tile_collision(self):
        for sprite in collision_tile_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if (
                    self.rect.bottom >= sprite.rect.top
                    and self.old_rect.bottom <= sprite.old_rect.top
                ):
                    self.rect.bottom = sprite.rect.top
                    self.is_jumping = False
                    self.is_on_ground = True

                self.pos.y = self.rect.y

    def enemy_collision(self):
        for enemy in enemy_group.sprites():
            if (
                self.hitbox.colliderect(enemy.hitbox)
                and not self.is_hit
                and not self.is_dead
                and not enemy.is_dead
            ):
                self.is_hit = True
                self.hit_time = pygame.time.get_ticks()
                self.health -= 1

                if self.health == 0:
                    self.frame_idx = 0
                    self.is_dead = True
                    self.sound_manager.play_sound("dead")
                    self.animation_speed = 3
                    self.play_animation(f"dead_{self.facing_dir}")

                    self.dir.x = 0
                else:
                    self.sound_manager.play_sound("hurt")

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, "red", self.hitbox)

    def update(self, dt):
        self.input()
        self.flame_timer()
        self.damage_timer()
        self.flame_attack()

        self.animate(dt)

        self.blink()
        self.move(dt)
        self.enemy_collision()

        if self.is_dead:
            if int(self.frame_idx) == len(self.animations[self.status]) - 1:
                self.frame_idx = len(self.animations[self.status]) - 1
