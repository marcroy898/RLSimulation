import numpy as np
import simple_RL_test.include.RL_test_car_ode as CarODE
import simple_RL_test.include.RL_test_env as car_env
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

class RL():
    def __init__(self):
        # --------- Course is a circle in this example ----------------
        self.course_radius = 100
        self.course_center = (0, 0)
        self.dt = 0.1
        self.init_state = [0, -self.course_radius, 5, 0] # x, y, vel, heading
        self.ACC_const = 0.1
        self.Steering_const = 5

        self.env = car_env.CarEnv(self.dt, self.init_state, self.course_center, self.course_radius, self.ACC_const, self.Steering_const)

        self.states = self.env.observation_space.shape
        self.actions = self.env.action_space.n



    # ------- Deep Learning Model with Keras ----------------
    def __build_model(self):
        self.model = Sequential()
        self.model.add(Flatten(input_shape=(1,) + self.states))

        # self.model.add(Dense(16, activation='relu', input_shape=self.states))
        self.model.add(Dense(50, activation='relu'))
        self.model.add(Dense(50, activation='relu'))
        self.model.add(Dense(50, activation='relu'))
        self.model.add(Dense(self.actions, activation='linear'))

    # -------- Build Agent with Keras-RL -----------------------------
    def __build_agent(self):
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=50000, window_length=1)
        self.dqn = DQNAgent(model=self.model, memory=memory, policy=policy,
                      nb_actions=self.actions, nb_steps_warmup=10, target_model_update=1e-2)
        self.dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    # -------- Train RL agent ---------------------------------
    def train(self):
        self.__build_model()
        self.__build_agent()
        self.dqn.fit(self.env, nb_steps=5000, visualize=False, verbose=1)
        self.dqn.save_weights('dqn_weights.h5f', overwrite=True)
        # scores = self.dqn.test(self.env, nb_episodes=10, visualize=False)
        # filename = "result.txt"
        # np.savetxt(filename, scores.history['episode_reward'])

    # -------- Load trained weight and run -------------------
    def test_agent(self, n_simulation_steps):
        self.__build_model()
        self.__build_agent()

        self.dqn.load_weights('dqn_weights.h5f')
        # _ = self.dqn.test(self.env, nb_episodes=5, visualize=False)
        test_car_agent = CarODE.Car(self.dt, self.init_state)

        for step in range(n_simulation_steps):
            dist2course = np.sqrt((test_car_agent.state[0] - self.course_center[0]) ** 2 + (test_car_agent.state[1] - self.course_center[1]) ** 2) - self.course_radius
            # xtest = np.array([dist2course])
            xtest = np.reshape(np.append(np.array(test_car_agent.state[3]), dist2course), (1, 1, -1))
            action = self.dqn.model.predict(xtest, batch_size=1)
            action = np.argmax(action[0])

            acc, steering = self.env.action_list(action, self.ACC_const, self.Steering_const)
            test_car_agent.update(acc, steering)

        x, y = test_car_agent.get_pos()

        fig, ax = plt.subplots(figsize=(7,7))
        circle = plt.Circle(self.course_center, self.course_radius, color='b', fill=False)
        ax.set_aspect('equal')
        ax.plot()  # Causes an autoscale update.
        ax.add_patch(circle)
        plt.plot(x, y, '-or')
        plt.show()


