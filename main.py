import pygame
from car import Car
from config_var import *
from track import Track
from math import *
import numpy as np

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player_car = Car(280, 280, 'Assets/car.png', .05)
        self.game_track = Track()

    def check_collision(self):
        angled_corners = [
            (self.player_car.rect.centerx + (25 * cos(radians(self.player_car.angle + 30))),  #Top-left corner
             self.player_car.rect.centery - (25 * sin(radians(self.player_car.angle + 30)))),
            (self.player_car.rect.centerx + (25 * cos(radians(self.player_car.angle - 30))),  # Top-right corner
             self.player_car.rect.centery - (25 * sin(radians(self.player_car.angle - 30)))),
            (self.player_car.rect.centerx - (25 * cos(radians(self.player_car.angle - 30))),  # Bottom-left corner
             self.player_car.rect.centery + (25 * sin(radians(self.player_car.angle - 30)))),
            (self.player_car.rect.centerx - (25 * cos(radians(self.player_car.angle + 30))),  # Bottom-right corner
             self.player_car.rect.centery + (25 * sin(radians(self.player_car.angle + 30))))
        ]

        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[0], radius=2, width=3)
        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[1], radius=2, width=3)
        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[2], radius=2, width=3)
        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[3], radius=2, width=3)

        rounded_position = [(round(angled_corners[0][0]), round(angled_corners[0][1])),
                            (round(angled_corners[1][0]), round(angled_corners[1][1])),
                            (round(angled_corners[2][0]), round(angled_corners[2][1])),
                            (round(angled_corners[3][0]), round(angled_corners[3][1])),
                            ]  #Have to round since black pixel list also rounded

        rounded_position = np.array(rounded_position)

        nrows, ncols = self.game_track.track_border_points.shape
        dtype = {'names': ['f{}'.format(i) for i in range(ncols)],
                 'formats': ncols * [self.game_track.track_border_points.dtype]}
        C = np.intersect1d(self.game_track.track_border_points.view(dtype), rounded_position.view(dtype))


        if C.size > 0:
            print("Collision")



    def game_loop(self):
        running = True
        while running:
            self.screen.blit(self.game_track.track_image, (0, 0))  # Background drawn first

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.player_car.image, self.player_car.rect)
            self.player_car.update_pos()
            self.check_collision()
            pygame.display.update()



pygame.init()
Game().game_loop()