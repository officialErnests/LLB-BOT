from enum import Enum
from Real_utils import *
import cv2 as cv
import numpy as np
import math

#Holds all information about stage
class stage_class:
    top = 0
    left = 0
    bottom = 0
    right = 0
    #Sets stage to size (takes in vector2d or size 4 array)
    def __init__(self, size):
        self.reset(size)
    #Sets stage to size position with scale 0 0 or other rect (size 4 array)
    def reset(self, size):
        if isinstance(size, vector2D):
            self.top = size.y
            self.bottom = size.y
            self.left = size.x
            self.right = size.x
        else:
            self.left = size[0]
            self.top = size[1]
            self.right = size[2]
            self.bottom = size[3]

    #Extends borders based on given position vector
    def update_border(self, position):
        if position.position.x > self.right:
            self.right = position.position.x
        elif position.position.x < self.left:
            self.left = position.position.x

        if position.position.y > self.bottom:
            self.bottom = position.position.y
        elif position.position.y < self.top:
            self.top = position.position.y

    #Draws itself
    def draw(self, drawImg):
        cv.rectangle(drawImg,(self.left,self.top),(self.right,self.bottom),(0,255,0),3)
    
    #Returns itself as size 4 array
    def arr(self):
        return [self.left, self.top, self.right, self.bottom]

#Stores all data for ball and some prediction
class ball_class:
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
    prew_speed : nbArray = None
    prediction_x = 0
    prediction_y = 0

    #Sets up basic ball params
    def __init__(self, position : vector2D = vector2D(0,0), position_history :int = 1):
        self.position = position
        self.range = position_history
        self.prew_speed = nbArray([0 for n in range(position_history)])

    #Resets normalised radiants
    def reset_rad(self, rads):
        self.previous_radiants = nbArray([rads for n in range(self.prev_rad_size)])

    #Updates denoised and values
    def update(self, delta):
        #Gets denoised ball speed
        self.prew_speed.pop(0)
        self.prew_speed.append(self.position.distance_to(self.last_positions) * delta * 10)
        self.ball_speed = self.prew_speed.denoised_array(0.1)
        #Gets denoised rads
        rads = self.position.rad_to(self.last_positions)
        norm_rads_uncaped = ((rads - (math.pi / 2)) % math.pi) - (math.pi / 2)
        norm_rads = abs(norm_rads_uncaped)
        #When hit it adds delay before the rads are jumpstarted denoised
        if self.init_dir > 0:
            self.init_dir -= 1
            if self.init_dir == 0:
                self.reset_rad(norm_rads)
            else:
                return
        self.previous_radiants.pop(0)
        self.previous_radiants.append(norm_rads)
        avg, if_outliner = self.previous_radiants.denoised_array(0.1, value_point = norm_rads)
        self.ball_rad = avg
        self.back_dir = norm_rads_uncaped < 0
        #Puts balls direction into 1/4 of circle so it can be calculated more nicer later 
        if not if_outliner:
            self.ball_direction = math.floor((rads*2) / math.pi)/2
            if norm_rads_uncaped < 0:
                self.ball_direction = self.ball_direction+0.5
        
        self.last_positions = self.position
            
    #Predicts ball's bounces and when it hits prediction x line and gets the y at it
    def prediction(self, image, stage, line_amount):
        color = (255, 255, 0) if self.state == 1 else (0, 0, 255)
        positions = [self.position.arr()]
        start = self.position
        direction = self.get_directional_vector()
        #Raycasts lines till it runs out of raycasted lines or hits prediction x
        for n in range(line_amount):
            len, hit_wall = start.distance_till_intersection(stage.arr(), direction)
            result = (start + direction * len)
            positions.append(result.round().arr())
            #If it hit prediction line it casts ray backwards until the line is hit
            if result.x < self.prediction_x < start.x or result.x > self.prediction_x > start.x :
                staged = stage.arr()
                if result.x < self.prediction_x < start.x:
                    staged[2] = self.prediction_x
                else:
                    staged[0] = self.prediction_x
                len2, hit_wall2 = result.distance_till_intersection(staged, direction * vector2D(-1,-1))
                result2 = (result + direction * vector2D(-1,-1) * len2)
                self.prediction_y = result2.y
                #Draws prediction line
                cv.line(image, (round(int(self.prediction_x + 100)), round(int(result2.y + 100))),
                                (round(int(self.prediction_x - 100)), round(int(result2.y - 100))),
                                (255,255,0), 2) 
                cv.line(image, (round(int(self.prediction_x + 100)), round(int(result2.y - 100))),
                                (round(int(self.prediction_x - 100)), round(int(result2.y + 100))),
                                (255,255,0), 2) 
                break
            direction *= hit_wall
            start = result
        #Displays raycast lines 
        pts = np.array([positions], dtype=np.int64)
        image = cv.polylines(image, [pts], 
                      False, color, 2)
    
    #Gets direction from vector (in heinsight it should go in vector 2d XD)
    def get_directional_vector(self):
        direction = vector2D(0,0)
        if self.back_dir:
            direction.vector_from_rad(-self.ball_rad + self.ball_direction * math.pi + math.pi)
        else:
            direction.vector_from_rad(self.ball_rad + self.ball_direction * math.pi + math.pi)
        direction = direction.normalize()
        return direction
        
#Stores all player data
class player_class:
    position : vector2D = None
    charecter = None
    speed = 0
    prev_direction = 0
    prev_pos = 0
    expected_speed : nbArray = None
    #Initilises players data
    def __init__(self, position, character):
        self.position = position
        self.character = character
        self.expected_speed = nbArray([0 for n in range(100)])
    #Denoises players speed
    def update(self, delta):
        self.expected_speed.pop(0)
        self.expected_speed.append(abs(self.position.x - self.prev_pos) * delta * 10)
        avg = self.expected_speed.denoised_array(0.2)
        self.prev_pos = self.position.x
        self.speed = avg

#Holds all game date
class gamedata:
    stage : stage_class = None
    ball : ball_class = None
    players = []
    game_start = False
    hit_amount = 0
    prev_hits = []
    #Initilises data 
    def __init__(self, ball_pos : vector2D = vector2D(0,0), players = None):
        self.stage = stage_class(ball_pos)
        self.ball = ball_class(ball_pos, [], 100)
        self.players.append(player_class(vector2D(0,0), "RAPTOR"))
    #Updates all data and prediction drawing
    def update(self, image, delta):
        if self.hit_amount > 0:
            self.prev_hits.append(self.hit_amount)
            estimate = 0
            for x in range(len(self.prev_hits)):
                estimate += self.prev_hits[x]
            estimate /= len(self.prev_hits)
            self.stage.draw(image)
            self.ball.prediction(image, self.stage, 100)
        elif len(self.prev_hits) > 0:
            self.prev_hits = []
        self.players[0].update(delta)
        self.ball.update(delta)
        if not self.game_start:
            self.game_start = True
            self.stage.reset(self.ball.position)
        self.stage.update_border(self.ball)
        self.stage.draw(image)
        self.ball.prediction(image, self.stage, 20)
        