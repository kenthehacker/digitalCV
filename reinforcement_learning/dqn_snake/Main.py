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
epsilon_min = 0.02
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



