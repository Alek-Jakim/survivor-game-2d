from settings import *
from os import walk


class SoundManager:
    def __init__(self):

        self.sounds = {}

        self.import_sounds()

    def import_sounds(self):
        sound_dir = os.walk(root_path + "/assets/sound")
        for folder in sound_dir:
            if folder[2]:
                for file in folder[2]:
                    if file not in self.sounds:
                        f = file.split(".")[0]
                        self.sounds[f] = pygame.mixer.Sound(
                            root_path + f"/assets/sound/{file}"
                        )
