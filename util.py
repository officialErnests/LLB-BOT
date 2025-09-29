import cv2 as cv
import pyautogui 
import numpy as np
import time
import pygetwindow
from LLBlaze import *
from Real_utils import *
import keyboard

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
    jump_delay = 0

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
    }

    prev_time = 0
    prev_fps = [0 for n in range(5)]
    def __init__(self, windowName):
        if len(pygetwindow.getWindowsWithTitle(windowName)):
            self.windows = pygetwindow.getWindowsWithTitle(windowName)[0]
            self.window_set = True
    
    def run(self):
        start_time = time.time()
        while (True):
            prev_time = time.time()


            #init img
            img_hsv_value = None
            start_img = None
            if self.window_set:
                self.coolRect = self.windows._getWindowRect()
                # print(self.coolRect)
                #What an beutifull code :))
                
                screenshot = pyautogui.screenshot()\
                    .crop((self.coolRect.left + window_cut.left,
                            self.coolRect.top + window_cut.top,
                            self.coolRect.right - window_cut.right,
                            self.coolRect.bottom - window_cut.bottom))
                open_cv_screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
                img_hsv_value = cv.cvtColor(open_cv_screenshot, cv.COLOR_BGR2HSV)
                start_img = open_cv_screenshot
            else:
                img_hsv_value = cv.cvtColor(self.img_test, cv.COLOR_BGR2HSV)
                start_img = self.img_test
            
            self.detect_player(start_img, img_hsv_value)

            self.detect_hit(start_img, img_hsv_value)

            self.detect_ball(start_img, img_hsv_value)
            
            #update game
            prew_inputs = {
                "walk_direction" : self.inputs["walk_direction"],
                "jump" :  self.inputs["jump"],
                "jump_timer" : 0,
                "Hit" : self.inputs["Hit"],
                "Hit_timer" : 0,
            }
            return_inputs = self.game.update(start_img)
            self.inputs["walk_direction"] = return_inputs["walk_direction"]
            self.inputs["jump"] = return_inputs["jump"]
            self.inputs["Hit"] = return_inputs["Hit"]

            #bot
            if self.bot_enabled:
                cv.putText(start_img, "[w] Bot enabled", (400,50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

                #handles hitting
                if self.inputs["Hit_timer"] > 0:
                    self.inputs["Hit_timer"] -= time.time() - prev_time
                elif self.inputs["Hit"]:
                    self.inputs["Hit_timer"] = 0.1
                    pyautogui.press("c")

                #handles jump
                if self.inputs["jump_timer"] > 0:
                    self.inputs["jump_timer"] -= time.time() - prev_time
                    if not self.inputs["jump"] and prew_inputs["jump"]:
                        pyautogui.keyUp("space")
                elif self.inputs["jump"]:
                    self.inputs["jump_timer"] = self.jump_delay
                    pyautogui.keyDown("space")
                elif prew_inputs["jump"] != self.inputs["jump"]:
                    pyautogui.keyUp("space")

                #handles walking
                if prew_inputs["walk_direction"] != self.inputs["walk_direction"]:
                    match self.inputs["walk_direction"]:
                        case -1:
                            pyautogui.keyDown("left")
                            pyautogui.keyUp("right")
                        case 0:
                            pyautogui.keyUp("left")
                            pyautogui.keyUp("right")
                        case 1:
                            pyautogui.keyUp("left")
                            pyautogui.keyDown("right")
                        case _:
                            pyautogui.keyUp("left")
                            pyautogui.keyUp("right")
            else:
                cv.putText(start_img, "[w] Bot disabled", (400,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

                
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
            if  keyboard.is_pressed("q"):
                cv.destroyAllWindows()
                pyautogui.keyUp("left")
                pyautogui.keyUp("right")
                pyautogui.keyUp("space")
                break
            if keyboard.is_pressed("w"):
                if not self.debounces["w"]:
                    self.inputs["walk_direction"] = 0
                    self.debounces["w"] = True
                    self.bot_enabled = not self.bot_enabled
                    if not self.bot_enabled:
                        pyautogui.keyUp("left")
                        pyautogui.keyUp("right")
                        pyautogui.keyUp("space")
            else:
                self.debounces["w"] = False
                
            if keyboard.is_pressed("r"):
                if not self.debounces["r"]:
                    self.debounces["r"] = True
                    self.game.game_start = False
            else:
                self.debounces["r"] = False
            
    
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
