import Game_frame as game

def get_squared_distance(a,b):
    return ((a.x-b.x)**2 + (a.y-b.y)**2)

def get_cnn_state(snake_body, food):
    grid = [[0] * game.game_size for _ in range(game.game_size)]
    for body in snake_body:
        grid[body.x][body.y] = 1
    grid[food.x][food.y] = 2
    return grid

def get_reward(snake_body, food, old_state, new_state):
    return 0
