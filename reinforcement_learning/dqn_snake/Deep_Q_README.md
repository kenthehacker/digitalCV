# Howdie
Howdie! chase_food is from following a sent dex tutorial where I learned about q learning w/o incorporating deep learning
Now I've moved onto learning about DQN. I've invested a bit of time reading relevant parts of Sutton's textbook
The idea is to use convolutional NN with q learning to train a snake. Before finishing that part,
I've also uploaded my code where I've trained snake using a regular linear NN where the state is represented by a head-relative array

## How We Represent The State
- We can either have the N x N grid itself be a state where we assign values
to the cell if we have a snake body it's a 0 snake head would be 1, food is a 2 and
3 for an empty cell. This would be really easy and we could use CNN 

- If we care about the large dimension of the board we can instead represent
the state of the game in a 1D array which contains info about the head's relative
position to the food and any obstacles

## General Algorithm:
- I have a regular model and a trailing model. The regular model updates with each iteration but the trailing model
copies the regular model after k-iterations the reason is that we don't want to "chase our own tail," thus I've implemented a replay buffer
for each episode:
    for each iteration in an episode:
        save old state
        pick an action
        now save new state
        obtain the reward after taking action a
        if replay_buffer size > 128:
            sample from replay buffer
            calculate q values based on trailing nn and update the regular NN
            
            if its k iteration copy params from model into trailing model


## Interesting Errors I've hit
I originally had an issue where the snake's rewards over time on average remained flat even after i trained it for approximately 5
million iterations for the CNN

I believe it's because the NN does not know which direction we're going when we submit the n x n grid as the input
The Volodymyr Mnih 2013 Atari paper mentioned that they fed k=3-4 states into the NN which indirectly encodes direction.
I've also been constantly been using 1 input channel and the Atari paper uses 4 input channels. Perhaps using greyscale isn't sufficient




https://towardsdatascience.com/deep-q-network-dqn-ii-b6bf911b6b2c
https://www.youtube.com/watch?v=KuXjwB4LzSA
