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

        self.max_speed = MAX_SPEED
        self.min_heading = 0
        self.max_heading = 360
        self.min_dist = -1500
        self.max_dist = 1500

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
        self.render()
        done = 0

        # Stop after n steps
        self.counter += 1
        if self.counter == 2000:
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

            self.dist2course = abs(np.sqrt((self.agent.state[0]-self.course_center[0])**2 + (self.agent.state[1]-self.course_center[1])**2) - circ_track_radius)
            if self.dist2course >= 20:
                # reward = np.exp(-(self.dist2course+np.abs(dist2wp)))
                # reward = np.exp(-self.dist2course)
                reward = -self.dist2course
            elif 5 < self.dist2course < 20:
                reward = 500 - self.dist2course
                if self.agent.state[2] > 20:
                    reward += 50
            elif self.dist2course <= 5:
                reward = 1000 - self.dist2course
                if self.agent.state[2] > 20:
                    reward += 100
            else:
                # done = 1
                reward = -1000

            if self.agent.state[2] == 0:
                reward = -10000
            # print("dist2course:", self.dist2course)
            # print("reward: ", reward)
            # print("state: ", self.state)
            # print("agent state: ", self.agent.state)
            # print("------------------")
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
        # x = self.np_random.uniform(low=300, high=900)
        # y = np.sqrt(circ_track_radius**2 - x**2)
        # v = self.np_random.uniform(low=-30, high=30)
        # heading = self.np_random.uniform(low=0, high=360)

        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT / 2
        v = 0
        heading = 0

        self.init_state = [x, y, v, heading]
        self.agent = Car(self.dt, self.init_state)
        self.dist2course = np.sqrt((x - self.course_center[0]) ** 2 + (y - self.course_center[1]) ** 2) - circ_track_radius

        self.state = np.append(np.array([v, heading]), self.dist2course)
        return self.state
