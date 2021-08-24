from pygame_RL_test.car_RL_setting import *

RL_agent = RL()
RL_agent.train()
RL_agent.test_agent(n_simulation_steps=1000)


