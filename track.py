import pygame
import numpy as np
from config_var import *

class Track:
    def __init__(self, screen):
        self.track_rect = pygame.Rect((100, 100), (900, 500))
        self.track_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.track_lane = pygame.draw.circle(screen, (255, 0, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 300, 1)
        #Creates a mask over all of the red pixels on screen
        self.track_mask = pygame.mask.from_threshold(screen, (255, 0, 0), (254, 254, 254))
        self.track_points = self.track_mask.outline()

