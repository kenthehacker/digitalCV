import numpy as np
SIZE = 10
q_table = {}
for i in range(-SIZE+1, SIZE):
    for ii in range(-SIZE+1, SIZE):
        for iii in range(-SIZE+1, SIZE):
                for iiii in range(-SIZE+1, SIZE):
                    q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]
print(q_table[((9, 8), (1, 8))])