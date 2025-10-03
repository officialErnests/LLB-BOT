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
    last_positions = []
    range = 0
    ball_speed = 0
    prev_rad = []
    prev_rad_size = 10
    ball_rad = 0
    ball_direction = 0
    back_dir = False
    def __init__(self, position : vector2D = vector2D(0,0), state : ball_states = ball_states.NEUTRAL, position_history :int = 1):
        self.position = position
        self.state = state
        self.range = position_history -1
        self.last_positions = [position for n in range(position_history)]
        self.reset_rad()

    def reset_rad(self):
        self.prev_rad = [0 for n in range(self.prev_rad_size)]

    def update(self):
        self.last_positions.pop(0)
        self.last_positions.append(self.position)

        #Get's the ball speed
        last_pos = None
        temp_speed = 0
        for pos in self.last_positions:
            if last_pos is None:
                last_pos = pos
            temp_speed += pos.distance_to(last_pos) / (self.range + 1)
            last_pos = pos
        self.ball_speed = self.ball_speed * 0.9 + temp_speed * 0.1

        # calculates angle
        #OH GOD WHAT I WAS ON YESTRADAY XXDD
        rads = self.position.rad_to(self.last_positions[self.range - 1])
        norm_rads_uncaped = ((rads - (math.pi / 2)) % math.pi) - (math.pi / 2)
        norm_rads = abs(norm_rads_uncaped)
        #Todo WHATEVER THE BATSHIT IS THIS
        self.prev_rad.pop(0)
        self.prev_rad.append(round(norm_rads,1))
        # print(norm_rads)
        #filters data.. idk how just like 11.11pm rjn i'm tierd ;-;
        sorted_arr = self.prev_rad
        sorted_arr.sort()
        middle = sorted_arr[int(math.floor(self.prev_rad_size / 2))]
        avg = 0
        avg_num = 1
        range = 1
        for x in sorted_arr:
            if x < middle - range:
                continue
            elif x < middle + range:
                avg = (avg * (avg_num - 1) + x) / avg_num
                avg_num += 1
            else:
                break
        #checks if the angle isn't valid
        self.ball_rad = norm_rads
        self.back_dir = norm_rads_uncaped < 0
        self.ball_direction = math.floor((rads*2) / math.pi)/2
        print(rads, norm_rads, self.ball_direction)
        if norm_rads_uncaped < 0:
            self.ball_direction = self.ball_direction+0.5
            # print(rads, norm_rads, self.ball_direction)
        # print(self.prev_rad)
        #1.596431735316574 1.545160918273219 -1.0707963267948966
        #1.596431735316574 = pi - 1.545160918273219
        #1.6030432092301505 1.5385494443596426 -1.5
        #1.6030432092301505 1.5385494443596426 -1.5
        # 2.5948038127005457 0.5467888408892474 0
        # WHY DOES IT ONLY GO IN ONE WAY BOTH WAYS TF????
        #bc 'im stoopid and used old formula witouth /2 in heinsaight i should have just used self.ball_direction in start iinstead of duplicating code XD
            
    
    def draw(self, image):
            color = (100, 100, 0) if self.state == 1 else (0, 0, 100)
            cool_array = []
            for vec2D in self.last_positions:
                cool_array.append(vec2D.arr())
            pts = np.array(cool_array)
            image = cv.polylines(image, [pts], 
                      False, color, 2)
    
    def prediction(self, image, stage, line_amount):
        color = (255, 255, 0) if self.state == 1 else (0, 0, 255)
        
        positions = [self.position.arr()]
        start = self.position
        direction = vector2D(0,0)
        # print(self.ball_rad, self.ball_direction * math.pi)
        # direction.vector_from_rad(self.ball_rad + math.pi)
        # direction.vector_from_rad(self.ball_direction * math.pi)
        if self.back_dir:
            direction.vector_from_rad(-self.ball_rad + self.ball_direction * math.pi + math.pi)
        else:
            direction.vector_from_rad(self.ball_rad + self.ball_direction * math.pi + math.pi)
        direction = direction.normalize()
        for n in range(line_amount):
            len, hit_wall = start.distance_till_intersection(stage.arr(), direction)
            # print(direction, len)
            result = (start + direction * len)
            positions.append(result.arr())
            direction *= hit_wall
            start = result

        pts = np.array([positions], dtype=np.int64)
        image = cv.polylines(image, [pts], 
                      False, color, 2)
        

class player_class:
    position : vector2D = None
    charecter = None
    speed : 0
    def __init__(self, position, character):
        self.position = position
        self.character = character

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
    def update(self, image):
        if self.hit_amount > 0:
            self.prev_hits.append(self.hit_amount)
            estimate = 0
            for x in range(len(self.prev_hits)):
                estimate += self.prev_hits[x]
            estimate /= len(self.prev_hits)
            self.stage.draw(image)
            self.ball.draw(image)
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
        self.ball.update()
        if not self.game_start:
            self.game_start = True
            self.stage.reset(self.ball.position)
        self.stage.update_border(self.ball)

        #debug stuff
        self.stage.draw(image)
        self.ball.draw(image)

        self.ball.prediction(image, self.stage, 10)
        
        #sends player input  c  c 
        return_inputs = {
            "walk_direction" : -1 if self.players[0].position.x > self.ball.position.x else 1,
            "jump" : self.players[0].position.y > self.ball.position.y,
            "Hit" : self.players[0].position.distance_to(self.ball.position) < 200,
            "Hit_dist" : self.players[0].position.distance_to(self.ball.position),
        }
        return return_inputs