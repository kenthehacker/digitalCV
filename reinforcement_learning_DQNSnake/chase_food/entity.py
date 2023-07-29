import numpy as np
class Blob:
    def __init__(self, max_size):
        self.x = np.random.randint(0,max_size)
        self.y = np.random.randint(0,max_size)
        self.max_size = max_size
    def __str__(self) -> str:
        return f"({self.x}), ({self.y})"
    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)
    def action(self, choice):
        if choice == 0:
            self.move(1,0)
        if choice == 1:
            self.move(-1,0)
        if choice == 2:
            self.move(0,1)
        if choice == 3:
            self.move(0,-1)
    def move(self, x, y):
        self.x += x
        self.y += y
        if self.x < 0:
            self.x = 0
        if self.x > self.max_size-1:
            self.x = self.max_size-1
        if self.y<0:
            self.y = 0
        if self.y>self.max_size-1:
            self.y = self.max_size-1
    def get_coord(self):
        return (self.x, self.y)
    

