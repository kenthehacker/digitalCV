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
epsilon = 1.0

discount_rate = 0.85
model = dqn.CNN_DQN(game.game_size)
model_path = "model_parameters_no_discount.pth"
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
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
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    if np.random.rand() <= epsilon:
        return np.random.randint(1,4)
    else:
        #print("CNN RESULT")
        with torch.no_grad():
            q_values = model(state_tensor)
            #print(q_values)
            #actions = torch.argmax(q_values, dim=1)
            #print(actions)
            #action = actions[0].item()
            action = torch.argmax(q_values)
            return action

def take_action(action, snake_body, food):
    #print("ACTION TAKEN: "+str(action))
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


################################################
try:
    reward_list = []
    for episode in range(game.num_episodes):
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

            #MUST CHANGE FOOD LOCATION and increment the size of the blob

            iter_reward = get_reward(snake_body, food, old_head_location)
            new_state = get_cnn_state(snake_body, food)
            episode_reward_count += iter_reward



            optimizer.zero_grad()
            old_state_tensor = torch.tensor(old_state, dtype=torch.float32).unsqueeze(0) #add extra dimension
            new_state_tensor = torch.tensor(new_state, dtype=torch.float32).unsqueeze(0)
            
            if (episode%500 == 0):
                print("EPISODE: "+str(episode)+" ITERATION: "+str(iter))
                print(model(old_state_tensor))
                print("EPSILON: "+str(epsilon))
                print("rewards: "+str(reward_list[-10:]))
            #old_q_value = model(old_state_tensor)[0][action]
            old_q_value = model(old_state_tensor)[action].unsqueeze(0)
            max_new_q_value = model(new_state_tensor).max().item()

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
                clock.tick(30)

            if iter_reward == game.death_penalty:
                break
        if episode%display_rate == 0:
            pygame.event.wait()
            pygame.quit()
        epsilon = max(np.exp(-epsilon_decay_rate * episode), epsilon_min)
        
        reward_list.append(episode_reward_count)
except KeyboardInterrupt:
    print("Keyboard interrupt saving model param")
finally:
    print(reward_list)
    torch.save(model.state_dict(), model_path)



sub_reward_list = reward_list[-500:]
fig, ax = plt.subplots()
ax.plot(sub_reward_list)
plt.tight_layout()
plt.show()




