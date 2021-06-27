import pygame
from car import Car

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        self.player_car = Car(280, 280, 'Assets/car.png', .05)
        self.track = pygame.image.load('Assets/Track1.png')

    def game_loop(self):
        running = True
        while running:
            self.screen.blit(self.track, (0,0))  # Background drawn first

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.player_car.image, self.player_car.rect)
            pygame.draw.ellipse(self.screen, (12, 96, 232), self.player_car.rect, width=1)
            self.player_car.update_pos()
            pygame.display.update()



pygame.init()
Game().game_loop()