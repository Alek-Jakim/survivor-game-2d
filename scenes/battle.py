from settings import *
from scripts.game_state_manager import Scene
from utils import close_game
from pytmx.util_pygame import load_pygame
from scripts.tile import Tile


tile_layers = [
    "background_sky",
    "background_buildings",
    "vegetation",
    "fence",
    "ground",
]


class Battle(Scene):
    def __init__(self, screen, game_state_manager, clock):
        super().__init__(screen, game_state_manager, clock)

        self.draw_map()

    def draw_map(self):
        tmx_map = load_pygame(root_path + "/assets/tilemap/map.tmx")

        for layer in tile_layers:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Tile(tile_group, surf, (x * 32, y * 32))

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

            tile_group.update()

            tile_group.draw(self.screen)

            pygame.display.update()
