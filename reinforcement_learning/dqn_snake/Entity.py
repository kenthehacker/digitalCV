class Entity:
    def __init__(self, max_size, x, y):
        self.x = x
        self.y = y
        self.max_size = max_size
    def __str__(self) -> str:
        return f"({self.x}), ({self.y})"
    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)
    def action(self, choice):
        if choice == 0:
            self.move(1,0)
            return (1,0)
        if choice == 1:
            self.move(-1,0)
            return (-1,0)
        if choice == 2:
            self.move(0,1)
            return (0,1)
        if choice == 3:
            self.move(0,-1)
            return (0,-1)
    def theoretical_action(self,choice):
        if choice == 0:
            return (self.x + 1, self.y)
        if choice == 1:
            return (self.x - 1, self.y)
        if choice == 2:
            return (self.x, self.y + 1)
        if choice == 3:
            return (self.x, self.y - 1)
    def move(self, x, y):
        self.x += x
        self.y += y
    def get_coord(self):
        return (self.x, self.y)
    def is_out_of_bounds(self):
        return not (self.x >= 0 and self.x < self.max_size and self.y >= 0 and self.y < self.max_size)
    

