import numpy as np
import cv2 as cv
import pygetwindow
import pyautogui 
import keyboard
import win32gui
import win32con
import time

from Real_utils import *
from LLBlaze import *

#Emulator for my lib
class emulator_lib:
    def movement(self, hit, jump, left, right, up):
        if hit: pyautogui.keyDown("c")
        else: pyautogui.keyUp("c")
        if jump: pyautogui.keyDown("space")
        else: pyautogui.keyUp("space")
        if left: pyautogui.keyDown("left")
        else: pyautogui.keyUp("left")
        if right: pyautogui.keyDown("right")
        else: pyautogui.keyUp("right")
        if up: pyautogui.keyDown("up")
        else: pyautogui.keyUp("up")
lib_move = None
try:
    from ctypes import cdll
    lib_move = cdll.LoadLibrary("./c_thingamajig/movement/movement_lib/x64/Debug/movement_lib.dll")
except:
    cv.namedWindow("Missing dependencies", cv.WINDOW_NORMAL)
    cv.resizeWindow("Missing dependencies", 400, 400)
    logo = cv.imread('Assets/Logo.png',cv.IMREAD_UNCHANGED)
    y = 0
    y += 50
    cv.putText(logo, "UNABLE TO LOAD DLL", (50,y), 1, 4, (200,200,0), 3)
    y += 50
    cv.putText(logo, "(It's common issue)", (50,y), 1, 4, (200,200,0), 3)
    y += 50
    cv.putText(logo, "All this means is that", (50,y), 1, 4, (200,200,0), 3)
    y += 50
    cv.putText(logo, "You will have to use ", (50,y), 1, 4, (200,200,0), 3)
    y += 50
    cv.putText(logo, "pyautogui, which isn't bad", (50,y), 1, 4, (200,200,0), 3)
    y += 50
    cv.putText(logo, "but it is slower", (50,y), 1, 4, (200,200,0), 3)
    y += 100
    cv.putText(logo, "press any key to continue", (50,y), 1, 4, (200,200,0), 3)
    cv.imshow("Missing dependencies", logo)
    cv.waitKey()
    try:
        cv.destroyWindow("Missing dependencies")
    except:
        pass
    lib_move = emulator_lib()


#Used for removing ded space that is added in default windows
class WND_CUT:
    top = 31
    right = 7
    bottom = 7
    left = 7

class llb_bot:
    windows = None
    ScreenRect = None
    bot_enabled = False
    #All game date goes in game class (in #LLBlaze.py)
    game = gamedata(vector2D(100,100))
    #Setable variables
    compact_mode = True
    vision_enabled = False
    bot_hit_enabled = True
    simple_ai = False
    #Constants
    JUMP_DELAY = 0.2
    HIT_DELAY = 0.1
    #Variables program uses
    window_open = False
    movement_data = {
        "walk_direction" : 0,
        "jump_timer" : 0,
        "Hit_timer" : 0,
    }
    debounces = {
        "5" : False,
        "6" : False,
        "7" : False,
        "8" : False,
        "9" : False,
    }
    main_loop = True
    prev_time = 0
    prev_fps = [0 for n in range(5)]
    last_direction = False
    windowName = None
    window = None

    #Gets the games window name as well finds the windows handle and window itself
    def __init__(self, windowName):
        self.windowName = windowName
        if len(pygetwindow.getWindowsWithTitle(windowName)):
            self.window = win32gui.FindWindow(None, windowName)
            self.windows = pygetwindow.getWindowsWithTitle(windowName)[0]
    
    #this is the main loop
    def cleaner_run(self):

        #Creates window
        cv.namedWindow("NSLB", cv.WINDOW_NORMAL)
        try:
            cv.resizeWindow("NSLB", 400, 400)
        except:
            print("couldn't resize ;-;")
        
        #Main loop
        Time_Till_Start = time.time()
        while self.main_loop:
            #fps
            self.prev_fps.pop(0)
            self.prev_fps.append(1/(time.time() - self.prev_time))
            sum = 0
            for x in self.prev_fps:
                sum += x / len(self.prev_fps)

            #Gets time at start of frame as well the together time
            self.prev_time = time.time()
            

            #bg image or starting canvas
            logo = cv.imread('Assets/Logo.png',cv.IMREAD_UNCHANGED)

            #Checks if programm is running
            if not self.window or not win32gui.IsWindow(self.window):

                lib_move.movement(False,False,False,False,False)
                self.compact_mode = True
                self.vision_enabled = False
                self.bot_enabled = False
                self.bot_hit_enabled = True
                self.simple_ai = False
                animation_time = time.time() - Time_Till_Start
                x,y = int(math.sin(animation_time)*120+20),50
                cv.putText(logo, "!!NO LLB??", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "!!NO LLB??", (x,y), 1, 10,        (0,0,255), 15)
                x,y = int(math.sin(animation_time+0.5)*120+20),200
                cv.putText(logo, "!!NO LLB??", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "!!NO LLB??", (x,y), 1, 10,        (0,0,255), 15)
                x,y = int(math.sin(animation_time+1)*120+20),350
                cv.putText(logo, "!!NO LLB??", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "!!NO LLB??", (x,y), 1, 10,        (0,0,255), 15)
                x,y = int(math.sin(animation_time+1.5)*120+20),500
                cv.putText(logo, "!!NO LLB??", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "!!NO LLB??", (x,y), 1, 10,        (0,0,255), 15)
                x,y = int(math.sin(animation_time+2)*120+20),650
                cv.putText(logo, "!!NO LLB??", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "!!NO LLB??", (x,y), 1, 10,        (0,0,255), 15)
                x,y = int(math.sin(animation_time+2.5)*120+20),800
                cv.putText(logo, "!!NO LLB??", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "!!NO LLB??", (x,y), 1, 10,        (0,0,255), 15)

                x,y = 0,int(math.cos(animation_time+2.5)*200+400)
                cv.putText(logo, "Q - QUIT", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "Q - QUIT", (x,y), 1, 10,        (255,255,0), 15)
                cv.imshow('NSLB',logo)
                cv.waitKey(1)
                time.sleep(0.1)
                self.handle_inputs()
                if self.window_open:
                    self.window_open = False
                    cv.destroyWindow('NOT SO LETHAL BLAZE')
                if len(pygetwindow.getWindowsWithTitle(self.windowName)):
                    self.window = win32gui.FindWindow(None, self.windowName)
                    self.windows = pygetwindow.getWindowsWithTitle(self.windowName)[0]
                continue

            #Checks if programm is minimized
            if win32gui.GetWindowPlacement(self.window)[1] == win32con.SW_SHOWMINIMIZED:
                lib_move.movement(False,False,False,False,False)
                self.compact_mode = True
                self.vision_enabled = False
                self.bot_enabled = False
                self.bot_hit_enabled = True
                self.simple_ai = False

                x,y = 10,780
                cv.putText(logo, "FPS:" + str(round(sum,2)), (x+5,y+5), 1, 3,    (255,255,255), 15)
                cv.putText(logo, "FPS:" + str(round(sum,2)), (x,y), 1, 3,        (0,0,0), 5)
                x,y = 10,100
                cv.putText(logo, "[5] Compact mode: " + ("V" if self.compact_mode else "X"), (x+3,y+3), 1, 4,       (255,255,0) if self.compact_mode else (255,255,255), 15)
                cv.putText(logo, "[5] Compact mode: " + ("V" if self.compact_mode else "X"), (x,y), 1, 4,           (255,255,255) if self.compact_mode else (0,0,0), 5)
                x,y = 10,200
                cv.putText(logo, "[6] Vision enabled: " + ("V" if self.vision_enabled else "X"), (x+5,y+5), 1, 4,   (255,255,0) if self.vision_enabled else (255,255,255), 15)
                cv.putText(logo, "[6] Vision enabled: " + ("V" if self.vision_enabled else "X"), (x,y), 1, 4,       (255,255,255) if self.vision_enabled else (0,0,0), 5)
                x,y = 10,300
                cv.putText(logo, "[7] Bot following: " + ("V" if self.bot_enabled else "X"), (x+5,y+5), 1, 4,  (255,255,0) if self.bot_enabled else (255,255,255), 15)
                cv.putText(logo, "[7] Bot following: " + ("V" if self.bot_enabled else "X"), (x,y), 1, 4,      (255,255,255) if self.bot_enabled else (0,0,0), 5)
                x,y = 10,400
                cv.putText(logo, "[8] Bot hitting: " + ("V" if self.bot_hit_enabled else "X"), (x+5,y+5), 1, 4, (255,255,0) if self.bot_hit_enabled else (255,255,255), 15)
                cv.putText(logo, "[8] Bot hitting: " + ("V" if self.bot_hit_enabled else "X"), (x,y), 1, 4,     (255,255,255) if self.bot_hit_enabled else (0,0,0), 5)
                x,y = 10,500
                cv.putText(logo, "[9] Simple ai: " + ("V" if self.simple_ai else "X"), (x+5,y+5), 1, 4,    (255,255,0) if self.simple_ai else (255,255,255), 15)
                cv.putText(logo, "[9] Simple ai: " + ("V" if self.simple_ai else "X"), (x,y), 1, 4,        (255,255,255) if self.simple_ai else (0,0,0), 5)
                x,y = 10,600
                cv.putText(logo, "[0] - Reset border", (x+5,y+5), 1, 4,    (255,255,255), 15)
                cv.putText(logo, "[0] - Reset border", (x,y), 1, 4,        (0,0,0), 5)
                x,y = 10,700
                cv.putText(logo, "[-] - Funny", (x+5,y+5), 1, 4,    (255,255,255), 15)
                cv.putText(logo, "[-] - Funny", (x,y), 1, 4,        (0,0,0), 5)
                x,y = 430,770
                cv.putText(logo, "QUIT - [Q]", (x+5,y+5), 1, 4,    (255,255,255), 15)
                cv.putText(logo, "QUIT - [Q]", (x,y), 1, 4,        (0,0,255), 5)
                x,y = 10,780
                cv.putText(logo, "MINIMIZED", (x+5,y+5), 1, 10,    (255,255,255), 30)
                cv.putText(logo, "MINIMIZED", (x,y), 1, 10,        (0,0,255), 15)
                if self.window_open:
                    self.window_open = False
                    cv.destroyWindow('NOT SO LETHAL BLAZE')
                cv.imshow('NSLB',logo)
                cv.waitKey(1)
                time.sleep(0.1)
                self.handle_inputs()
                continue

            #Does all detection checks aka vision
            start_img, img_hsv_value = self.get_image()
            if self.vision_enabled:
                self.detect_player(start_img, img_hsv_value)
                self.detect_hit(start_img, img_hsv_value)
                self.detect_ball(start_img, img_hsv_value)
                #Updates all variables (normalises and processes next positions)
                self.game.update(start_img, time.time() - self.prev_time)
            
            #Moves bot based on game data
            self.bot_movement(start_img, time.time() - self.prev_time)

            #Gui text
            x,y = 10,780
            cv.putText(logo, "FPS:" + str(round(sum,2)), (x+5,y+5), 1, 3,    (255,255,255), 15)
            cv.putText(logo, "FPS:" + str(round(sum,2)), (x,y), 1, 3,        (0,0,0), 5)
            x,y = 10,100
            cv.putText(logo, "[5] Compact mode: " + ("V" if self.compact_mode else "X"), (x+3,y+3), 1, 4,       (255,255,0) if self.compact_mode else (255,255,255), 15)
            cv.putText(logo, "[5] Compact mode: " + ("V" if self.compact_mode else "X"), (x,y), 1, 4,           (255,255,255) if self.compact_mode else (0,0,0), 5)
            x,y = 10,200
            cv.putText(logo, "[6] Vision enabled: " + ("V" if self.vision_enabled else "X"), (x+5,y+5), 1, 4,   (255,255,0) if self.vision_enabled else (255,255,255), 15)
            cv.putText(logo, "[6] Vision enabled: " + ("V" if self.vision_enabled else "X"), (x,y), 1, 4,       (255,255,255) if self.vision_enabled else (0,0,0), 5)
            x,y = 10,300
            cv.putText(logo, "[7] Bot following: " + ("V" if self.bot_enabled else "X"), (x+5,y+5), 1, 4,  (255,255,0) if self.bot_enabled else (255,255,255), 15)
            cv.putText(logo, "[7] Bot following: " + ("V" if self.bot_enabled else "X"), (x,y), 1, 4,      (255,255,255) if self.bot_enabled else (0,0,0), 5)
            x,y = 10,400
            cv.putText(logo, "[8] Bot hitting: " + ("V" if self.bot_hit_enabled else "X"), (x+5,y+5), 1, 4, (255,255,0) if self.bot_hit_enabled else (255,255,255), 15)
            cv.putText(logo, "[8] Bot hitting: " + ("V" if self.bot_hit_enabled else "X"), (x,y), 1, 4,     (255,255,255) if self.bot_hit_enabled else (0,0,0), 5)
            x,y = 10,500
            cv.putText(logo, "[9] Simple ai: " + ("V" if self.simple_ai else "X"), (x+5,y+5), 1, 4,    (255,255,0) if self.simple_ai else (255,255,255), 15)
            cv.putText(logo, "[9] Simple ai: " + ("V" if self.simple_ai else "X"), (x,y), 1, 4,        (255,255,255) if self.simple_ai else (0,0,0), 5)
            x,y = 10,600
            cv.putText(logo, "[0] - Reset border", (x+5,y+5), 1, 4,    (255,255,255), 15)
            cv.putText(logo, "[0] - Reset border", (x,y), 1, 4,        (0,0,0), 5)
            x,y = 10,700
            cv.putText(logo, "[-] - Funny", (x+5,y+5), 1, 4,    (255,255,255), 15)
            cv.putText(logo, "[-] - Funny", (x,y), 1, 4,        (0,0,0), 5)
            x,y = 430,770
            cv.putText(logo, "QUIT - [Q]", (x+5,y+5), 1, 4,    (255,255,255), 15)
            cv.putText(logo, "QUIT - [Q]", (x,y), 1, 4,        (0,0,255), 5)
            cv.imshow('NSLB',logo)

            #displays how everything is detected
            if not self.compact_mode:
                cv.imshow('NOT SO LETHAL BLAZE',start_img)
                self.window_open = True
            elif self.window_open:
                self.window_open = False
                cv.destroyWindow('NOT SO LETHAL BLAZE')

            #Waits so programm just dosn;t rush inf cycles (as well open cv just crashes if there isn't no cv.waitkey XD)
            cv.waitKey(1)
            self.handle_inputs()

    #Takes screenshot and crops it so it fits the game window then creates 2 versions one BGR and second HSV
    def get_image(self):
        img_hsv_value = None
        start_img = None
        self.ScreenRect = self.windows._getWindowRect()
        screenshot = pyautogui.screenshot()\
            .crop((self.ScreenRect.left + WND_CUT.left,
                    self.ScreenRect.top + WND_CUT.top,
                    self.ScreenRect.right - WND_CUT.right,
                    self.ScreenRect.bottom - WND_CUT.bottom))
        open_cv_screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        img_hsv_value = cv.cvtColor(open_cv_screenshot, cv.COLOR_BGR2HSV)
        start_img = open_cv_screenshot
        return start_img, img_hsv_value

    #Makes bot move and hit based on game data
    def bot_movement(self, start_img, delta):
        #These are used so i only have to call library once
        inputs = {
            "Hit" : False,
            "Jump" : False,
            "Left" : False,
            "Right" : False
        }
        if self.bot_enabled:
            if self.simple_ai:
                #Switcher is used to instantly turn around (presing up before switching direction)
                switcher = False
                if self.last_direction != self.game.players[0].position.x > self.game.ball.position.x:
                    self.last_direction = self.game.players[0].position.x > self.game.ball.position.x
                    switcher = True
                
                #Handles jump and if held down then after cooldown it represses it so player can double jump
                inputs["Jump"] = self.game.players[0].position.y > self.game.ball.position.y
                if self.movement_data["jump_timer"] <= 0:
                    self.movement_data["jump_timer"] = self.JUMP_DELAY
                    inputs["Jump"] = False
                elif inputs["Jump"]:
                    self.movement_data["jump_timer"] -= delta
                else:
                    self.movement_data["jump_timer"] = 0

                #Sames as jump it holds hit and after timer represes hit 
                inputs["Hit"] = (self.game.players[0].position.distance_to(self.game.ball.position) < 200) if self.bot_hit_enabled else False
                if self.movement_data["Hit_timer"] <= 0:
                    self.movement_data["Hit_timer"] = self.HIT_DELAY
                    inputs["Hit"] = False
                elif inputs["Hit"]:
                    self.movement_data["Hit_timer"] -= delta
                else:
                    self.movement_data["Hit_timer"] = 0

                #Calls library to execute 
                lib_move.movement(inputs["Hit"],
                                  inputs["Jump"],
                                  self.game.players[0].position.x > self.game.ball.position.x, 
                                  self.game.players[0].position.x < self.game.ball.position.x,
                                  switcher)
            else:
                #Gets the next position from calculate_next_pos()
                self.movement_data["walk_direction"], switch, hit, jump = self.calculate_next_pos(start_img)

                #Just checks movement direction and sets coresponding direction
                if self.movement_data["walk_direction"] == -1: inputs["Left"] = True
                elif self.movement_data["walk_direction"] == 1: inputs["Right"] = True

                #Same as simple ai
                inputs["Jump"] = jump
                if self.movement_data["jump_timer"] <= 0:
                    self.movement_data["jump_timer"] = self.JUMP_DELAY
                    inputs["Jump"] = False
                elif inputs["Jump"]:
                    self.movement_data["jump_timer"] -= delta
                else:
                    self.movement_data["jump_timer"] = 0
                
                inputs["Hit"] = hit if self.bot_hit_enabled else False
                if self.movement_data["Hit_timer"] <= 0:
                    self.movement_data["Hit_timer"] = self.HIT_DELAY
                    inputs["Hit"] = False
                elif inputs["Hit"]:
                    self.movement_data["Hit_timer"] -= delta
                else:
                    self.movement_data["Hit_timer"] = 0

                lib_move.movement(inputs["Hit"], inputs["Jump"], inputs["Left"], inputs["Right"], switch)

    #Used to handle key presses (q and 5-0 and '-')
    def handle_inputs(self):
        #Quits
        if  keyboard.is_pressed("q"):
            cv.destroyAllWindows()
            lib_move.movement(False, False, False, False, False)
            self.main_loop = False
            return
        
        #Enables/disables compact mode (Enabled by default)
        if keyboard.is_pressed("num 5"):
            if not self.debounces["5"]:
                self.debounces["5"] = True
                self.compact_mode = not self.compact_mode
        else:
            self.debounces["5"] = False

        #Enables/disables detection aka vision aka opencv detection
        if keyboard.is_pressed("num 6")  and not keyboard.is_pressed("right"):
            if not self.debounces["6"]:
                self.debounces["6"] = True
                self.vision_enabled = not self.vision_enabled
        else:
            self.debounces["6"] = False

        #Enables/disables bot movement
        if keyboard.is_pressed("num 7") and not keyboard.is_pressed("home"):
            if not self.debounces["7"]:
                self.debounces["7"] = True
                self.bot_enabled = not self.bot_enabled
                if not self.bot_enabled:
                    lib_move.movement(False,False,False,False,False)
        else:
            self.debounces["7"] = False

        #Enables/disables bot hitting (Enabled by default)
        if keyboard.is_pressed("num 8") and not keyboard.is_pressed("up"):
            if not self.debounces["8"]:
                self.debounces["8"] = True
                self.bot_hit_enabled = not self.bot_hit_enabled
        else:
            self.debounces["8"] = False

        #Enables/disables simpler ai
        if keyboard.is_pressed("num 9") and not keyboard.is_pressed("page up"):
            if not self.debounces["9"]:
                self.debounces["9"] = True
                self.simple_ai = not self.simple_ai
        else:
            self.debounces["9"] = False
        
        #Resets border
        if keyboard.is_pressed("num 0") and not keyboard.is_pressed("insert"):
            if not self.debounces["0"]:
                self.debounces["0"] = True
                self.game.game_start = False
        else:
            self.debounces["0"] = False

        #Does the funny dance
        if keyboard.is_pressed("-"):
            lib_move.movement(False, False, False, False, True)
            time.sleep(1/240)
            lib_move.movement(False, False, True, False, False)
            time.sleep(1/240)
            lib_move.movement(False, False, False, False, True)
            time.sleep(1/240)
            lib_move.movement(False, False, False, True, False)
            time.sleep(1/240)
            lib_move.movement(False, False, False, False, False)
    
    #gets where the collision will hapen between player and ball (only x as y is handeled by LLBlaze.py)
    def calculate_next_pos(self, start_img):
        balls_speed = (self.game.ball.get_directional_vector() * self.game.ball.ball_speed).x
        #Edge case
        if balls_speed == 0: balls_speed = 1

        #Sets up all variables
        players_position = self.game.players[0].position.x
        balls_position = self.game.ball.position.x
        players_speed = self.game.players[0].speed
        players_speed *= -1 if balls_position < players_position else 1

        #Gets prediction
        pos_global = self.get_prediction(players_position,balls_position,players_speed,balls_speed)

        #Checks if prediction is past borders if so run prediction again but from borders towards player to get collision point
        if self.game.stage.left > pos_global:
            distance_till_wall = abs(self.game.stage.left - balls_position) / abs(balls_speed)
            players_position += players_speed * distance_till_wall
            balls_position = self.game.stage.left
            balls_speed *= -1
            pos_global = self.get_prediction(players_position,balls_position,players_speed,balls_speed)
        elif self.game.stage.right < pos_global:
            distance_till_wall = abs(self.game.stage.right - balls_position) / abs(balls_speed)
            players_position += players_speed * distance_till_wall
            balls_position = self.game.stage.right
            balls_speed *= -1
            pos_global = self.get_prediction(players_position,balls_position,players_speed,balls_speed)

        #Draws collision x
        cv.line(start_img, (round(pos_global), 0), (round(pos_global),round(self.ScreenRect.bottom  - self.ScreenRect.top)), (255,255,0), 2) 
        
        #Calls ball so can get collision y position
        self.game.ball.prediction(start_img, self.game.stage, 20)

        #Outputs bot movement
        self.game.ball.prediction_x = pos_global
        direction = -1 if  self.game.ball.position.x < self.game.players[0].position.x else 1
        switch = self.game.players[0].prev_direction != direction
        self.game.players[0].prev_direction = direction
        hit = abs(self.game.players[0].position.x - pos_global) < 100
        jump = self.game.players[0].position.y > self.game.ball.prediction_y
        return direction, switch, hit, jump

    #Gets wheter somone is hitting the ball
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
            self.game.ball.init_dir = 1

    #Gets position of bot
    def detect_player(self, start_img, img_hsv_value):
        screen_witdth = start_img.shape
        masked_screenshot = img_hsv_value[120:screen_witdth[0], 0:screen_witdth[1]]
        ret, thresh = self.color_find(masked_screenshot, 
                                    np.array([1, 242, 217]),
                                    np.array([2, 242, 217]))
        movement = cv.moments(thresh)
        #If player is found
        if movement['m00'] > 0:
            cX = int(movement["m10"] / movement["m00"])
            cY = int(movement["m01"] / movement["m00"]) + 120
            cv.circle(start_img, (cX, cY), 20, (255, 255, 255), -1)
            cv.circle(start_img, (cX, cY), 10, (0, 0, 0), -1)
            self.game.players[0].position = vector2D(cX, cY)

    #Gets position of ball (abscured)
    def detect_ball(self, start_img, img_hsv_value):
        self.game.ball.state = 0
        self.get_color(start_img, img_hsv_value, 1,
                                np.array([105, 243, 255]),
                                np.array([105, 244, 255]))
        self.get_color(start_img, img_hsv_value, 2,
                                np.array([5, 229, 255]),
                                np.array([5, 230, 255]))

    #Gets ball
    def get_color(self, start_img, hsv_img, ball_stage, mask_upper, mask_lower):
        color = (255, 255, 0) if ball_stage == 1 else (0, 0, 255)
        ret, thresh = self.color_find(hsv_img, mask_upper, mask_lower)
        movement = cv.moments(thresh)
        #If ball exists
        if movement['m00'] > 0:
            cX = int(movement["m10"] / movement["m00"])
            cY = int(movement["m01"] / movement["m00"])
            cv.circle(start_img, (cX, cY), 20, (255, 255, 255), -1)
            cv.circle(start_img, (cX, cY), 10, (0, 0, 0), -1)
            cv.circle(start_img, (cX, cY), 5, color, -1)
            self.game.ball.state = ball_stage
            self.game.ball.position = vector2D(cX, cY)
    
    #Finds specific color in hsv_img
    def color_find(self, hsv_img, mask_upper, mask_lower):
        masked_screenshot = cv.inRange(hsv_img, mask_upper, mask_lower)
        return cv.threshold(masked_screenshot,254,255,0)
    
    #Some insane math that returns x position of meating point
    def get_prediction(self, players_position, balls_position, players_speed, balls_speed):
        delta_x = players_position - balls_position
        if (players_speed - balls_speed) == 0:
            return 0
        pos = -players_speed * delta_x / (players_speed - balls_speed)
        pos_global = pos + players_position
        return pos_global