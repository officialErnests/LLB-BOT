from enum import Enum
from Real_utils import *
import cv2 as cv
import numpy as np
import math

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
    range = 0
    ball_speed = 0
    previous_radiants : nbArray = None
    prev_rad_size = 20
    ball_rad = 0
    ball_direction = 0
    back_dir = False
    init_dir = 2
    last_positions = vector2D(0,0)
    prew_speed = []
    def __init__(self, position : vector2D = vector2D(0,0), state : ball_states = ball_states.NEUTRAL, position_history :int = 1):
        self.position = position
        self.state = state
        self.range = position_history
        self.prew_speed = [0 for n in range(position_history)]

    def reset_rad(self, rads):
        self.previous_radiants = nbArray([rads for n in range(self.prev_rad_size)])

    def update(self, delta):
        self.prew_speed.pop(0)
        self.prew_speed.append(self.position.distance_to(self.last_positions) / delta)

        #Get's the ball speed
        temp_speed = 0
        for pos in self.prew_speed:
            temp_speed += (pos / self.range)
        
        self.ball_speed = self.ball_speed * 0.5 + temp_speed * 0.5
        # print(self.ball_speed)

        #Get balls radiant
        rads = self.position.rad_to(self.last_positions)
        norm_rads_uncaped = ((rads - (math.pi / 2)) % math.pi) - (math.pi / 2)
        norm_rads = abs(norm_rads_uncaped)


        if self.init_dir > 0:
            self.init_dir -= 1
            if self.init_dir == 0:
                self.reset_rad(norm_rads)
            else:
                return
        
        self.previous_radiants.pop(0)
        self.previous_radiants.append(norm_rads)
        avg, if_outliner = self.previous_radiants.denoised_array(0.1, norm_rads)
        self.ball_rad = avg
        self.back_dir = norm_rads_uncaped < 0
        if not if_outliner:
            self.ball_direction = math.floor((rads*2) / math.pi)/2
            if norm_rads_uncaped < 0:
                self.ball_direction = self.ball_direction+0.5
        
        self.last_positions = self.position
            
    
    def draw(self, image):
            print("Depricated func ball.draw()")
            return #DEPRICATED BC CHANGES ON HOW THE last_positions WORKS XD
            color = (100, 100, 0) if self.state == 1 else (0, 0, 100)
            cool_array = []
            for vec2D in self.last_positions:
                cool_array.append(last_positions)
            pts = np.array(cool_array)
            image = cv.polylines(image, [pts], 
                      False, color, 2)
    
    def prediction(self, image, stage, line_amount):
        color = (255, 255, 0) if self.state == 1 else (0, 0, 255)
        
        positions = [self.position.arr()]
        start = self.position
        direction = self.get_directional_vector()
        for n in range(line_amount):
            len, hit_wall = start.distance_till_intersection(stage.arr(), direction)
            result = (start + direction * len)
            positions.append(result.arr())
            direction *= hit_wall
            start = result

        pts = np.array([positions], dtype=np.int64)
        image = cv.polylines(image, [pts], 
                      False, color, 2)
    
    def get_directional_vector(self):
        direction = vector2D(0,0)
        if self.back_dir:
            direction.vector_from_rad(-self.ball_rad + self.ball_direction * math.pi + math.pi)
        else:
            direction.vector_from_rad(self.ball_rad + self.ball_direction * math.pi + math.pi)
        direction = direction.normalize()
        return direction
        

class player_class:
    position : vector2D = None
    charecter = None
    speed = 0
    prev_direction = 0
    next_pos = 0
    expected_speed = []
    def __init__(self, position, character):
        self.position = position
        self.character = character
        self.expected_speed = [0 for n in range(10)]

class gamedata:
    stage : stage_class = None
    ball : ball_class = None
    players = []
    game_start = False
    hit_amount = 0
    prev_hits = []
    def __init__(self, ball_pos : vector2D = vector2D(0,0), players = None):
        self.stage = stage_class(ball_pos)
        self.ball = ball_class(ball_pos, [], 4)
        self.players.append(player_class(vector2D(0,0), "RAPTOR"))
        # TODO
        # for player in players:
        #     self.players.append(player)
    def update(self, image, delta):
        if self.hit_amount > 0:
            self.prev_hits.append(self.hit_amount)
            estimate = 0
            for x in range(len(self.prev_hits)):
                estimate += self.prev_hits[x]
            estimate /= len(self.prev_hits)
            self.stage.draw(image)
            # self.ball.draw(image)
            self.ball.prediction(image, self.stage, 10)
            return_inputs = {
                "walk_direction" : 0,
                "jump" : False,
                "Hit" : False,
                "Hit_dist" : -1,
            }
            return return_inputs
        elif len(self.prev_hits) > 0:
            self.prev_hits = []

        self.ball.update(delta)
        if not self.game_start:
            self.game_start = True
            self.stage.reset(self.ball.position)
        self.stage.update_border(self.ball)

        #debug stuff
        self.stage.draw(image)
        # self.ball.draw(image)

        self.ball.prediction(image, self.stage, 10)
        
        #sends player input
        return_inputs = {
            "jump" : self.players[0].position.y > self.ball.position.y,
            "Hit" : self.players[0].position.distance_to(self.ball.position) < 200,
            "Hit_dist" : self.players[0].position.distance_to(self.ball.position),
        }
        return return_inputs