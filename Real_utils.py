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
        if isinstance(mul, vector2D):
            return vector2D(self.x * mul.x, self.y * mul.y)
        else:
            return vector2D(self.x * mul, self.y * mul)
    def distance_till_intersection(self, borders, direction_vec):
        x_distance = borders[0] - self.x if direction_vec.x < 0 else -1 if direction_vec.x == 0 else borders[2] - self.x
        y_distance = borders[1] - self.y if direction_vec.y < 0 else -1 if direction_vec.y == 0 else borders[3] - self.y

        if direction_vec.x == 0 and direction_vec.y == 0:
            return 0, 0
        if direction_vec.x == 0:
            return abs(y_distance), vector2D(1, -1)
        if direction_vec.y == 0:
            return abs(x_distance), vector2D(-1, 1)
        
        ratio_x = x_distance / direction_vec.x
        ratio_y = y_distance / direction_vec.y

        if ratio_x < ratio_y:
            y_distance = (direction_vec.y * x_distance) / direction_vec.x
            return vector2D(x_distance, y_distance).magnitude(), vector2D(-1, 1)
        else:
            x_distance = (direction_vec.x * y_distance) / direction_vec.y
            return vector2D(x_distance, y_distance).magnitude(), vector2D(1, -1)
    def magnitude(self):
        return abs(self.x) + abs(self.y)
    def len(self):
        return math.sqrt(self.x**2 + self.y**2)
    def distance_to(self, vec2d):
        return (self - vec2d).len()
    def rad_to(self, vec2d):
        return math.atan2(vec2d.x - self.x, vec2d.y - self.y)
    def vector_from_rad(self, rad):
        self.x = math.sin(rad)
        self.y = math.cos(rad)