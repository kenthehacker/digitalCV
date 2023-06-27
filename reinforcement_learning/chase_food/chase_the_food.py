import numpy as np
import basic_rl_funcs as rl_lib
import pygame
import entity
import random
import pickle
import argparse
import matplotlib
#matplotlib.use("TkAgg")  # Or use "Agg" if you don't need an interactive window
import matplotlib.pyplot as plt


NUM_EPISODES = 25000
MAX_SIZE = 15
MOVE_PENALITY = 1
DEATH_PENALTY = -100
EAT_REWARD = 50
ITERS_PER_EPISODE = 200
epsilon = 1.0 #1-epsilon% takes normal action psilon% of the time it explores 
decay_rate = 0.0001
epsilon_min = 0.02
learning_rate = 0.1
discount_rate = 0.9
display_rate = 5000
disp_epsilon_rate = 100
pixel_size = 20

green=(0,255,0)
blue = (0,0,255)
red=(255,0,0)
black = (0,0,0)

'''
((agent-food) , (agent-enemy)) : [action0, action1, action2...]
'''
q_table = None
def init_qtable(NUM_POSSIBLE_ACTIONS):
    new_table = {}
    for a in range(-MAX_SIZE, MAX_SIZE):
        for b in range(-MAX_SIZE, MAX_SIZE):
            for c in range(-MAX_SIZE, MAX_SIZE):
                for d in range(-MAX_SIZE, MAX_SIZE):
                    action_table = []
                    for e in range(NUM_POSSIBLE_ACTIONS):
                        action_table.append(random.randint(int(-0.5*MAX_SIZE), int(0.5*MAX_SIZE)))
                    new_table[((a, b), (c, d))] = action_table
    return new_table

def get_squared_distance(agent_obj):
    return (agent_obj[0]**2) + (agent_obj[1]**2)

def get_reward(agent, food, enemy, old_state, new_state):
    if (agent.get_coord() == enemy.get_coord()):
        return DEATH_PENALTY
    if (agent.get_coord() == food.get_coord()):
        return EAT_REWARD
    old_food_dist = get_squared_distance(old_state[0])
    new_food_dist = get_squared_distance(new_state[0])
    if new_food_dist < old_food_dist:
        return MOVE_PENALITY
    return -1*MOVE_PENALITY
parser = argparse.ArgumentParser(description="Q table loader")
parser.add_argument("--input", type=str, help="type serialised q table name or no to make new q table")
args = parser.parse_args()
input_str = args.input
if input_str == 'no':
    NUM_POSSIBLE_ACTIONS = 4
    q_table = init_qtable(NUM_POSSIBLE_ACTIONS)    
else:
    with open(input_str, "rb") as f:
        q_table = pickle.load(f)


reward_list = []
for episode in range(NUM_EPISODES):
    agent = entity.Blob(MAX_SIZE)
    food = entity.Blob(MAX_SIZE)
    enemy = entity.Blob(MAX_SIZE)
    
    episode_reward_counter = 0
    
    clock = pygame.time.Clock()
    if episode%display_rate == 0:
        pygame.init()
        display = pygame.display.set_mode((MAX_SIZE*pixel_size,MAX_SIZE*pixel_size))
        display.fill(black)


    for iter in range(ITERS_PER_EPISODE):
        old_state = ((agent-food),(agent-enemy))
        action = -1
        if np.random.rand() <= epsilon:#explore
            action = np.random.randint(1,4)
        else:
            action = np.argmax(q_table[old_state])
        agent.action(action)
        old_qvalue = q_table[old_state][action]
        new_state = ((agent-food),(agent-enemy))
        iter_reward = get_reward(agent, food, enemy, old_state, new_state)
        
        pred_qvalue = np.max(q_table[new_state])

        new_qvalue = iter_reward
        if iter_reward != EAT_REWARD:
            new_qvalue = rl_lib.update_rule(q_table,learning_rate,old_state,new_state,action, iter_reward, discount_rate)
        
        q_table[old_state][action] = new_qvalue

        episode_reward_counter += iter_reward
        if episode%display_rate == 0:
            display.fill(black)
            pygame.draw.rect(display, red, [pixel_size*enemy.x, pixel_size*enemy.y,pixel_size,pixel_size])
            pygame.draw.rect(display, blue, [pixel_size*food.x, pixel_size*food.y,pixel_size,pixel_size])
            pygame.draw.rect(display, green, [pixel_size*agent.x, pixel_size*agent.y,pixel_size,pixel_size])
            pygame.display.update()
            pygame.event.pump()
            clock.tick(120)

        if iter_reward == EAT_REWARD or iter_reward == DEATH_PENALTY:
            break
        
        
    if episode%display_rate == 0:
        pygame.event.wait()
        pygame.quit()
    
    if episode%disp_epsilon_rate == 0:
        print(f"epsilon: {epsilon}")

    #epsilon decay controls exploration vs learning
    epsilon = max(np.exp(-decay_rate * episode), epsilon_min)
    reward_list.append(episode_reward_counter)

with open("my_dict.pickle", "wb") as f:
    pickle.dump(q_table, f)

moving_avg = np.convolve(reward_list, np.ones((display_rate,))/display_rate, mode='valid')
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel("Reward")
plt.xlabel("episode #")
plt.show()

