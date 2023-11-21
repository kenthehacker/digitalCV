## chase_food
This is where I experimented the first time a simple q-learning programming where a blob attempts to chase another blob. 
It employed q learning to guess and check while learning "strategies" along the way to increase reward and minimise punishment

## dqn_snake
This folder also contains a readme that explains the process.
Instead of a regular vanilla RL program, I had to tweak the algorithm. For example, the snake head needs to 'know' which direction
it's currently moving in
Furthermore, as n increases in an n x n board the memory complexity blows up exponentially. Thus, I can't memoize every single situation
neural nets needs to be implemented to predict the q-value instead of out-right memoizing it
To make it all work, replay buffer and a target neural net was employed.
