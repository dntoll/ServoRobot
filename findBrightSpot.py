# import the necessary packages
import numpy as np
import cv2
import glob
import re
from RobotArm import RobotArm
from FakeKit import FakeKit
    
lowerhalfOfImage = np.array([[0, 550], [959, 550], [959, 719], [0, 719]])
fake = FakeKit()
b = RobotArm(fake)
r = 5

X = [] #Position in imaage
TX =[] #Robot arm belief position (forward kinematics)
Y = [] #sev (shoulder, elbow, wrist)

images = glob.glob('images/*.jpg')
"""
image_data = []
for img in images:
    this_image = cv2.imread(img, 1)
    image_data.append(this_image)

avg_image = image_data[0]
for i in range(len(image_data)):
    if i == 0:
        pass
    else:
        alpha = 1.0/(i + 1)
        beta = 1.0 - alpha
        avg_image = cv2.addWeighted(image_data[i], alpha, avg_image, beta, 0.0)

cv2.imshow("Robust", avg_image)
cv2.waitKey(0)
"""
for filename in images:
    # load the image and convert it to grayscale
    image = cv2.imread(filename)
    orig = image.copy()
    red_channel = orig[:,:,2]
    gray = cv2.GaussianBlur(red_channel, (r, r), 0)
    cv2.fillPoly(gray, [lowerhalfOfImage],  color=(0, 0, 0))
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    
    #showImage = gray.copy()
    #cv2.circle(showImage, maxLoc, r, (255, 0, 0), 1)
    # display the results of our newly improved method
    
    
   
    #cv2.imshow("Robust", showImage)
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

import json
with open("robotArmDataSet.json", "w") as fp:
    json.dump([X, TX, Y], fp)
#https://scikit-learn.org/stable/modules/generated/sklearn.cross_decomposition.PLSRegression.html
