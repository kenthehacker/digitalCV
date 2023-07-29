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

tick_rate = 10
epsilon_decay_rate = 0.9999999
epsilon_min = 0.01
epsilon = 0.4
original_epsilon = epsilon
temp_decay = 2.5*original_epsilon/game.num_episodes
input_size = 16
game_size = 20 #bigger because less dimensionality compared to cnn 
def decay_epsilon(epsilon, epsilon_min, epsilon_decay_rate):
    epsilon = max(epsilon_min, epsilon * epsilon_decay_rate)
    return max(epsilon, epsilon_min)

discount_rate = 0.99
model = dqn.CNN_DQN_V3(input_size)
target_model = dqn.CNN_DQN_V3(input_size)
model_path = "CNN_model_params.pth"

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    target_model.load_state_dict(torch.load(model_path))
    print("Loaded "+model_path)

def get_cnn_state(snake_body, food):
    grid = [[0] * game.game_size for _ in range(game.game_size)]
    for body in snake_body:
        if body.is_out_of_bounds() == False:
            grid[body.x][body.y] = 1
    head = snake_body[-1]
    if head.is_out_of_bounds() == False:
        grid[head.x][head.y] = 2
    grid[food.x][food.y] = 3
    return grid

def choose_action(state):
    if np.random.rand() < epsilon:
        return np.random.randint(1,4)
    state_tensor = torch.tensor(state, dtype=torch.float32)
    return torch.argmax(model(state_tensor))

def take_action(action, snake_bodies, food):
    head = snake_bodies[-1]
    new_location = head.theoretical_action(action)
    if new_location == food.get_coord():
        new_head = Entity.Entity(game_size,new_location[0], new_location[1])
        snake_bodies.append(new_head)
        return True
    tail = snake_bodies.pop(0)
    tail.x,tail.y = new_location
    snake_bodies.append(tail)
    return False


training = True
reward_list = []
clock = pygame.time.Clock()
target_update_rate = 100
max_episode = 0

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

pygame.quit()



