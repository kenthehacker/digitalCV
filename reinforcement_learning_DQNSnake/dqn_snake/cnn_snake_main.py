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
from collections import deque

tick_rate = 10
epsilon_decay_rate = 0.999992 
epsilon_min = 0.01
epsilon = 0.9970613219777701
original_epsilon = epsilon
temp_decay = 2.5*original_epsilon/game.num_episodes
input_size = 16
game_size = game.game_size 

def decay_epsilon(epsilon, epsilon_decay_rate, epsilon_min):
    return max(epsilon_min, epsilon * epsilon_decay_rate)
    #return max(epsilon, epsilon_min)

discount_rate = 0.99
model = dqn.Stacked_CNN(input_size)
target_model = dqn.Stacked_CNN(input_size)
model_path = "conv_model_params.pth"

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    target_model.load_state_dict(torch.load(model_path))
    print("Loaded "+model_path)

loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
display_rate = game.display_rate


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

def choose_action(state_stack):
    if np.random.rand() < epsilon:
        return np.random.randint(1,4)
    state_stack_tensor = torch.tensor(state_stack, dtype=torch.float32).unsqueeze(0)
    #print("PRINTING TENSOR")
    #print(model(state_stack_tensor))
    return torch.argmax(model(state_stack_tensor))

def take_action(action, snake_bodies, food):
    head = snake_bodies[-1]
    new_location = head.theoretical_action(action)
    if new_location == food.get_coord():
        new_head = Entity.Entity(game_size,new_location[0], new_location[1])
        snake_bodies.append(new_head)
        return True
    tail = snake_bodies.pop(0)
    #print("TAIL" + str(tail))
    #print(f"NEW LOCATION {new_location} {action}")
    tail.x,tail.y = new_location
    snake_bodies.append(tail)
    return False


training = True
reward_list = []
clock = pygame.time.Clock()
target_update_rate = 100
max_episode = 0
frame_count = 1
frame_skip = 3
n_step = 4
frame_deque = deque([np.zeros((game_size, game_size)) for _ in range(3)], maxlen=3)


try:
    experience_replay = dqn.Multi_Step_Exp_Replay(10000, n_step, discount_rate)
    experience_replay_batch_size = 128
    reward_list = []
    pygame.init()
    display = pygame.display.set_mode((game_size * game.pixel_size, game_size * game.pixel_size))
    display.fill(game.black)
    
    for episode in range(game.num_episodes):
        if episode!=0 and episode%target_update_rate==0:
            target_model.load_state_dict(model.state_dict())
        
        food = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
        head = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
        while food.get_coord() == head.get_coord():
            food = Entity.Entity(game_size, np.random.randint(0,game_size), np.random.randint(0,game_size))
        snake_bodies = [head]
        episode_reward = 0
        
        for iter in range(game.iters_per_ep):    
            old_state = get_cnn_state(snake_bodies, food)
            old_state_stack = np.array(frame_deque)
            old_head_location = snake_bodies[-1].get_coord()
            #action = choose_action(old_state)
            action = choose_action(old_state_stack)

            ate_apple = take_action(action, snake_bodies, food)
            
            if iter%target_update_rate == 0: #target model update 
                target_model.load_state_dict(model.state_dict())

            iter_reward = f.get_reward(snake_bodies, food, old_head_location)
            
            if ate_apple:
                food = Entity.Entity(game.game_size, np.random.randint(0,game.game_size),np.random.randint(0,game.game_size))
                get_new_loc = True
                while get_new_loc:
                    continue_loop = False
                    for body in snake_bodies:
                        if body.get_coord() == food.get_coord():
                            continue_loop = True
                            food = Entity.Entity(game.game_size, np.random.randint(0,game.game_size),np.random.randint(0,game.game_size))
                            break
                    get_new_loc = continue_loop


            new_state = get_cnn_state(snake_bodies, food)
            frame_deque.append(new_state)
            new_state_stack = np.array(frame_deque)
            episode_reward += iter_reward

            #experience_replay.push(old_state,action,new_state,iter_reward)
            experience_replay.push(np.array(frame_deque), action, np.array(frame_deque), iter_reward)
            optimizer.zero_grad()

            if (len(experience_replay) > experience_replay_batch_size):
                exp_state,exp_action,exp_reward,exp_next_state = experience_replay.get_batched_state_act_reward_nextState(experience_replay_batch_size)
                exp_old_q_value = model(exp_state).gather(1, exp_action.unsqueeze(-1)).squeeze(-1) 
                exp_max_new_q_value = model(exp_next_state).max(1)[0].detach()
                exp_predicted_q_value = exp_reward + (discount_rate * exp_max_new_q_value)
                loss = loss_fn(exp_old_q_value, exp_predicted_q_value)
            else:
                old_state_tensor = torch.tensor(old_state_stack, dtype=torch.float32).unsqueeze(0)
                new_state_tensor = torch.tensor(new_state_stack, dtype=torch.float32).unsqueeze(0)
                # print(f"old_state_tensor shape: {old_state_tensor.shape}")
                # print(f"new_state_tensor shape: {new_state_tensor.shape}")
                old_q_value = model(old_state_tensor)[0, action].unsqueeze(0)
                max_new_q_value = target_model(new_state_tensor).max().item()

                if (episode%1000 == 0):
                    print("EPISODE: "+str(episode)+" ITERATION: "+str(iter))
                    #print(model(old_state_tensor))
                    print("EPSILON: "+str(epsilon))
                    print("rewards: "+str(reward_list[-10:]))

                predicted_q_value = torch.tensor([iter_reward + discount_rate * max_new_q_value], device=old_q_value.device)
                loss = loss_fn(old_q_value, predicted_q_value)

            
            loss.backward()
            optimizer.step()


            if episode%display_rate == 0:
                display.fill(game.black)
                for body in snake_bodies:
                    pygame.draw.rect(display, game.blue, [game.pixel_size * body.x, game.pixel_size*body.y, game.pixel_size, game.pixel_size])
                pygame.draw.rect(display, game.red, [game.pixel_size*food.x, game.pixel_size*food.y, game.pixel_size, game.pixel_size])
                pygame.display.update()
                pygame.event.pump()
                if training:
                    clock.tick(0)
                else:
                    clock.tick(15)

            if iter_reward == game.death_penalty:
                break
        if episode%50 == 0:
            print(f"Episode reward: {episode_reward}")
        if episode%display_rate == 0:
            pygame.quit()
        if training:
            epsilon = decay_epsilon(epsilon, epsilon_decay_rate, epsilon_min)
            if iter % 20 == 0:
                print("epsilon now: "+ str(epsilon))
        
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

pygame.quit()



