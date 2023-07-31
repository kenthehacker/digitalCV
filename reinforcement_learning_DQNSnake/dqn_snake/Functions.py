import Game_frame as game

def get_squared_distance(a,b):
    return ((a.x-b.x)**2 + (a.y-b.y)**2)

def get_cnn_state(snake_body, food):
    grid = [[0] * game.game_size for _ in range(game.game_size)]
    for body in snake_body:
        if body.is_out_of_bounds() == False:
            grid[body.x][body.y] = 1
    head = snake_body[-1]
    if head.is_out_of_bounds() == False:
        grid[head.x][head.y] = 2
    grid[food.x][food.y] = 3
    return grid

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
