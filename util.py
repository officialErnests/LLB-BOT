import cv2 as cv
import pyautogui 
import numpy as np
import time

def test():
    img_test = cv.imread('testimg/test2.png',cv.IMREAD_UNCHANGED)
    img_ball = cv.imread('examples/ball/Ball.png',cv.IMREAD_UNCHANGED)
    w, h = img_ball.shape[1::-1]

    while (True):
        screenshot = pyautogui.get_screenshot()
        open_cv_image = screenshot
        open_cv_image = np.array(screenshot)
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
