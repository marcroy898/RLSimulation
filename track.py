import pygame
import numpy as np
from config_var import *

class Track:
    def __init__(self):
        self.track_image = pygame.image.load(CURRENT_TRACK)
        self.track_border_points = np.array(self.create_track_points_list())

    def create_track_points_list(self):
        list_points = []
        for y in range(WINDOW_HEIGHT):
            for x in range(WINDOW_WIDTH):
                if self.track_image.get_at((x, y))[0] == 0:
                    list_points.append([x, y])

        return list_points
