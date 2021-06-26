import time
import pygame
from math import *
from config_var import *
import numpy as np

class Car:

    def __init__(self, x, y, image, start_speed):
        self.position = [x, y]
        self.velocity = 0
        self.acceleration = 0
        self.pointing_vector = [0, 0]

        self.angle = 0
        self.rotate_factor = 0
        self.source_image = pygame.image.load(image).convert()
        self.source_image = pygame.transform.scale(self.source_image, (50,25))
        self.image = self.source_image
        self.rect = self.image.get_rect().move(self.position)

    def rotate_sequence(self):
        self.angle = self.rotate_factor % 360 #Prevent rotation overflow
        self.image = pygame.transform.rotate(self.source_image, self.angle)

        #Keeps the car in place when rotating
        x,y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update_pos(self):
        self.pointing_vector = [(cos(radians(self.angle))), (sin(radians(self.angle)))]
        self.acceleration = 0
        self.rect = self.image.get_rect(topleft=self.position)
        pressed = pygame.key.get_pressed()

        #Rotation
        if pressed[pygame.K_a]:
            self.rotate_factor += .1

        if pressed[pygame.K_d]:
            self.rotate_factor -= .1

        if self.rotate_factor != 0:
            self.rotate_sequence()

        #Movement
        if pressed[pygame.K_w]:
            self.acceleration = ACCELERATION_CONSTANT

        if abs(self.velocity) < MAX_SPEED:
            self.velocity += self.acceleration
        else:
            self.velocity = MAX_SPEED

        #Friction
        if self.acceleration == 0 and self.velocity > 0:
            self.velocity -= FRICTION
            self.velocity = max(0, self.velocity)

        if self.acceleration == 0 and self.velocity < 0:
            self.velocity += FRICTION
            self.velocity = max(0, self.velocity)

        dx = self.velocity * self.pointing_vector[0]
        dy = self.velocity * self.pointing_vector[1]
        self.position = [self.position[0] + dx, self.position[1] - dy] #Subtract from y since top corner is Y=0

        print("Pos: " + str(self.position) + " Velocity: " + str(self.velocity) + " Acc: " + str(self.acceleration))
