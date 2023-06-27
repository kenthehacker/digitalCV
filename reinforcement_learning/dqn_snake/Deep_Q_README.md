## Walk through


## How we represent the state
- We can either have the N x N grid itself be a state where we assign values
to the cell if we have a snake body it's a 0 snake head would be 1, food is a 2 and
3 for an empty cell. This would be really easy and we could use CNN 

- If we care about the large dimension of the board we can instead represent
the state of the game in a 1D array which contains info about the head's relative
position to the food and any obstacles


## Interesting Errors I've hit
I originally had an issue where the snake's rewards over time on average remained flat even after i trained it for approximately 5 million iterations
What I next experimented with was using "experience replay" 


https://towardsdatascience.com/deep-q-network-dqn-ii-b6bf911b6b2c
