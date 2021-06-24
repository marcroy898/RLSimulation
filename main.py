import pygame

#Intializes pygame
pygame.init()

#Screen intialization, WidthxHeight
screen = pygame.display.set_mode((800,600))

#Car intialization
carImg = pygame.image.load('Assets/car.png')
carImg = pygame.transform.scale(carImg, (50,25)) #Original image 960x480, scaled down in 2:1 ratio
carX = 370
carY = 500

def car():
    screen.blit(carImg, (carX, carY))

#Running Game Loop: Anything persistent must be in here
running = True
while running:
    screen.fill((255, 255, 255)) #Background drawn first

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car()
    pygame.display.update()