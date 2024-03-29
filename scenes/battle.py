from settings import *
from scripts.game_state_manager import Scene
from utils import close_game, draw_text, get_font
from pytmx.util_pygame import load_pygame
from scripts.tile import Tile, CollisionTile
from scripts.player import Player
from scripts.enemy import RedWerewolf, WhiteWerewolf
from scripts.ui_element import Score
from random import randint


class Battle(Scene):
    def __init__(self, screen, game_state_manager, clock, sound_manager):
        super().__init__(screen, game_state_manager)

        self.clock = clock

        self.sound_manager = sound_manager

        self.init_player()

        self.enemy_timer = pygame.USEREVENT + 1

        pygame.time.set_timer(self.enemy_timer, randint(3000, 4500))

        # UI
        self.score = Score("/assets/UI", (WIN_WIDTH - 250, -25), (WIN_WIDTH - 450, -25))

        self.draw_map()

    def draw_map(self):

        tmx_map = load_pygame(root_path + "/assets/tilemap/map.tmx")

        for tile in tile_layers:
            for x, y, surf in tmx_map.get_layer_by_name(tile).tiles():
                Tile(tile_group, surf, (x * 32, y * 32))

        for x, y, surf in tmx_map.get_layer_by_name("ground_collide").tiles():
            CollisionTile(collision_tile_group, surf, (x * 32, y * 32))

        for x, y, surf in tmx_map.get_layer_by_name("ground").tiles():
            Tile(
                tile_group,
                surf,
                (x * 32, y * 32),
            )

    def game_over_screen(self):
        game_over_bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        game_over_bg.set_alpha(120)

        self.screen.blit(game_over_bg, (0, 0))

        total_score = self.score.calculate_total_score()

        draw_text(
            f"White werewolves killed: {self.score.white_score}\nRed werewolves killed: {self.score.red_score}\nTotal score is {total_score}",
            get_font(font_path, 60),
            "red",
            self.screen,
            (self.screen.get_width() // 2, self.screen.get_height() // 2 - 100),
        )

        draw_text(
            f'Click "Escape" to go back to the main menu',
            get_font(font_path, 50),
            "white",
            self.screen,
            (self.screen.get_width() // 2, self.screen.get_height() // 2 + 100),
        )

    def reset_battle(self):
        self.init_player()
        enemy_group.empty()
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, randint(3000, 4500))
        self.score.reset_score()

    def init_player(self):
        self.player = Player(
            player_group, (300, 300), collision_tile_group, self.sound_manager
        )

    def run(self):
        running = True

        if running:
            self.sound_manager.play_sound("main_theme", 0.5, -1)

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    close_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_state_manager.set_state("menu")
                        running = False
                        self.reset_battle()

                # Spawn Enemy
                if event.type == self.enemy_timer:
                    rand_pos = randint(0, 1)
                    rand_enemy = randint(0, 1)
                    enemy_pos = (WIN_WIDTH + 150 if rand_pos == 0 else -150, 200)

                    enemy_dir = "left" if rand_pos == 0 else "right"

                    if rand_enemy == 0:
                        RedWerewolf(
                            enemy_group, enemy_pos, 450, enemy_dir, 2, self.score
                        )
                        self.sound_manager.play_sound("red")
                    else:
                        WhiteWerewolf(
                            enemy_group, enemy_pos, 200, enemy_dir, 3, self.score
                        )
                        self.sound_manager.play_sound("white")

            dt = self.clock.tick(FPS) / 1000

            tile_group.update()
            flame_group.update(dt)
            player_group.update(dt)
            enemy_group.update(dt)

            self.screen.fill("black")

            tile_group.draw(self.screen)
            player_group.draw(self.screen)
            enemy_group.draw(self.screen)
            flame_group.draw(self.screen)

            player_group.sprite.health_bar(self.screen)

            self.score.draw(self.screen)

            if self.player.game_over:
                self.game_over_screen()

            pygame.display.update()
