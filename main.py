import pygame
from car import Car

#Intializes pygame
pygame.init()

#Screen intialization, WidthxHeight
screen = pygame.display.set_mode((800,600))

#Car intialization
player_car = Car(280, 280, 'Assets/car.png', .05)


#Running Game Loop: Anything persistent must be in here
running = True
while running:
    screen.fill((255, 255, 255)) #Background drawn first

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(player_car.image, player_car.rect)
    pygame.draw.rect(player_car.image,(10,10,10), player_car.rect, 1)
    player_car.update_pos()
    pygame.display.update()