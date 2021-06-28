import pygame
from car import Car
from config_var import *
from track import Track

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player_car = Car(280, 280, 'Assets/car.png', .05)
        self.game_track = Track()

    def check_collision(self):
        rounded_position = [round(num, 1) for num in self.player_car.position]  #Have to round since black pixel list also rounded
        if rounded_position in self.game_track.track_border_points:
            print("Collision!")

    def game_loop(self):
        running = True
        while running:
            self.screen.blit(self.game_track.track_image, (0, 0))  # Background drawn first

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.player_car.image, self.player_car.rect)
            pygame.draw.ellipse(self.screen, (12, 96, 232), self.player_car.rect, width=1)
            self.player_car.update_pos()
            self.check_collision()
            pygame.display.update()



pygame.init()
Game().game_loop()