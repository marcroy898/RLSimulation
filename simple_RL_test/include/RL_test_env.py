from gym import Env
from gym.spaces import Discrete, Box
import simple_RL_test.include.RL_test_car_ode as CarODE
import numpy as np
from gym.utils import seeding


class CarEnv(Env):
    def __init__(self, dt, init_state, course_center, course_radius, ACC_const, Steering_const):

        self.agent = CarODE.Car(dt, init_state)
        self.init_state = np.array(init_state)
        self.dt = dt
        self.course_radius = course_radius
        self.course_center = course_center
        self.counter = 0
        self.ACC_const = ACC_const
        self.Steering_const = Steering_const
        self.total_steering = 0

        # Action space and observation space for gym
        self.action_space = Discrete(9)

        self.min_dist = -100
        self.max_dist = 100

        self.observation_space = Box(low=np.array([self.min_dist]), high=np.array([self.max_dist]))

        # Initialization
        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        done = 0
        total_reward = 0

        # Stop after n steps
        for i in range(1000):
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

            acc, steering = self.action_list(action, self.ACC_const, self.Steering_const)

            # Update state of the car
            self.agent.update(acc, steering)

            # Calculate reward
            self.dist2course = np.sqrt((self.agent.state[0]-self.course_center[0])**2 + (self.agent.state[1]-self.course_center[1])**2) - self.course_radius
            self.state = self.dist2course

            if np.abs(self.dist2course) <= 1:
                # reward = -np.abs(self.dist2course) * 100
                reward = 10
            # else:
            #     reward = -np.abs(self.dist2course) * 1000

            if acc <= 0:
                reward = -10

            total_reward = total_reward + reward

            if np.abs(self.dist2course) > 1:
                total_reward = total_reward
                break
        done = 1

        # Return step information
        return self.state, total_reward, done, {}

    def action_list(self, action, ACC_const, Steering_const):
        if action == 0:
            acc = ACC_const
            steering = -Steering_const
        elif action == 1:
            acc = ACC_const
            steering = 0
        elif action == 2:
            acc = ACC_const
            steering = Steering_const
        elif action == 3:
            acc = 0
            steering = -Steering_const
        elif action == 4:
            acc = 0
            steering = 0
        elif action == 5:
            acc = 0
            steering = Steering_const
        elif action == 6:
            acc = -ACC_const
            steering = -Steering_const
        elif action == 7:
            acc = -ACC_const
            steering = 0
        elif action == 8:
            acc = -ACC_const
            steering = Steering_const

        return acc, steering

    def render(self):
        pass

    def reset(self):
        # x = self.np_random.uniform(low=-100, high=100)
        # y = np.sqrt(self.course_radius**2 - x**2)
        # v = self.np_random.uniform(low=-10, high=10)
        # heading = self.np_random.uniform(low=0, high=360)
        x = 0
        y = -100
        v = 5
        heading = 0

        self.init_state = [x, y, v, heading]
        self.agent = CarODE.Car(self.dt, self.init_state)
        self.dist2course = np.sqrt((x - self.course_center[0]) ** 2 + (y - self.course_center[1]) ** 2) - self.course_radius

        self.state = self.dist2course

        # print(self.init_state, 're')

        return self.state