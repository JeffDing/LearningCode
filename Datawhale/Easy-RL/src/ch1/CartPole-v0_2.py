import gym  

import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

env = gym.make('CartPole-v1')  
env.reset()  
for _ in range(1000):
    env.render()  
    action = env.action_space.sample() 
    observation, reward, done, info = env.step(action)
    print(observation)
env.close()   
