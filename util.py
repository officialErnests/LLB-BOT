import cv2 as cv
import pyautogui 
import numpy as np
import time
import pygetwindow



class llb_bot:
    windows = None
    img_test = cv.imread('testimg/test4.png',cv.IMREAD_UNCHANGED)
    img_ball = cv.imread('examples/ball/Ball.png',cv.IMREAD_UNCHANGED)
    w, h = img_ball.shape[1::-1]
    coolRect = None
    window_set = False
    def __init__(self, windowName):
        if len(pygetwindow.getWindowsWithTitle(windowName)):
            self.windows = pygetwindow.getWindowsWithTitle(windowName)[0]
            self.window_set = True
        
    def run(self):
        x = 0
        while (True):
            x+=1
            img_hsv_value = None
            if self.window_set:
                self.coolRect = self.windows._getWindowRect()
                # print(self.coolRect)
                #What an beutifull code :))
                
                screenshot = pyautogui.screenshot()\
                    .crop((self.coolRect.left,
                            self.coolRect.top,
                            self.coolRect.right,
                            self.coolRect.bottom))
                open_cv_screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
                img_hsv_value = cv.cvtColor(open_cv_screenshot, cv.COLOR_BGR2HSV)
            else:
                img_hsv_value = cv.cvtColor(self.img_test, cv.COLOR_BGR2HSV)
            #209, 95, 100
            #Why does it have 0-179
            #Also why is it default GBR
            #at the end i spend like 3min manualy homing in :))
            mask_upper = np.array([105, 244, 255])
            mask_lower = np.array([105, 243, 255])
            masked_screenshot = cv.inRange(img_hsv_value, mask_lower, mask_upper)
            # time.sleep(0.1)
            contours, hierarchy = cv.findContours(masked_screenshot,
                      cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            # cv.findContours(masked_screenshot, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE, countours)
            # print(contours)
            # cv.rectangle(masked_screenshot,contours, bottom_right, 255, 2)
            movement = cv.moments(contours)
            movement_point = 
            cv.putText(masked_screenshot, str(x), (100,100), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 4)
            cv.imshow('funn.',movement)
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break