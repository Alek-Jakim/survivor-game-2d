from settings import *
from scripts.game_state_manager import Scene
from utils import close_game
from pytmx.util_pygame import load_pygame
from scripts.tile import Tile, CollisionTile
from scripts.player import Player
from scripts.enemy import Enemy
from random import randint


class Battle(Scene):
    def __init__(self, screen, game_state_manager, clock, sound_manager):
        super().__init__(screen, game_state_manager)

        self.clock = clock

        self.sound_manager = sound_manager

        self.init_player()

        self.enemy_timer = pygame.USEREVENT + 1

        pygame.time.set_timer(self.enemy_timer, randint(3000, 6000))

        self.draw_map()

    def draw_map(self):

        tmx_map = load_pygame(root_path + "/assets/tilemap/map.tmx")

        for tile in tile_layers:
            for x, y, surf in tmx_map.get_layer_by_name(tile).tiles():
                Tile(tile_group, surf, (x * 32, y * 32))

        for x, y, surf in tmx_map.get_layer_by_name("ground_collide").tiles():
            CollisionTile(
                collision_tile_group,
                surf,
                (x * 32, y * 32),
            )

        for x, y, surf in tmx_map.get_layer_by_name("ground").tiles():
            Tile(
                tile_group,
                surf,
                (x * 32, y * 32),
            )

    def init_player(self):
        self.player = Player(player_group, (300, 300), collision_tile_group)

    def run(self):
        running = True

        if running:
            self.sound_manager.sounds["main_theme"].play(loops=-1)

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    close_game()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_state_manager.set_state("menu")
                        running = False

                # Spawn Enemy
                if event.type == self.enemy_timer:
                    rand_pos = randint(0, 1)
                    rand_enemy = randint(0, 1)

                    Enemy(
                        enemy_group,
                        (WIN_WIDTH + 200 if rand_pos == 0 else -200, 300),
                        "red" if rand_enemy == 0 else "white",
                        600 if rand_enemy == 0 else 200,
                        "left" if rand_pos == 0 else "right",
                    )

            dt = self.clock.tick(FPS) / 1000

            tile_group.update()
            player_group.update(dt)
            enemy_group.update(dt)

            self.screen.fill("black")

            print(len(enemy_group))

            tile_group.draw(self.screen)
            player_group.draw(self.screen)
            enemy_group.draw(self.screen)

            pygame.display.update()
