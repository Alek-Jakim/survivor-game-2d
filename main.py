import pygame, sys
from settings import *
from scripts.game_state_manager import *


class Menu(Scene):
    def __init__(self, screen, game_state_manager, clock):
        super().__init__(screen, game_state_manager, clock)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_l:
                        self.game_state_manager.set_state("character_choice")
                        running = False

            self.screen.fill("purple")

            pygame.display.update()


class CharacterChoice(Scene):
    def __init__(self, screen, game_state_manager, clock):
        super().__init__(screen, game_state_manager, clock)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_m:
                        self.game_state_manager.set_state("menu")
                        running = False

            self.screen.fill("red")

            pygame.display.update()


# Main game loop
class Game:
    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Survivor")

        self.clock = pygame.time.Clock()

        # Game states
        self.game_state_manager = GameStateManager("menu")

        self.menu_scene = Menu(self.screen, self.game_state_manager, self.clock)
        self.character_choice_scene = CharacterChoice(
            self.screen, self.game_state_manager, self.clock
        )

        self.game_states = {
            "menu": self.menu_scene,
            "character_choice": self.character_choice_scene,
        }

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(FPS)

            self.game_states[self.game_state_manager.get_state()].run()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
