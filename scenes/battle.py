from settings import *
from scripts.game_state_manager import Scene
from utils import close_game


class Battle(Scene):
    def __init__(self, screen, game_state_manager, clock):
        super().__init__(screen, game_state_manager, clock)

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

            self.screen.fill("red")

            pygame.display.update()
