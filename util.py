import cv2

def test():
    img_test = cv2.imread('testimg/test4',0)
    cv2.imshow('graycsale image',img_test)
    cv2.waitKey(0)