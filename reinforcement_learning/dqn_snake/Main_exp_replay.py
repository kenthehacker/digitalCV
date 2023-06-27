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

epsilon_decay_rate = 0.00005
epsilon_min = 0.02
epsilon = 1
target_update_rate = 1000
target_update_episode_rate = 500

discount_rate = 0.85
model = dqn.CNN_DQN_V3(game.game_size)
target_model = dqn.CNN_DQN_V3(game.game_size)
model_path = "model_parameters_no_discount.pth"

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    target_model.load_state_dict(torch.load(model_path))
    print("Loaded "+model_path)

loss_fn = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)


display_rate = game.display_rate

#function 
def get_cnn_state(snake_body, food):
    grid = [[0] * game.game_size for _ in range(game.game_size)]
    for body in snake_body:
        if body.is_out_of_bounds() == False:
            grid[body.x][body.y] = 1
    grid[food.x][food.y] = 2
    return grid
#function

def choose_action(state):
    #v1 state tensor:
    #state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)

    #v2 state tensor:
    state_tensor = torch.tensor(np.array(state)).unsqueeze(0).unsqueeze(0).float()
    if np.random.rand() <= epsilon:
        return np.random.randint(1,4)
    else:
        #print("CNN RESULT")
        with torch.no_grad():
            q_values = model(state_tensor)
            action = torch.argmax(q_values)
            return action

def take_action(action, snake_body, food):
    if snake_body[-1].get_coord() == food.get_coord():
        new_location = snake_body[-1].theoretical_action(action)
        tail = snake_body[0]
        new_head = Entity.Entity(game.game_size, new_location[0], new_location[1])
        snake_body.append(new_head)
        return True
    else:
        new_location = snake_body[-1].theoretical_action(action)
        tail = snake_body.pop(0)
        tail.x, tail.y = new_location
        snake_body.append(tail)
        return False

def get_reward(snake_body, food, old_location):
    def is_dead():
        head = snake_body[-1]
        if head.is_out_of_bounds():
            return True
        for body in snake_body[:-1]:
            if body.get_coord() == head.get_coord():
                return True
        return False
    if is_dead():
        return game.death_penalty
    head = snake_body[-1]
    if head.get_coord() == food.get_coord():
        return game.eat_reward
    old_sq_distance = (old_location[0] - food.x)**2 + (old_location[1] - food.y)**2
    new_sq_distance = (head.x - food.x)**2 + (head.y - food.y)**2
    if old_sq_distance > new_sq_distance:
        return game.closer_reward
    return game.further_penalty

def decay_epsilon(epsilon, decay_rate, min_epsilon):
    epsilon = max(1 / (1 + epsilon_decay_rate * episode), epsilon_min)
    return max(epsilon, min_epsilon)

max_episode = 0
training = True
################################################
try:
    reward_list = []
    experience_replay = dqn.Experiece_Reply(10000)
    experience_replay_batch_size = 128

    for episode in range(game.num_episodes):
        max_episode = episode
        food = Entity.Entity(game.game_size, np.random.randint(0,game.game_size),np.random.randint(0,game.game_size))
        head = Entity.Entity(game.game_size, np.random.randint(0,game.game_size),np.random.randint(0,game.game_size))
        snake_body = [head]
        speed = (0,1)
        episode_reward_count = 0

        if episode % display_rate == 0 :
            clock = pygame.time.Clock()
            pygame.init()
            display = pygame.display.set_mode((game.game_size * game.pixel_size, game.game_size * game.pixel_size))
            display.fill(game.black)


        if episode!=0 and episode%target_update_episode_rate == 0:  #target model update 
            target_model.load_state_dict(model.state_dict())

        for iter in range(game.iters_per_ep):    
            old_state = get_cnn_state(snake_body, food)
            old_head_location = snake_body[-1].get_coord()
            action = choose_action(old_state)
                    
            ate_apple = take_action(action, snake_body, food)

            if ate_apple:
                food = Entity.Entity(game.game_size, np.random.randint(0,game.game_size),np.random.randint(0,game.game_size))
                get_new_loc = True
                while get_new_loc:
                    continue_loop = False
                    for body in snake_body:
                        if body.get_coord() == food.get_coord():
                            continue_loop = True
                            food = Entity.Entity(game.game_size, np.random.randint(0,game.game_size),np.random.randint(0,game.game_size))
                            break
                    get_new_loc = continue_loop
                #check for bad replacement

            if iter%target_update_rate == 0: #target model update 
                target_model.load_state_dict(model.state_dict())

            iter_reward = get_reward(snake_body, food, old_head_location)
            new_state = get_cnn_state(snake_body, food)
            episode_reward_count += iter_reward
            # Computing loss values:

            experience_replay.push(old_state,action,new_state,iter_reward)
            if (len(experience_replay) > experience_replay_batch_size):
                exp_state,exp_action,exp_reward,exp_next_state = experience_replay.get_batched_state_act_reward_nextState(experience_replay_batch_size)
                exp_old_q_value = model(exp_state).gather(1, exp_action.unsqueeze(-1)).squeeze(-1) #.gather() chooses q-values based on actions chosen
                exp_max_new_q_value = model(exp_next_state).max(1)[0].detach()
                exp_predicted_q_value = exp_reward + (discount_rate * exp_max_new_q_value)
                loss = loss_fn(exp_old_q_value, exp_predicted_q_value)
            else:
                optimizer.zero_grad()
                '''
                #V1 Code:
                old_state_tensor = torch.tensor(old_state, dtype=torch.float32).unsqueeze(0) 
                new_state_tensor = torch.tensor(new_state, dtype=torch.float32).unsqueeze(0)
                '''
                '''
                #MLP Code:
                old_state_tensor = torch.tensor(old_state, dtype=torch.float32).unsqueeze(0) 
                new_state_tensor = torch.tensor(new_state, dtype=torch.float32).unsqueeze(0)
                '''
                #CNN V3:
                old_state_tensor = torch.tensor(np.array(old_state)).unsqueeze(0).unsqueeze(0).float()
                new_state_tensor = torch.tensor(np.array(new_state)).unsqueeze(0).unsqueeze(0).float()
                
                ##########

                '''
                #V1 Code:
                old_q_value = model(old_state_tensor)[action].unsqueeze(0)
                max_new_q_value = target_model(new_state_tensor).max().item()
                '''
                #MLP Code:
                '''
                old_q_value = model(old_state_tensor)[0, action].unsqueeze(0)
                max_new_q_value = target_model(new_state_tensor).max().item()
                '''
                #CNN V3:
                old_q_value = model(old_state_tensor)
                max_new_q_value = target_model(new_state_tensor).max().item()

                if (episode%1000 == 0):
                    print("EPISODE: "+str(episode)+" ITERATION: "+str(iter))
                    print(model(old_state_tensor))
                    print("EPSILON: "+str(epsilon))
                    print("rewards: "+str(reward_list[-10:]))
                
                predicted_q_value = torch.tensor([iter_reward + discount_rate * max_new_q_value], device=old_q_value.device)
                loss = loss_fn(old_q_value, predicted_q_value)

            
            loss.backward()
            optimizer.step()


            if episode%display_rate == 0:
                display.fill(game.black)
                for body in snake_body:
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
        if episode%display_rate == 0:
            pygame.quit()
        if training:
            #epsilon = max(np.exp(-epsilon_decay_rate * episode), epsilon_min)
            epsilon = decay_epsilon(epsilon, epsilon_decay_rate, epsilon_min)
            if iter % 20 == 0:
                print("epsilon now: "+ str(epsilon))
        
        reward_list.append(episode_reward_count)
except KeyboardInterrupt:
    print("Keyboard interrupt saving model param")
finally:
    print(reward_list)
    torch.save(model.state_dict(), model_path)


print("REACHED EPISODE "+str(episode)+" EPSILON "+str(epsilon))

sub_reward_list = reward_list[-500:]
fig, ax = plt.subplots()
ax.plot(sub_reward_list)
plt.tight_layout()
plt.show()




