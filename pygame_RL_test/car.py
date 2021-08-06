import pygame
from math import *
from pygame_RL_test.config_var import *
import math
import numpy as np

class Car:

    def __init__(self, dt, init_state):
        self.state = init_state #x, y, vel, heading
        self.dt = dt

        self.source_image = pygame.image.load(CAR_IMG).convert()
        self.source_image.set_colorkey((0, 0, 0))  #Makes car background transparent
        self.source_image = pygame.transform.scale(self.source_image, (50, 25))
        self.image = self.source_image #Reference for rotation
        self.rect = self.image.get_rect(center=(self.state[0], self.state[1]))
        self.car_mask = pygame.mask.from_surface(self.image)

        self.state_history = [self.state]


    def rotate_sequence(self):
        self.heading = self.heading % 360  #Prevent rotation overflow
        self.image = pygame.transform.rotate(self.source_image, self.heading)

        #Keeps the car in place when rotating
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def car_ode(self, state, u1, u2):
        lf = 1
        lr = 1
        x = state[0]
        y = state[1]
        v = state[2]
        angle = state[3]
        beta = math.atan(lr / (lf + lr) * math.tan(radians(u2)))
        dx = v * math.cos(radians(angle) + beta)
        dy = v * math.sin(radians(angle) + beta)
        dheading = v / lr * math.sin(beta)

        #Bound
        if abs(v) >= MAX_SPEED:
            dv = 0
        else:
            dv = u1

        #Friction
        if u1 == 0 and v > 0:
            dv = -FRICTION

        if u1 == 0 and v < 0:
            dv = FRICTION

        return [dx, dy, dv, dheading]

    def update_pos(self, acc, steering):
        self.rect = self.image.get_rect(center=[self.state[0], self.state[1]])
        self.acceleration = acc
        self.steering = steering

        #Car ode
        [dx, dy, dv, dheading] = self.car_ode(self.state, self.acceleration, self.steering)
        self.state = [self.state[0] + dx*self.dt, self.state[1] - dy*self.dt, self.state[2] + dv*self.dt, self.state[3] + dheading*self.dt] #Subtract from y since top corner is Y=0

        #Rotate car image
        self.heading = self.state[3]
        if self.steering != 0:
            self.rotate_sequence()

        self.state_history.append(self.state)


    def get_pos(self):
        x = np.array(self.state_history)[:, 0]
        y = np.array(self.state_history)[:, 1]

        return x, y
