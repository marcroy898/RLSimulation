import pygame


class Car:

    def __init__(self, x, y, image, speed):
        self.speed = speed
        self.max_speed = 500 #pixels/second
        self.acceleration = 85 #pixels/second^2
        self.angle = 90
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.source_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.source_image, (50,25))

    def update_pos(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.x = self.x + self.speed
        rotate_factor = 0
        if pressed[pygame.K_a]:
            rotate_factor -= 1
        if pressed[pygame.K_d]:
            rotate_factor += 1

        if rotate_factor != 0:
            self.angle += rotate_factor
            self.image = pygame.transform.rotate(self.image, self.angle)
        # self.speed = self.speed + self.acceleration

