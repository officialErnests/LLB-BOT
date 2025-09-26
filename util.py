import cv2 as cv

def test():
    img_test = cv.imread('testimg/test2.png',cv.IMREAD_UNCHANGED)
    img_ball = cv.imread('examples/ball/Ball.png',cv.IMREAD_UNCHANGED)
    w, h = img_ball.shape[1::-1]
    # 0c88ff
 
    result = cv.matchTemplate(img_test, img_ball, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(result,top_left, bottom_right, 255, 2)
    cv.imshow('graycsale image',result)
    cv.waitKey(0)
