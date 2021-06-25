import time
import pygame


class Car:

    def __init__(self, x, y, image, speed):
        self.speed = speed
        self.max_speed = 500 #pixels
        self.acceleration = 85 #pixels
        self.angle = 0
        self.rotate_factor = 0
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.source_image = pygame.image.load(image).convert()
        self.source_image = pygame.transform.scale(self.source_image, (50,25))
        self.image = self.source_image
        self.rect = self.image.get_rect().move(self.x,self.y)


    def rotate_sequence(self):
        self.angle = self.rotate_factor % 360
        self.image = pygame.transform.rotate(self.source_image, self.angle)
        x,y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update_pos(self):
        self.rect = self.image.get_rect(topleft=(self.x, self.y)) #Set rectangle to match x and y
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.x = self.x + self.speed
        if pressed[pygame.K_a]:
            self.rotate_factor += .1

        if pressed[pygame.K_d]:
            self.rotate_factor -= .1

        if self.rotate_factor != 0:
            self.rotate_sequence()
            print(self.image.get_size())

        # self.speed = self.speed + self.acceleration



