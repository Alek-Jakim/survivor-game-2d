import pygame, sys
from settings import *


class Game:
    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Survivor")

        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(60)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
