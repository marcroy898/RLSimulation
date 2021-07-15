import pygame
from math import *
from config_var import *
import math

class Car:

    def __init__(self, x, y, image):
        self.state = [x, y, 0, 0] #x, y, vel, heading

        self.source_image = pygame.image.load(image).convert()
        self.source_image.set_colorkey((0, 0, 0))  #Makes car background transparent
        self.source_image = pygame.transform.scale(self.source_image, (50, 25))
        self.image = self.source_image #Reference for rotation
        self.rect = self.image.get_rect(center=(self.state[0], self.state[1]))
        self.car_mask = pygame.mask.from_surface(self.image)

    def distance_to_ref_lane(self):
        #https://math.stackexchange.com/questions/127613/closest-point-on-circle-edge-from-point-outside-inside-the-circle
        #Not generalized at the moment, only works for circle shaped paths
        circle_radius = 300
        vec_x = self.state[0] - WINDOW_WIDTH/2
        vec_y = self.state[1] - WINDOW_HEIGHT/2
        normalize = math.sqrt((vec_x ** 2) + (vec_y ** 2))
        circle_x = WINDOW_WIDTH/2 + circle_radius * (vec_x/normalize)
        circle_y = WINDOW_HEIGHT/2 + circle_radius * (vec_y/normalize)

        eucl_distance = math.sqrt(abs((self.state[0] - circle_x) ** 2 + (self.state[1] - circle_y) ** 2))

        print(eucl_distance)
        return circle_x, circle_y, eucl_distance

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
        if u1 == 0 and v  > 0:
            dv = -FRICTION

        if u1 == 0 and v  < 0:
            dv = FRICTION

        return [dx, dy, dv, dheading]

    def update_pos(self, dt):
        self.rect = self.image.get_rect(center=[self.state[0], self.state[1]])
        pressed = pygame.key.get_pressed()

        #Rotation
        self.steering = 0
        if pressed[pygame.K_a]:
            self.steering = 25

        if pressed[pygame.K_d]:
            self.steering = -25

        #Movement
        self.acceleration = 0
        if pressed[pygame.K_w]:
            self.acceleration = ACCELERATION_CONSTANT

        if pressed[pygame.K_s]:
            self.acceleration = -ACCELERATION_CONSTANT

        #Car ode
        [dx, dy, dv, dheading] = self.car_ode(self.state, self.acceleration, self.steering)
        self.state = [self.state[0] + dx*dt, self.state[1] - dy*dt, self.state[2] + dv*dt, self.state[3] + dheading*dt] #Subtract from y since top corner is Y=0

        #Rotate car image
        self.heading = self.state[3]
        if self.steering != 0:
            self.rotate_sequence()

        # print(self.state)