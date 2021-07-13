import numpy as np
import math

class Car:
    def __init__(self, dt, init_state):
        self.state = init_state
        self.dt = dt
        self.vehicle_length = 2
        self.vehicle_width = 1
        self.state_history = [self.state]

    def update(self, acc, psi):
        lf = self.vehicle_length / 2
        lr = self.vehicle_length / 2

        x = self.state[0]
        y = self.state[1]
        v = self.state[2]
        heading = self.state[3]
        beta = math.atan(lr / (lf + lr) * math.tan(np.radians(psi)))
        dx = v * math.cos(np.radians(heading) + beta)
        dy = v * math.sin(np.radians(heading) + beta)
        dheading = np.degrees(v / lr * math.sin(beta))

        # Bound
        MAX_SPEED = 10
        if abs(v) >= MAX_SPEED:
            dv = 0
        else:
            dv = acc

        # Friction
        FRICTION = 0.5

        if acc == 0 and v > 0:
            dv = -FRICTION

        if acc == 0 and v < 0:
            dv = FRICTION

        self.state = [x + dx * self.dt,
                      y + dy * self.dt,
                      v + dv * self.dt,
                      self.__normalize_angle(heading + dheading * self.dt)]
        self.state_history.append(self.state)

    def __normalize_angle(self, angle):

        while angle > 360:
            angle -= 360

        while angle < 0:
            angle += 360
        return angle

    def get_pos(self):
        x = np.array(self.state_history)[:, 0]
        y = np.array(self.state_history)[:, 1]

        return x, y

    def get_heading(self):
        heading = np.array(self.state_history)[:, 3]

        return heading
