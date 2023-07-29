import matplotlib.pyplot as plt
import numpy as np 

steps = 10000
epsilon = 0.1
alpha = 0.1
num_arms = 10
standard_dev = 0.1
q_star = np.zeros(num_arms)

def epsilon_greedy_choice(Q):
    if np.random.rand() < epsilon:
        return np.random.randint(0,num_arms)
    else:
        return np.argmax(Q)

def update_exp_weighted_avg(Q, H, a, reward):
    H[a] = alpha * (reward - Q[a]) + (1-alpha) * H[a]
    Q[a] = H[a] + Q[a] 
    return Q, H 

def update_sample_average(Q,N,a,reward):
    Q[a] =Q[a] + alpha*(reward - Q[a])
    N[a] =N[a] + 1
    return Q, N 

def take_random_walk():
    for i in range(len(q_star)):
        q_star[i] += np.random.normal(0, standard_dev)

def reward(action):
    return np.random.normal(q_star[action],1)

def bandit_exp(num_episodes, num_steps_per_ep):
    avg_reward_sa = np.zeros(num_steps_per_ep)
    pct_optimal_sa = np.zeros(num_steps_per_ep)
    avg_reward_era = np.zeros(num_steps_per_ep)
    pct_optimal_era = np.zeros(num_steps_per_ep)

    for ep in range(num_episodes):
        Q_exp_w_avg = np.zeros(num_arms)
        Q_sample_avg = np.zeros(num_arms)
        N = np.zeros(num_arms)
        H = np.zeros(num_arms)
        for step in range(num_steps_per_ep):
            exp_w_action = epsilon_greedy_choice(Q_exp_w_avg)
            exp_w_reward = reward(exp_w_action)
            Q_exp_w_avg, H = update_exp_weighted_avg(Q_exp_w_avg,H,exp_w_action,exp_w_reward)

            samp_avg_action = epsilon_greedy_choice(Q_sample_avg)
            samp_avg_reward = reward(samp_avg_action)
            
            avg_reward_sa[step] += samp_avg_reward / num_episodes
            avg_reward_era[step] += exp_w_reward / num_episodes

            Q_sample_avg, N = update_sample_average(Q_sample_avg, N, samp_avg_action, samp_avg_reward)

            if np.argmax(q_star) == exp_w_action:
                pct_optimal_era[step] += 100/num_episodes
            
            if np.argmax(q_star) == samp_avg_action:
                pct_optimal_sa[step] += 100/num_episodes
            take_random_walk()
            
    plt.figure(figsize=(12, 4))
    plt.plot(pct_optimal_sa, label='Sample-average')
    plt.plot(pct_optimal_era, label='Exponential recency-weighted average')
    plt.xlabel('Steps')
    plt.ylabel('% Optimal action')
    plt.legend()
    plt.show()

bandit_exp(50,1000)

            

    