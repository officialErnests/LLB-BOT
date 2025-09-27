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