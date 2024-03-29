from settings import *


class Scene:
    def __init__(self, screen, game_state_manager):
        self.screen = screen
        self.game_state_manager = game_state_manager

    def run(self):
        pass


class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        print(self.current_state)
        return self.current_state

    def set_state(self, state):
        self.current_state = state
