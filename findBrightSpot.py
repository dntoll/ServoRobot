# import the necessary packages
import numpy as np
import cv2
import glob
import re
from RobotArm import RobotArm


class FakeServo:
    angle = 0

class FakeKit:
    servo = []

    def __init__(self):
        for i in range(16):
            self.servo.append(FakeServo())
    

fake = FakeKit()
b = RobotArm(fake)
r = 5

X = []
TX =[]
Y = []

for filename in glob.glob('images/*.jpg'):
    # load the image and convert it to grayscale
    image = cv2.imread(filename)
    orig = image.copy()
    red_channel = image[:,:,2]
    gray = cv2.GaussianBlur(red_channel, (r, r), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(red_channel)
    
    #image = orig.copy()
    #cv2.circle(image, maxLoc, r, (255, 0, 0), 2)
    # display the results of our newly improved method
    #cv2.imshow("Robust", image)
    #cv2.waitKey(0)
    
    #images\9_s98_e81_w52.jpg
    m = re.search(r'\w*\\\d*_s(\d*)_e(\d*)_w(\d*).jpg', filename)
    s= float(m.group(1))
    e= float(m.group(2))
    w= float(m.group(3))

    b.setState(RobotArm.ROTATE_NORMAL, s,e,w, 0)


    print(s,e,w, "=>", maxLoc, b.wristBone.getPos().x, b.wristBone.getPos().y)

    Y.append([s,e,w])
    X.append(maxLoc)
    TX.append([b.wristBone.getPos().x, b.wristBone.getPos().y])
#https://scikit-learn.org/stable/modules/generated/sklearn.cross_decomposition.PLSRegression.html
from sklearn.cross_decomposition import PLSRegression

pls2 = PLSRegression(n_components=2)
pls2.fit(X, Y)
Y_pred = pls2.predict(X)
#print(Y)
#print(Y_pred)

import matplotlib.pyplot as plt