from settings import *
from scripts.game_state_manager import Scene
from utils import close_game, draw_text, get_font


class Controls(Scene):
    def __init__(self, screen, game_state_manager):
        super().__init__(screen, game_state_manager)

        self.import_key_icons()

    def import_key_icons(self):
        self.keys = {}

        for folder in os.walk(root_path + "/assets/icons/keyboard"):
            for icon in folder[2]:
                icon_key = icon.split(".")[0]
                self.keys[icon_key] = pygame.transform.scale_by(
                    pygame.image.load(
                        root_path + f"/assets/icons/keyboard/{icon}"
                    ).convert_alpha(),
                    5,
                )

    def draw_controls(self):
        draw_text(
            f"Controls",
            get_font(font_path, 80),
            "white",
            self.screen,
            (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 200),
        )

        # Movement keys
        self.screen.blit(
            self.keys["a_key"],
            (
                WIN_WIDTH // 2 - 300,
                WIN_HEIGHT // 2 - 100,
            ),
        )
        self.screen.blit(
            self.keys["d_key"],
            (
                WIN_WIDTH // 2 - 200,
                WIN_HEIGHT // 2 - 100,
            ),
        )
        draw_text(
            f"MOVE LEFT/RIGHT",
            get_font(font_path, 50),
            "white",
            self.screen,
            (WIN_WIDTH // 2 - 210, WIN_HEIGHT // 2),
        )

        # Jump key
        self.screen.blit(
            self.keys["space_key"],
            (
                WIN_WIDTH // 2 + 150,
                WIN_HEIGHT // 2 - 100,
            ),
        )
        draw_text(
            f"JUMP",
            get_font(font_path, 50),
            "white",
            self.screen,
            (WIN_WIDTH // 2 + 230, WIN_HEIGHT // 2),
        )

        # Attack key
        self.screen.blit(
            self.keys["p_key"],
            (
                WIN_WIDTH // 2 - 35,
                WIN_HEIGHT // 2 + 100,
            ),
        )

        draw_text(
            f"ATTACK",
            get_font(font_path, 50),
            "white",
            self.screen,
            (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 200),
        )

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

            self.screen.fill("black")

            self.draw_controls()

            pygame.display.update()
