import cv2 as cv
import pyautogui 
import numpy as np
import time
import pygetwindow

class llb_bot:
    windows = pygetwindow.getWindowsWithTitle("Calculator")[0]
    img_test = cv.imread('testimg/test2.png',cv.IMREAD_UNCHANGED)
    img_ball = cv.imread('examples/ball/Ball.png',cv.IMREAD_UNCHANGED)
    w, h = img_ball.shape[1::-1]
    coolRect = None
    def __init__(self):
        pass
    def run(self):
        while (True):
            self.coolRect = self.windows._getWindowRect()
            print(self.coolRect)
            #What an beutifull code :))
            screenshot = pyautogui.screenshot()\
                .crop((self.coolRect.left,
                        self.coolRect.top,
                        self.coolRect.right,
                        self.coolRect.bottom))
            open_cv_image = screenshot
            open_cv_image = np.array(screenshot)
            open_cv_image = cv.cvtColor(open_cv_image, cv.COLOR_RGB2BGR)
            # result = cv.matchTemplate(open_cv_image, img_ball, cv.TM_CCOEFF_NORMED)
            # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            # # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            # top_left = max_loc
            # bottom_right = (top_left[0] + w, top_left[1] + h)
            # cv.rectangle(result,top_left, bottom_right, 255, 2)
            time.sleep(0.1)
            cv.imshow('funn.',open_cv_image)
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break