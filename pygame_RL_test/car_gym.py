import math
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

        self.waypoints = self.get_waypoints(60)
        self.current_wp_idx = 0

        # Action space and observation space for gym
        self.action_space = Discrete(9)

        self.max_speed = MAX_SPEED
        self.min_heading = 0
        self.max_heading = 360
        self.min_x = 0
        self.max_x = WINDOW_WIDTH
        self.min_y = 0
        self.max_y = WINDOW_HEIGHT
        self.min_ref_dist = 0
        self.max_ref_dist = 1000
        self.dist_traveled = 0

        self.low = np.array([self.min_x, self.min_y, -self.max_speed, self.min_heading, self.min_ref_dist])
        self.high = np.array([self.max_x, self.max_y, self.max_speed, self.max_heading, self.max_ref_dist])
        self.observation_space = Box(self.low, self.high, dtype=np.float32)

        # Initialization
        self.seed()
        self.reset()


    def get_waypoints(self, n_degrees):
        angle = n_degrees
        waypoints = []
        while abs(angle) < 360:
            waypoints.append((self.course_center[0] + circ_track_radius * math.cos(math.radians(angle)),
                              self.course_center[1] + circ_track_radius * math.sin(math.radians(angle))))
            angle -= n_degrees
        return np.array(waypoints)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self.render()
        done = 0
        self.dist2course = np.sqrt((self.agent.state[0] - self.course_center[0]) ** 2 + (
                    self.agent.state[1] - self.course_center[1]) ** 2) - circ_track_radius

        # Stop after n steps
        self.counter += 1
        if self.counter == 10000:
            self.counter = 0
            done = 1
            reward = 0
            return self.state, reward, done, {}
        if abs(self.dist2course) > 45:
            self.counter = 0
            done = 1
            reward = -5000
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
            self.dist_traveled += self.agent.state[2] * self.dt
            dist2wp = np.sqrt((self.current_wp[0] - self.agent.state[0]) ** 2 + (self.current_wp[1] - self.agent.state[1]) ** 2)
            if dist2wp < 10:
                self.current_wp_idx += 1
                self.current_wp_idx = self.current_wp_idx % len(self.waypoints)
                self.current_wp = self.waypoints[self.current_wp_idx]
                dist2wp = np.sqrt((self.current_wp[0] - self.agent.state[0]) ** 2 + (self.current_wp[1] - self.agent.state[1]) ** 2)
                reward = 500
            else:
                reward = -dist2wp
            # print("dist2course:", self.dist2course)
            # print("reward: ", reward)
            # print("state: ", self.state)
            # print("agent state: ", self.agent.state)
            # print("distance traveled: ", self.dist_traveled)
            # print("Current WP:", (self.current_wp[0], self.current_wp[1]))
            # print("Distance 2 wp", dist2wp)
            # print("Reward:", reward)
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
        pygame.draw.circle(self.window, (0, 0, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 240, 3)  # Wall
        pygame.draw.circle(self.window, (0, 0, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), 360, 3)  # Wall
        for x in self.waypoints:
            pygame.draw.circle(self.window, (0, 0, 0), (x[0], x[1]), 3, 1)
        self.window.blit(self.agent.image, self.agent.rect)
        pygame.display.update()

    def reset(self):
        # x = self.np_random.uniform(low=300, high=900)
        # y = np.sqrt(circ_track_radius**2 - x**2)
        # v = self.np_random.uniform(low=-MAX_SPEED, high=MAX_SPEED)
        # heading = self.np_random.uniform(low=0, high=360)

        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT / 2 + 300
        v = 0
        heading = 0

        self.init_state = [x, y, v, heading]
        self.agent = Car(self.dt, self.init_state)
        self.dist2course = np.sqrt((x - self.course_center[0]) ** 2 + (y - self.course_center[1]) ** 2) - circ_track_radius
        self.dist_traveled = 0
        self.current_wp_idx = 0
        self.current_wp = self.waypoints[self.current_wp_idx]

        self.state = np.append(self.agent.state, self.dist2course)
        return self.state
