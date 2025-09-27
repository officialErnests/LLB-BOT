from enum import Enum
from Real_utils import *
import cv2 as cv

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

class ball_class:
    state : ball_states
    position : vector2D = None
    last_positions = []

    def __init__(self, position : vector2D = vector2D(0,0), state : ball_states = ball_states.NEUTRAL, position_history :int = 1):
        self.position = position
        self.state = state
        self.last_positions = [position for n in range(position_history)]
        print(self.last_positions[2])

    def update(self):
        self.last_positions.pop(0)
        self.last_positions.append(self.position)
        print(self.last_positions)
    
    def draw(self, image):
            color = (255, 255, 0) if self.state == 1 else (0, 0, 255)
            cv.circle(image, (self.last_positions[0].x, self.last_positions[0].y), 20, (255, 255, 255), -1)
            cv.circle(image, (self.last_positions[1].x, self.last_positions[1].y), 10, (0, 0, 0), -1)
            cv.circle(image, (self.last_positions[2].x, self.last_positions[2].y), 5, color, -1)

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
        self.stage.update_border(self.ball)
        self.stage.draw(image)
        self.ball.draw(image)