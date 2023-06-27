import numpy as np
def update_rule(q_table, lr, old_state, new_state, action, reward, discount_rate):
    current_qvalue = q_table[old_state][action]
    max_future_qvalue = np.max(q_table[new_state])
    return (1-lr)*(current_qvalue + lr*(reward + discount_rate * max_future_qvalue))
    #q(s,a) = (1-lr)(current_q_value+lr(reward+discount_rate * max_future_q_value)




