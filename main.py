import pygame
from car import Car
from config_var import *
from track import Track
from math import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player_car = Car(280, 280, 'Assets/car.png', .05)
        self.game_track = Track()

    def check_collision(self):
        # rounded_position = [round(num, 1) for num in self.player_car.position]  #Have to round since black pixel list also rounded
        # if rounded_position in self.game_track.track_border_points:
        #     print("Collision!")
        angled_corners = [
            (self.player_car.rect.centerx + (25*cos(radians(self.player_car.angle + 25))),  #Top-left corner
             self.player_car.rect.centery - (25*sin(radians(self.player_car.angle + 25)))),
            (self.player_car.rect.centerx + (25 * cos(radians(self.player_car.angle - 25))),  # Top-right corner
             self.player_car.rect.centery - (25 * sin(radians(self.player_car.angle - 25)))),
            (self.player_car.rect.centerx - (25 * cos(radians(self.player_car.angle - 25))),  # Bottom-left corner
             self.player_car.rect.centery + (25 * sin(radians(self.player_car.angle - 25)))),
            (self.player_car.rect.centerx - (25 * cos(radians(self.player_car.angle + 25))),  # Bottom-right corner
             self.player_car.rect.centery + (25 * sin(radians(self.player_car.angle + 25))))
        ]
        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[0], radius=2, width=3)
        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[1], radius=2, width=3)
        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[2], radius=2, width=3)
        pygame.draw.circle(self.screen, (12, 96, 232), angled_corners[3], radius=2, width=3)
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