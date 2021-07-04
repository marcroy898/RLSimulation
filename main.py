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
        self.clock = pygame.time.Clock()

    def check_collision(self):
        if self.game_track.track_mask.overlap(self.player_car.car_mask,
                                              (round(self.player_car.state[0]), round(self.player_car.state[1]))):
            print("Collision")



    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #Timestep
            dt = self.clock.tick(60)
            dt /= 1000 #Convert ms -> sec
            #Game rendering
            self.screen.blit(self.game_track.track_image, (0, 0))  # Background drawn first
            self.screen.blit(self.player_car.image, self.player_car.rect)
            self.player_car.update_pos(dt)
            self.check_collision()
            pygame.display.update()



pygame.init()
Game().game_loop()