import torch
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random

#classes specific for snake game

class CNN_DQN(nn.Module):
    def __init__(self, game_dimension):
        input_channel = 1
        output_channel = 1
        super(CNN_DQN, self).__init__()
        self.layer1 = nn.Conv2d(input_channel, output_channel, kernel_size=5, stride=3, padding=1)
        #self.layer2 = nn.Linear(output_channel * game_dimension * game_dimension, 128)
        self.layer2 = nn.Linear(9, 128)
        self.layer3 = nn.Linear(128, 64)
        self.layer4 = nn.Linear(64, 4)
        #so since we have 4 outputs we're getting a 1D array of 4 values, each value represents the q value of an action we can take
        
    def forward(self, x):
        #x = torch.stack(x)
        x = F.relu(self.layer1(x))
        x = x.view(x.size(0), -1)
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        x = self.layer4(x)
        return x.squeeze()
class CNN_DQN_V2(nn.Module):
    def __init__(self,game_dimension):
        super(CNN_DQN_V2, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(32 * 10 * 10, 64)
        self.fc2 = nn.Linear(64, 4)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

class CNN_DQN_V3(nn.Module):
    def __init__(self, game_dimension):
        super(CNN_DQN_V3, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(6400, 512)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(512, 4) 
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        #print("Shape after conv1:", x.shape)
        x = self.conv2(x)
        x = self.relu2(x)
        #print("Shape after conv2:", x.shape)
        x = self.flatten(x)
        #print("Shape after flatten:", x.shape)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        return x


class MLP_DQN(nn.Module):
    def __init__(self, game_dimension):
        super(MLP_DQN, self).__init__()
        self.lay1 = nn.Linear(game_dimension*game_dimension, 128)
        self.lay2 = nn.Linear(128, 256)
        self.lay3 = nn.Linear(256,128)
        self.lay4 = nn.Linear(128,64)
        self.lay5 = nn.Linear(64, 4)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.lay1(x))
        x = F.relu(self.lay2(x))
        x = F.relu(self.lay3(x))
        x = F.relu(self.lay4(x))
        return self.lay5(x)



class Experiece_Reply:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, state, action, next_state, reward):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = (state, action, next_state, reward)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def get_batched_state_act_reward_nextState(self, batch_size):
        data = self.sample(batch_size)
        state, action, next_state, reward = zip(*data) #transpose our data
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(1)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float32)
        next_state = torch.tensor(next_state,dtype=torch.float32).unsqueeze(1)
        return state,action,reward,next_state

    def __len__(self):
        return len(self.memory)


