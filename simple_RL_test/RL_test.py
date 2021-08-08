from include.RL_setting import *

RL_agent = RL()
RL_agent.train()
RL_agent.test_agent(n_simulation_steps=500)