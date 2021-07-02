import pygame
import numpy as np
from config_var import *

class Track:
    def __init__(self):
        self.track_image = pygame.image.load(CURRENT_TRACK)
        self.track_mask = pygame.mask.from_threshold(self.track_image, (0, 0, 0), (254, 254, 254))