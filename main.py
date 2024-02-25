import sys
from settings import *
from scripts.game_state_manager import *

# Scenes
from scenes.menu_scene import Menu
from scenes.character_select_scene import CharacterSelect


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
        self.character_select_scene = CharacterSelect(
            self.screen, self.game_state_manager, self.clock
        )

        self.game_states = {
            "menu": self.menu_scene,
            "character_select": self.character_select_scene,
        }

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    close_game()

            self.clock.tick(FPS)

            self.game_states[self.game_state_manager.get_state()].run()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
