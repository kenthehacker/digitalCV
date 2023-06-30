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
tick_rate = 10
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

discount_rate = 0.99
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
max_episode = 0
clock = pygame.tick.Clock()
target_update_rate = 100
try:
    experience_replay = dqn.Experiece_Reply(10000)
    experience_replay_batch = 128
    for episode in range(game.num_episodes):
        if episode % display_rate == 0:
            pygame.init()
            display = pygame.display.set_mode((game_size * game.pixel_size, game_size * game.pixel_size))
            display.fill(game.black)
        if episode!=0 and episode%target_update_rate == 0:
            target_model.load_state_dict(model.state_dict)

        max_episode = episode
        food = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
        head = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
        while food.get_coord() == head.get_coord():
            food = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
        snake_bodies = [head]
        speed = (1,0)
        episode_reward = 0

        for iter in range(game.iters_per_ep):
            old_state = get_state_linear(snake_bodies, food, speed)
            old_head_location = snake_bodies[-1].get_coord()
            action = choose_action(old_state)
            speed = snake_bodies[-1].update_speed(action)

            snake_ate = take_action(action)
            iter_reward = f.get_reward(snake_bodies, food, old_head_location)
            episode_reward += iter_reward
            if snake_ate:
                food = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
                while food.get_coord() in [body.get_coord() for body in snake_bodies]:
                    food = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
            new_state = get_state_linear(snake_bodies, food, speed)
        
            # experience_replay.push(old_state, action, new_state, iter_reward)
            optimizer.zero_grad()
            # if len(experience_replay) > experience_replay_batch:
            #     pass
            # else:
            #     old_state_tensor = torch.tensor(old_state, dtype=torch.float)
            #     new_state_tensor = torch.tensor(new_state, dtype=torch.float)
            #im using the wrong replay buffer for multi step learning



            
            optimizer.step()
            #loss.backward()

            if episode%display_rate == 0:
                display.fill(game.black)
                for body in snake_bodies:
                    pygame.draw.rect(display, game.blue, [game.pixel_size * body.x, game.pixel_size*body.y, game.pixel_size, game.pixel_size])
                pygame.draw.rect(display, game.red, [game.pixel_size*food.x, game.pixel_size*food.y, game.pixel_size, game.pixel_size])
                pygame.display.update()
                if training:
                    clock.tick(5)
                else:
                    clock.tick(15)

            if iter_reward == game.death_penalty:
                break

        if episode%display_rate == 0:
            pygame.quit()
        if episode%50 == 0:
            print("Epsilon: "+str(epsilon))
        reward_list.append(episode_reward)

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



