import pygame
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
from gym.utils import seeding
from pygame_RL_test.car import Car
from pygame_RL_test.config_var import *

class CarEnv(Env):
    def __init__(self, dt, init_state):
        self.init_render()

        self.agent = Car(dt, init_state)
        self.agent_state = self.agent.state
        self.init_state = np.array(init_state)
        self.dt = dt
        self.counter = 0

        self.course_center = [WINDOW_WIDTH/2, WINDOW_HEIGHT/2]
        # Action space and observation space for gym
        self.action_space = Discrete(9)

        self.max_speed = 10
        self.min_heading = 0
        self.max_heading = 360
        self.min_dist = -25
        self.max_dist = 25

        self.low = np.array([-self.max_speed, self.min_heading, self.min_dist])
        self.high = np.array([self.max_speed, self.max_heading, self.max_dist])
        self.observation_space = Box(self.low, self.high, dtype=np.float32)

        # Initialization
        self.seed()
        self.reset()


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        done = 0

        # Stop after n steps
        self.counter += 1
        if self.counter == 1000:
            self.counter = 0
            done = 1
            reward = 0
            return self.state, reward, done, {}
        else:
            # nine different actions
            # ----------------------------------------------------
            #               Steer left      hold      Steer right
            # ----------------------------------------------------
            #    +Acc       action #0     action #1    action #2
            # ----------------------------------------------------
            #   No Acc      action #3     action #4    action #5
            # ----------------------------------------------------
            #    -Acc       action #6     action #7    action #8
            # ----------------------------------------------------

            acc, steering = self.action_list(action)

            # Update state of the car
            self.agent.update_pos(acc, steering)

            #Reward to be implemented
            self.dist2course = np.sqrt((self.agent.state[0]-self.course_center[0])**2 + (self.agent.state[1]-self.course_center[1])**2) - circ_track_radius

            if self.dist2course >= 50:
                # reward = np.exp(-(self.dist2course+np.abs(dist2wp)))
                # reward = np.exp(-self.dist2course)
                reward = -self.dist2course
            elif 10 < self.dist2course < 50:
                reward = 100 - self.dist2course
            elif self.dist2course <= 10:
                reward = 500 - self.dist2course
            else:
                # done = 1
                reward = -1000

            return self.state, reward, done, {}

    def action_list(self, action):
        if action == 0:
            acc = ACC_const/self.dt
            steering = -Steering_const/self.dt
        elif action == 1:
            acc = ACC_const / self.dt
            steering = 0
        elif action == 2:
            acc = ACC_const / self.dt
            steering = Steering_const / self.dt
        elif action == 3:
            acc = 0
            steering = -Steering_const / self.dt
        elif action == 4:
            acc = 0
            steering = 0
        elif action == 5:
            acc = 0
            steering = Steering_const / self.dt
        elif action == 6:
            acc = -ACC_const / self.dt
            steering = -Steering_const / self.dt
        elif action == 7:
            acc = -ACC_const / self.dt
            steering = 0
        elif action == 8:
            acc = -ACC_const / self.dt
            steering = Steering_const / self.dt

        self.render()

        return acc, steering

    def init_render(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

    def render(self):
        self.window.fill((255, 255, 255))  # Background drawn first
        pygame.draw.circle(self.window, (255, 0, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 300, 1)  # Reference lane
        self.window.blit(self.agent.image, self.agent.rect)
        pygame.display.update()


    def reset(self):
        x = self.np_random.uniform(low=100, high=WINDOW_WIDTH - 100)
        y = self.np_random.uniform(low=100, high=WINDOW_HEIGHT - 100)
        v = self.np_random.uniform(low=-10, high=10)
        heading = self.np_random.uniform(low=0, high=360)

        self.init_state = [x, y, v, heading]
        self.agent = Car(self.dt, self.init_state)
        self.dist2course = np.sqrt((x - self.course_center[0]) ** 2 + (y - self.course_center[1]) ** 2) - circ_track_radius


        self.state = np.append(np.array([v, heading]), self.dist2course)

        return self.state
