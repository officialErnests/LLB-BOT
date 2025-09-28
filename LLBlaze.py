from enum import Enum
from Real_utils import *
import cv2 as cv
import numpy as np

#enums
class ball_states(Enum):
    NEUTRAL = 0
    RED = 1
    BLUE = 2

# TODO
class charecters(Enum):
    Stitch = 0
    Switch = 1

#classes
class stage_class:
    top = 0
    left = 0
    bottom = 0
    right = 0
    def __init__(self, vector):
        self.reset(vector)
    
    def reset(self, vector):
        if isinstance(vector, vector2D):
            self.top = vector.y
            self.bottom = vector.y
            self.left = vector.x
            self.right = vector.x
        else:
            self.left = vector[0]
            self.top = vector[1]
            self.right = vector[2]
            self.bottom = vector[3]

    def update_border(self, ball):
        if ball.position.x > self.right:
            self.right = ball.position.x
        elif ball.position.x < self.left:
            self.left = ball.position.x

        if ball.position.y > self.bottom:
            self.bottom = ball.position.y
        elif ball.position.y < self.top:
            self.top = ball.position.y

    def draw(self, drawImg):
        cv.rectangle(drawImg,(self.left,self.top),(self.right,self.bottom),(0,255,0),3)
    
    def arr(self):
        return [self.left, self.top, self.right, self.bottom]

class ball_class:
    state : ball_states
    position : vector2D = None
    last_positions = []
    range = 0
    def __init__(self, position : vector2D = vector2D(0,0), state : ball_states = ball_states.NEUTRAL, position_history :int = 1):
        self.position = position
        self.state = state
        self.range = position_history -1
        self.last_positions = [position for n in range(position_history)]

    def update(self):
        self.last_positions.pop(0)
        self.last_positions.append(self.position)
    
    def draw(self, image):
            color = (100, 100, 0) if self.state == 1 else (0, 0, 100)
            # print(str(self.last_positions))
            #WHY
            cool_array = []
            for vec2D in self.last_positions:
                cool_array.append(vec2D.arr())
            pts = np.array(cool_array)
            image = cv.polylines(image, [pts], 
                      False, color, 2)
    
    def prediction(self, image, stage):
        color = (255, 255, 0) if self.state == 1 else (0, 0, 255)
        to_vector = ((self.last_positions[self.range - 1] - self.position).normalize()) * -1
        len, hit_wall = self.position.distance_till_intersection(stage.arr(), to_vector)
        print(hit_wall)
        idk = (self.position + to_vector * len)
        
        len2, hit_wall2 = idk.distance_till_intersection(stage.arr(), to_vector * hit_wall)
        idk2 = (idk + to_vector * len2 * hit_wall)
        pts = np.array([self.position.arr(), idk.arr(), idk2.arr()], dtype=np.int32)
        image = cv.polylines(image, [pts], 
                      False, color, 2)
        

class player_class:
    position : vector2D = None
    charecter = None
    def __init__(self, position, character):
        self.position = position
        self.character = character

class gamedata:
    stage : stage_class = None
    ball : ball_class = None
    players = []
    game_start = False
    def __init__(self, ball_pos : vector2D = vector2D(0,0), players = None):
        self.stage = stage_class(ball_pos)
        self.ball = ball_class(ball_pos, [], 3)
        # TODO
        # for player in players:
        #     self.players.append(player)
    def update(self, image):
        self.ball.update()
        if not self.game_start:
            self.game_start = True
            self.stage.reset(self.ball.position)
        self.stage.update_border(self.ball)

        #debug stuff
        self.stage.draw(image)
        self.ball.draw(image)

        self.ball.prediction(image, self.stage)