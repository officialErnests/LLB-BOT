import cv2 as cv
import pyautogui 
import numpy as np
import time
import pygetwindow
from LLBlaze import *
from Real_utils import *

class window_cut:
    top = 31
    right = 7
    bottom = 7
    left = 7

class llb_bot:
    windows = None
    img_test = cv.imread('testimg/test1.png',cv.IMREAD_UNCHANGED)
    img_ball = cv.imread('examples/ball/Ball.png',cv.IMREAD_UNCHANGED)
    w, h = img_ball.shape[1::-1]
    coolRect = None
    window_set = False

    game = gamedata(vector2D(100,100))

    def __init__(self, windowName):
        if len(pygetwindow.getWindowsWithTitle(windowName)):
            self.windows = pygetwindow.getWindowsWithTitle(windowName)[0]
            self.window_set = True
    
    def run(self):
        x = 0
        while (True):
            x+=1

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
            
            self.game.ball.state = 0

            #detection
            #BLUE
            self.get_color(start_img, img_hsv_value, 1,
                                    np.array([105, 244, 255]),
                                    np.array([105, 243, 255]))
            #RED
            self.get_color(start_img, img_hsv_value, 2,
                                    np.array([5, 230, 255]),
                                    np.array([5, 229, 255]))
            match self.game.ball.state:
                case 1:
                    cv.putText(start_img, "Blue ball", (100,300), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 4)
                    pass
                case 2:
                    cv.putText(start_img, "Red ball", (100,300), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 4)
                    pass
                case _:
                    cv.putText(start_img, "No ball", (100,300), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 4)
                    pass
            
            #update game
            self.game.update(start_img)

            #display
            cv.imshow('funn.',start_img)
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
    
    def get_color(self, start_img, hsv_img, ball_stage, mask_upper_red, mask_lower_red):
        color = (255, 255, 0) if ball_stage == 1 else (0, 0, 255)
        masked_screenshot = cv.inRange(hsv_img, mask_lower_red, mask_upper_red)
        ret,thresh = cv.threshold(masked_screenshot,254,255,0)
        movement = cv.moments(thresh)
        if movement['m00'] > 0:
            cX = int(movement["m10"] / movement["m00"])
            cY = int(movement["m01"] / movement["m00"])
            cv.circle(start_img, (cX, cY), 20, (255, 255, 255), -1)
            cv.circle(start_img, (cX, cY), 10, (0, 0, 0), -1)
            cv.circle(start_img, (cX, cY), 5, color, -1)
            cv.putText(start_img, "x:" + str(cX) + " y:"+ str(cY), (100,100), cv.FONT_HERSHEY_SIMPLEX, 1, color, 4)
            self.game.ball.state = ball_stage
            self.game.ball.position = vector2D(cX, cY)