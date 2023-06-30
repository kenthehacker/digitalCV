import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
import Deep_q_nn as dqn
import pygame
import Game_frame as game
import Entity
import pickle
import matplotlib.pyplot as plt
import Functions as f
import os

'''
one hot encoding vs categorical representation of direction:
using categorical data means model can misinterp information as continous not discrete
hence direction is represented as 4 digit binaries
However it will introduce higher dimension 
'''

epsilon_decay_rate = 0.99999
epsilon_min = 0.02
epsilon = 0.35
original_epsilon = epsilon
temp_decay = 2.5*original_epsilon/game.num_episodes
input_size = 16
game_size = 20 #bigger because less dimensionality compared to cnn 
def decay_epsilon():
    epsilon = max(epsilon_min, epsilon * epsilon_decay_rate)
    return max(epsilon, epsilon_min)

discount_rate = 0.85
model = dqn.Linear_snake(input_size)
target_model = dqn.Linear_snake(input_size)
model_path = "linear_snake_parameters.pth"

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    target_model.load_state_dict(torch.load(model_path))
    print("Loaded "+model_path)

loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
display_rate = game.display_rate

def get_state_linear(snake_bodies, food, speed):
    head = snake_bodies[-1]
    state = [
        #food relative position to snake head
        int(head.x < food.x),
        int(head.x > food.x),
        int(head.y < food.y),
        int(head.y > food.y),

        #direction of snake
        int(speed[0] > 0),
        int(speed[0] < 0),
        int(speed[1] > 0),
        int(speed[1] < 0),

        #direct obstacles relative to head
        int(head.x == 0),
        int(head.x == game_size-1),
        int(head.y == 0),
        int(head.y == game_size-1),

        #collision w/itself
        int(head.theoretical_action(0) in [body.get_coord() for body in snake_bodies]),
        int(head.theoretical_action(1) in [body.get_coord() for body in snake_bodies]),
        int(head.theoretical_action(2) in [body.get_coord() for body in snake_bodies]),
        int(head.theoretical_action(3) in [body.get_coord() for body in snake_bodies])

    ]
    return state



def choose_action(state):
    if np.random.rand() <= epsilon:
        return np.random.randint(1,4)
    state_tensor = torch.tensor(state,dtype=torch.float64)
    q_values = model(state_tensor)
    action = torch.argmax(q_values)
    return action
    
def take_action(action, snake_bodies, food):
    head = snake_bodies[-1]
    if head.theoretical_action(action) == food.get_coord():
        pass
    else:
        pass 



training = True


reward_list = []
max_episode = 0
speed = (1,0)
try:
    pass
except KeyboardInterrupt:
    print("Keyboard interrupt saving model param")
finally:
    print(reward_list)
    torch.save(model.state_dict(), model_path)

print("REACHED EPISODE "+str(max_episode)+" EPSILON "+str(epsilon))

sub_reward_list = reward_list[-250:]
fig, ax = plt.subplots()
ax.plot(sub_reward_list)
plt.tight_layout()
plt.show()



