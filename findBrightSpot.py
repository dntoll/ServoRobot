# import the necessary packages
import numpy as np
import cv2
import glob
import re

r = 5

image_list = []

for filename in glob.glob('images/*.jpg'):
    # load the image and convert it to grayscale
    image = cv2.imread(filename)
    orig = image.copy()
    red_channel = image[:,:,2]
    gray = cv2.GaussianBlur(red_channel, (r, r), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(red_channel)
    image = orig.copy()
    #cv2.circle(image, maxLoc, r, (255, 0, 0), 2)
    # display the results of our newly improved method
    #cv2.imshow("Robust", image)
    #cv2.waitKey(0)

    m = re.search(r'\w*\\\d*_s(\d*)_e(\d*)_w(\d*).jpg', filename)
    s= float(m.group(1))
    e= float(m.group(2))
    w= float(m.group(3))
    print(s,e,w, "=>", maxLoc)