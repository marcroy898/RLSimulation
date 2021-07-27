from gym import Env
from gym.spaces import Discrete, Box
import simple_RL_test.include.RL_test_car_ode as CarODE
import numpy as np
from gym.utils import seeding


class CarEnv(Env):
    def __init__(self, dt, init_state, course_center, course_radius):

        self.agent = CarODE.Car(dt, init_state)
        self.agent_state = self.agent.state
        self.init_state = np.array(init_state)
        self.dt = dt
        self.course_radius = course_radius
        self.course_center = course_center
        self.counter = 0

        # Action space and observation space for gym
        self.action_space = Discrete(9)

        self.min_position_x = -110
        self.max_position_x = 110
        self.min_position_y = -110
        self.max_position_y = 110
        self.max_speed = 10
        self.min_heading = 0
        self.max_heading = 360
        self.min_dist = -15
        self.max_dist = 15

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
            ACC_const = 0.1
            Steering_const = 5

            acc, steering = self.action_list(action, ACC_const, Steering_const)

            # Update state of the car
            self.agent.update(acc, steering)

            # Update waypoint
            dist2wp = np.sqrt((self.current_wp[0]-self.agent.state[0])**2+ (self.current_wp[1] - self.agent.state[1])**2)
            if dist2wp < 10:
                self.current_wp_idx += 1
                self.current_wp_idx = self.current_wp_idx % len(self.waypoints)
                self.current_wp = self.waypoints[self.current_wp_idx]
                dist2wp = np.sqrt((self.current_wp[0] - self.agent.state[0]) ** 2 + (self.current_wp[1] - self.agent.state[1]) ** 2)

            # Calculate reward
            self.dist2course = np.sqrt((self.agent.state[0]-self.course_center[0])**2 + (self.agent.state[1]-self.course_center[1])**2) - self.course_radius
            self.state = np.append(np.array(self.agent.state)[2:], self.dist2course)

            # Condition1: If |dist2course| > 9, reward: -5000, done
            # Condition2: If 0 < dist2course < 5, acc > 0, reward: 5, otherwise -5
            # print("state:", np.array(self.state))
            # print(self.current_wp_idx, self.dist2course, dist2wp)
            # print('--------------')

            # if self.state[0] > 0 and self.dist2course >= 0 and self.dist2course < 5:
            if self.dist2course >= 50:
                # reward = np.exp(-(self.dist2course+np.abs(dist2wp)))
                # reward = np.exp(-self.dist2course)
                reward = -dist2wp
            elif 10 < self.dist2course < 50:
                reward = 100 - dist2wp
            elif self.dist2course <= 10:
                reward = 500 - dist2wp
            else:
                # done = 1
                reward = -1000

            # if np.abs(self.dist2course) > 10:
            #     # done = 1
            #     reward = -1000

            # print("count:", self.counter)
            # # print("wp_idx:",self.current_wp_idx)
            # # print("wp:", self.current_wp)
            # print("dist2course:", self.dist2course)
            # print("dist2wp:", dist2wp)
            # if dist2wp < 10:
            #     print("Waypoint change")
            # print("reward: ", reward)
            # print("------------------")

            # Return step information
            return self.state, reward, done, {}

    def action_list(self, action, ACC_const, Steering_const):
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

    def render(self):
        pass

    def reset(self):
        x = self.np_random.uniform(low=-100, high=100)
        y = np.sqrt(self.course_radius**2 - x**2)
        v = self.np_random.uniform(low=-10, high=10)
        heading = self.np_random.uniform(low=0, high=360)

        self.waypoints = np.array([[self.course_center[0] + self.course_radius, self.course_center[1]],
                                   [self.course_center[0] - self.course_radius, self.course_center[1]],
                                   [self.course_center[0], self.course_center[1] + self.course_radius * 2],
                                   ])

        self.init_state = [x, y, v, heading]
        self.agent = CarODE.Car(self.dt, self.init_state)
        self.dist2course = np.sqrt((x - self.course_center[0]) ** 2 + (y - self.course_center[1]) ** 2) - self.course_radius

        self.current_wp_idx = np.argmin([np.sqrt((wp[0]-self.agent.state[0])**2+ (wp[1] - self.agent.state[1])**2) for wp in self.waypoints])
        self.current_wp = self.waypoints[self.current_wp_idx]

        self.state = np.append(np.array([v, heading]), self.dist2course)

        return self.state