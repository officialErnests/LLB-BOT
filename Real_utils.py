import math
class vector2D():
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "<"+str(self.x)+"; "+str(self.y)+">"
    def __repr__(self):
        return [self.x, self.y]
    def arr(self):
        return [self.x, self.y]
    def __sub__(self, vec2):
        return vector2D(self.x - vec2.x, self.y - vec2.y)
    def normalize(self):
        max = abs(self.x) + abs(self.y)
        if max == 0:
            return vector2D(0,0)
        return vector2D(self.x / max, self.y / max)
    def __add__(self, vec2):
        return vector2D(self.x + vec2.x, self.y + vec2.y)
    def __mul__(self, mul):
        return vector2D(self.x * mul, self.y * mul)
    def distance_till_intersection(self, borders, direction_vec):
        #hate math ;-;
        #did this on paper, can check #noob-dev for it ;-;
        x_distance = borders[0] - self.x
        y_distance = borders[1] - self.y
        
        #handles edge cases (so div by zero XD)
        if direction_vec.x == -1 and direction_vec.y == -1:
            return 0
        if direction_vec.x == -1:
            return y_distance
        if direction_vec.y == -1:
            return x_distance
        
        ratio_x = abs(x_distance / direction_vec.x)
        ratio_y = abs(y_distance / direction_vec.y)

        if ratio_x < ratio_y:
            # print(x_distance, y_distance, ratio_x, ratio_y, direction_vec.x, direction_vec.y)
            y_distance = (direction_vec.y * x_distance) / direction_vec.x
            # print(x_distance, y_distance)
            return x_distance
        return 0
        if x_distance < y_distance:
            print(x_distance, y_distance, direction_vec.y, direction_vec.x, vector2D(x_distance, direction_vec.y / direction_vec.x * x_distance).len())
            return vector2D(x_distance, direction_vec.y / direction_vec.x * x_distance).len()
        else:
            return vector2D(direction_vec.x /  direction_vec.y * y_distance, y_distance).len()
    def len(self):
        return math.sqrt(self.x**2 + self.y**2)