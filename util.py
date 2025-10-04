import cv2 as cv
import pyautogui 
import numpy as np
import time
import pygetwindow
from LLBlaze import *
from Real_utils import *
import keyboard

#importing c or some shit like that
from ctypes import cdll
lib_move = cdll.LoadLibrary('.\\c_thingamajig\\movement\\movement_lib\\x64\\Debug\\movement_lib.dll')

class window_cut:
    top = 31
    right = 7
    bottom = 7
    left = 7

class llb_bot:
    windows = None
    img_test = cv.imread('testimg/test2.png',cv.IMREAD_UNCHANGED)
    img_ball = cv.imread('examples/ball/Ball.png',cv.IMREAD_UNCHANGED)
    w, h = img_ball.shape[1::-1]
    coolRect = None
    window_set = False
    bot_enabled = False
    game = gamedata(vector2D(100,100))

    #adjust based on fps your getting
    #higger fps set like 0.2 or 0.1
    #else leave it at 0
    jump_delay = 0.2
    detailed_debuger = False
    hit_enabled = False
    inputs = {
        "walk_direction" : 0,
        "jump" : False,
        "jump_timer" : 0,
        "Hit" : False,
        "Hit_timer" : 0,
    }
    debounces = {
        "w" : False,
        "r" : False,
        "e" : False,
        "s" : False,
        "a" : False,
    }
    main_loop = True
    prev_time = 0
    prev_fps = [0 for n in range(5)]
    def __init__(self, windowName):
        if len(pygetwindow.getWindowsWithTitle(windowName)):
            self.windows = pygetwindow.getWindowsWithTitle(windowName)[0]
            self.window_set = True
    
    #main function
    def run(self):
        start_time = time.time()
        while (self.main_loop):
            prev_time = time.time()

            if self.detailed_debuger: debugTimer = time.time()

            #init img
            start_img, img_hsv_value = self.get_image()
            

            #detection cycle
            self.detect_player(start_img, img_hsv_value)
            if self.detailed_debuger:
                print("Player detected:" + str(round(time.time() - debugTimer,3)))
                debugTimer = time.time()
            else:
                debugTimer = 0

            #Detects when ball is hit
            self.detect_hit(start_img, img_hsv_value)
            if self.detailed_debuger:
                print("Hit detected:" + str(round(time.time() - debugTimer,3)))
                debugTimer = time.time()

            self.detect_ball(start_img, img_hsv_value)
            if self.detailed_debuger:
                print("Ball detected:" + str(round(time.time() - debugTimer,3)))
                debugTimer = time.time()
            
            #update game
            return_inputs = self.game.update(start_img, time.time() - self.prev_time)
            self.inputs["jump"] = return_inputs["jump"]
            self.inputs["Hit"] = return_inputs["Hit"]
            if 0 in self.game.players:
                cv.putText(start_img, str(round(return_inputs["Hit_dist"],2)), (self.game.players[0].position.x + 25,self.game.players[0].position.y - 25), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if self.detailed_debuger:
                print("Game updated:" + str(round(time.time() - debugTimer,3)))
                debugTimer = time.time()

            #bot
            self.bot_movement(start_img, prev_time, debugTimer, time.time() - self.prev_time)

            #Displays if hit is enabled 
            if self.hit_enabled:
                cv.putText(start_img, "[s] Hit enabled", (400,70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            else:
                cv.putText(start_img, "[s] Hit disabled", (400,70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

                
            #timers
            self.prev_fps.pop(0)
            self.prev_fps.append(1/(time.time() - self.prev_time))
            sum = 0
            for x in self.prev_fps:
                sum += x / len(self.prev_fps)
            cv.putText(start_img, "fps:" + str(round(sum,2)), (400,550), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            cv.putText(start_img, "sec:" + str(round(time.time() - start_time, 10)), (400,580), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            self.prev_time = time.time()


            #display
            cv.imshow('funn.',start_img)
            cv.waitKey(1)

            #inputs
            self.handle_inputs(debugTimer)

    
    #pulled out func for clarities sake
    def get_image(self):
        img_hsv_value = None
        start_img = None
        if self.window_set:
            if self.detailed_debuger: debugTimer_bot = time.time()
            self.coolRect = self.windows._getWindowRect()
            # print(self.coolRect)
            #What an beutifull code :))
            if self.detailed_debuger:
                print("-Window rect :" + str(round(time.time() - debugTimer_bot,3)))
                debugTimer = time.time()
            
            screenshot = pyautogui.screenshot()\
                .crop((self.coolRect.left + window_cut.left,
                        self.coolRect.top + window_cut.top,
                        self.coolRect.right - window_cut.right,
                        self.coolRect.bottom - window_cut.bottom))
            if self.detailed_debuger:
                print("-Screenshot :" + str(round(time.time() - debugTimer_bot,3)))
                debugTimer = time.time()
            open_cv_screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
            img_hsv_value = cv.cvtColor(open_cv_screenshot, cv.COLOR_BGR2HSV)
            start_img = open_cv_screenshot
            if self.detailed_debuger:
                print("-Color convert :" + str(round(time.time() - debugTimer_bot,3)))
                debugTimer = time.time()
        else:
            img_hsv_value = cv.cvtColor(self.img_test, cv.COLOR_BGR2HSV)
            start_img = self.img_test
        if self.detailed_debuger:
            print("Loaded img in:" + str(round(time.time() - debugTimer,3)))
            debugTimer = time.time()
        return start_img, img_hsv_value

    def bot_movement(self, start_img, prev_time, debugTimer, delta):
        inputs = {
            "Hit" : False,
            "Jump" : False,
            "Left" : False,
            "Right" : False
        }
        if self.bot_enabled:
            if self.detailed_debuger: debugTimer_bot = time.time()
            
            cv.putText(start_img, "[w] Bot enabled", (400,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            #handles hitting
            if self.inputs["Hit_timer"] > 0:
                self.inputs["Hit_timer"] -= time.time() - prev_time
            elif self.inputs["Hit"] and self.hit_enabled:
                self.inputs["Hit_timer"] = 0.1
                inputs["Hit"] = True
            if self.detailed_debuger:
                print("-Hit :" + str(round(time.time() - debugTimer_bot,3)))
                debugTimer = time.time()

            #handles jump
            if self.inputs["jump_timer"] <= 0:
                self.inputs["jump_timer"] = self.jump_delay
                inputs["Jump"] = False
            elif self.inputs["jump"]:
                self.inputs["jump_timer"] -= time.time() - prev_time
                # DEBUG
                # inputs["Jump"] = True
            if self.detailed_debuger:
                print("-jump :" + str(round(time.time() - debugTimer_bot,3)))
                debugTimer = time.time()

            #handles walking
            self.inputs["walk_direction"], switch = self.calculate_next_pos(start_img, delta)
            match self.inputs["walk_direction"]:
                case -1:
                    inputs["Left"] = True
                case 0:
                    #if both disabled ;)
                    pass
                case 1:
                    inputs["Right"] = True
                case _:
                    #if both passed ;)
                    pass
            if self.detailed_debuger:
                print("-movement :" + str(round(time.time() - debugTimer_bot,3)))
                debugTimer = time.time()

            #sends input to c
            lib_move.movement(inputs["Hit"], inputs["Jump"], inputs["Left"], inputs["Right"], switch)
        else:
            cv.putText(start_img, "[w] Bot disabled", (400,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        if self.detailed_debuger:
            print("Bot processed:" + str(round(time.time() - debugTimer,3)))
            debugTimer = time.time()

    def handle_inputs(self, debugTimer):
        if  keyboard.is_pressed("q"):
            cv.destroyAllWindows()
            lib_move.movement(False, False, False, False, False)
            self.main_loop = False
            return
        if keyboard.is_pressed("w"):
            if not self.debounces["w"]:
                self.inputs["walk_direction"] = 0
                self.debounces["w"] = True
                self.bot_enabled = not self.bot_enabled
                if not self.bot_enabled:
                    lib_move.movement(False, False, False, False, False)
        else:
            self.debounces["w"] = False
            
        if keyboard.is_pressed("r"):
            if not self.debounces["r"]:
                self.debounces["r"] = True
                self.game.game_start = False
        else:
            self.debounces["r"] = False

        if keyboard.is_pressed("s"):
            if not self.debounces["s"]:
                self.debounces["s"] = True
                self.hit_enabled = not self.hit_enabled
        else:
            self.debounces["s"] = False
        
        if keyboard.is_pressed("e"):
            if not self.debounces["e"]:
                self.debounces["e"] = True
                self.detailed_debuger = not self.detailed_debuger
        else:
            self.debounces["e"] = False

        if keyboard.is_pressed("a"):
            if not self.debounces["a"]:
                self.debounces["a"] = True
                if len(self.game.players) > 0:
                    lib_move.movement(False, False, False, False, False)
                    self.game.players[0].speed = 0
                    time.sleep(0.1)
                    lib_move.movement(False, False, True, False, False)
                    time.sleep(0.1)
                    lib_move.movement(False, False, False, False, True)
                    start_img, img_hsv_value = self.get_image()
                    self.detect_player(start_img, img_hsv_value)
                    prev_playerPos = self.game.players[0].position.x
                    lib_move.movement(False, False, False, True, False)
                    time.sleep(0.2)
                    start_img, img_hsv_value = self.get_image()
                    self.detect_player(start_img, img_hsv_value)
                    self.game.players[0].speed += abs(self.game.players[0].position.x - prev_playerPos)
                    lib_move.movement(False, False, False, False, False)
                    print(self.game.players[0].speed)
                    # calib_len = 5
                    # for i in range(calib_len):
                    #     time.sleep(0.3)
                    #     prev_playerPos = self.game.players[0].position.x
                    #     lib_move.movement(False, False, False, True, False)
                    #     time.sleep(0.5)
                    #     #refreshes image and takes mesure
                    #     start_img, img_hsv_value = self.get_image()
                    #     self.detect_player(start_img, img_hsv_value)
                    #     self.game.players[0].speed += abs(self.game.players[0].position.x - prev_playerPos) / (calib_len * 2)
                    #     print(self.game.players[0].speed)
                    #     lib_move.movement(False, False, False, False, False)
                    #     time.sleep(0.3)
                    #     lib_move.movement(False, False, True, False, False)
                    #     time.sleep(0.5)
                    #     #refreshes image and takes mesure
                    #     start_img, img_hsv_value = self.get_image()
                    #     self.detect_player(start_img, img_hsv_value)
                    #     self.game.players[0].speed += abs(self.game.players[0].position.x - prev_playerPos) / (calib_len * 2)
                    #     print(self.game.players[0].speed)
                    #     lib_move.movement(False, False, False, False, False)
        else:
            self.debounces["a"] = False
        if keyboard.is_pressed("d"):
            lib_move.movement(False, False, False, False, True)
            time.sleep(1/240)
            lib_move.movement(False, False, True, False, False)
            time.sleep(1/240)
            lib_move.movement(False, False, False, False, True)
            time.sleep(1/240)
            lib_move.movement(False, False, False, True, False)
            time.sleep(1/240)
            lib_move.movement(False, False, False, False, True)
            self.debounces["a"] = False
        if keyboard.is_pressed("t"):
            self.game.players[0].speed -= 2
        if keyboard.is_pressed("g"):
            self.game.players[0].speed += 2

        
        #final debug print :))
        if self.detailed_debuger and not self.debounces["e"]:
            print("Inputs processed:" + str(round(time.time() - debugTimer,3)))
            debugTimer = time.time()
    
    
    #others aka 2nd in tree

    def calculate_next_pos(self, start_img, delta):
        # print(self.game.players[0].speed, self.game.ball.ball_speed)

        players_position = self.game.players[0].position.x
        balls_position = self.game.ball.position.x
        players_speed = self.game.players[0].speed
        players_speed *= -1 if balls_position < players_position else 1
        balls_speed = (self.game.ball.get_directional_vector() * self.game.ball.ball_speed).x
        if balls_speed == 0: balls_speed = 1
        pos_global = self.get_prediction(players_position,balls_position,players_speed,balls_speed)
        #checks if out of bounds
        # cv.line(start_img, (int(pos_global), 0), (int(pos_global),int(self.coolRect.bottom  - self.coolRect.top)), (255,255,0), 2) 
        # return -1 if pos_global < players_position else 1
        # print(self.game.ball.ball_speed, self.game.players[0].speed)
        distance_till_wall = 0
        #WHY IS IT TWEAKING LIKE THAT XD
        print(players_speed, balls_speed)
        # print(self.game.stage.left > pos_global, players_position, balls_position, players_speed, balls_speed)
        if self.game.stage.left > pos_global:
            #gets distance till wall so player can be moved
            distance_till_wall = abs(self.game.stage.left - balls_position) / abs(balls_speed)

            players_position += players_speed * distance_till_wall
            balls_position = self.game.stage.left
            balls_speed *= -1
            # players_speed *= -1 if balls_position < players_position else 1
            pos_global = self.get_prediction(players_position,balls_position,players_speed,balls_speed)
        elif self.game.stage.right < pos_global:
            #gets distance till wall so player can be moved
            distance_till_wall = abs(self.game.stage.right - balls_position) / abs(balls_speed)

            players_position += players_speed * distance_till_wall
            balls_position = self.game.stage.right
            balls_speed *= -1
            # players_speed *= -1 if balls_position < players_position else 1
            pos_global = self.get_prediction(players_position,balls_position,players_speed,balls_speed)
        # print(distance_till_wall)
        #displays players speed and prediction
        cv.putText(start_img, "[T-G]Pl sp: " + str(players_speed), (int(0),int(self.coolRect.bottom - 50 - self.coolRect.top)), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        cv.line(start_img, (int(pos_global), 0), (int(pos_global),int(self.coolRect.bottom  - self.coolRect.top)), (255,255,0), 2) 

        # if abs(players_position - pos_global) > 100:
        # else:
        #     print("2 close")

        # direction = 0
        direction = -1 if pos_global < self.game.players[0].position.x else 1
        switch = self.game.players[0].prev_direction != direction
        self.game.players[0].prev_direction = direction
        return direction, switch
        # cv.line(start_img, (pos, 0), (pos, self.coolRect.bottom), (255,255,0), 1) 

    def detect_hit(self, start_img, img_hsv_value):
        screen_witdth = start_img.shape
        var = 65/2
        var2 = screen_witdth[1] + 170
        masked_screenshot = img_hsv_value[screen_witdth[0]-120:screen_witdth[0]-110, int(var2/2-var):int(var2/2+var)]
        masked_screenshot = cv.inRange(masked_screenshot, 
                                       np.array([0, 0, 0]),
                                        np.array([0, 0, 0]))
        detected = 0
        for y in range(0, masked_screenshot.shape[0]):
            for x in range(0,masked_screenshot.shape[1]):
                if masked_screenshot[y,x] != 0:
                    detected += 1
        self.game.hit_amount = detected
        if detected > 2:
            self.game.ball.init_dir = 5

    def detect_player(self, start_img, img_hsv_value):
        screen_witdth = start_img.shape
        masked_screenshot = img_hsv_value[120:screen_witdth[0], 0:screen_witdth[1]]
        ret, thresh = self.color_find(masked_screenshot, 
                                    np.array([1, 242, 217]),
                                    np.array([2, 242, 217]))
        movement = cv.moments(thresh)
        if movement['m00'] > 0:
            cX = int(movement["m10"] / movement["m00"])
            cY = int(movement["m01"] / movement["m00"]) + 120
            cv.circle(start_img, (cX, cY), 20, (255, 255, 255), -1)
            cv.circle(start_img, (cX, cY), 10, (0, 0, 0), -1)
            self.game.players[0].position = vector2D(cX, cY)

    def detect_ball(self, start_img, img_hsv_value):
        self.game.ball.state = 0

        #detection
        #BLUE
        self.get_color(start_img, img_hsv_value, 1,
                                np.array([105, 243, 255]),
                                np.array([105, 244, 255]))
        #RED
        self.get_color(start_img, img_hsv_value, 2,
                                np.array([5, 229, 255]),
                                np.array([5, 230, 255]))
        match self.game.ball.state:
            case 1:
                cv.putText(start_img, "Blue ball", (100,570), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
                pass
            case 2:
                cv.putText(start_img, "Red ball", (100,570), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                pass
            case _:
                cv.putText(start_img, "No ball", (100,570), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                pass

    def get_color(self, start_img, hsv_img, ball_stage, mask_upper, mask_lower):
        color = (255, 255, 0) if ball_stage == 1 else (0, 0, 255)
        ret, thresh = self.color_find(hsv_img, mask_upper, mask_lower)
        movement = cv.moments(thresh)
        if movement['m00'] > 0:
            cX = int(movement["m10"] / movement["m00"])
            cY = int(movement["m01"] / movement["m00"])
            cv.circle(start_img, (cX, cY), 20, (255, 255, 255), -1)
            cv.circle(start_img, (cX, cY), 10, (0, 0, 0), -1)
            cv.circle(start_img, (cX, cY), 5, color, -1)
            cv.putText(start_img, "x:" + str(cX) + " y:"+ str(cY), (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            self.game.ball.state = ball_stage
            self.game.ball.position = vector2D(cX, cY)
    
    def color_find(self, hsv_img, mask_upper, mask_lower):
        masked_screenshot = cv.inRange(hsv_img, mask_upper, mask_lower)
        return cv.threshold(masked_screenshot,254,255,0)

    #layer 3 of hell
    def get_prediction(self, players_position, balls_position, players_speed, balls_speed):
        #whatever the fuck this is
        delta_x = balls_position - players_position
        if (balls_speed - players_speed) == 0:
            return 0
        pos = -balls_speed * delta_x / (balls_speed - players_speed)
        pos_global = pos + balls_position
        return pos_global