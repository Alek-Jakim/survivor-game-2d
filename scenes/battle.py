from settings import *
from scripts.game_state_manager import Scene
from utils import close_game
from pytmx.util_pygame import load_pygame
from scripts.tile import Tile
from scripts.player import Player


tile_layers = [
    "background_sky",
    "background_buildings",
    "vegetation",
    "fence",
    "ground",
]


class Battle(Scene):
    def __init__(self, screen, game_state_manager, clock):
        super().__init__(screen, game_state_manager)

        self.draw_map()

        self.clock = clock

        self.init_player()

    def draw_map(self):
        tmx_map = load_pygame(root_path + "/assets/tilemap/map.tmx")

        for layer in tile_layers:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(tile_group, surf, (x * 32, y * 32))

    def init_player(self):
        self.player = Player(player_group, (400, 300))

    def run(self):
        running = True
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

            tile_group.draw(self.screen)
            player_group.draw(self.screen)

            pygame.display.update()
