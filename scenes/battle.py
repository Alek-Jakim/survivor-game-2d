from settings import *
from scripts.game_state_manager import Scene
from utils import close_game
from pytmx.util_pygame import load_pygame
from scripts.tile import Tile, CollisionTile
from scripts.player import Player


tile_layers = ["sky", "buildings", "buildings_back", "ground"]


class Battle(Scene):
    def __init__(self, screen, game_state_manager, clock, sound_manager):
        super().__init__(screen, game_state_manager)

        self.clock = clock

        self.sound_manager = sound_manager

        self.init_player()

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

            delta = self.clock.tick(FPS) / 1000

            tile_group.update()
            player_group.update(delta)

            self.screen.fill("black")

            tile_group.draw(self.screen)
            player_group.draw(self.screen)

            pygame.display.update()
