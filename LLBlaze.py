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
    def __init__(self, position : vector2D = vector2D(0,0), state : ball_states = ball_states.NEUTRAL):
        self.position = position
        self.state = state

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
        self.ball = ball_class(ball_pos)
        # TODO
        # for player in players:
        #     self.players.append(player)
    def update():
        self.game.stage.update_border(self.game.ball)
        self.game.stage.draw(start_img)