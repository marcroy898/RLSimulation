import pygame
from car import Car

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 700))
        self.player_car = Car(280, 280, 'Assets/car.png', .05)

    def game_loop(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))  # Background drawn first

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.player_car.image, self.player_car.rect)
            pygame.draw.rect(self.screen, (10, 10, 10), self.player_car.rect, 1)
            self.player_car.update_pos()
            pygame.display.update()



pygame.init()
Game().game_loop()