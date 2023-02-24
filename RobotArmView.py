import cv2
import numpy as np
from matplotlib import pyplot as plt
from Vector3 import Vector3

class RobotArmView:

    def __init__(self, robotArm):
        self.arm = robotArm
        self.height = 512
        self.width = 512
        self.target = (0, 0)
        

    def draw(self):
        



        lap = self.arm.lowerArmBone.getPos()
        uap = self.arm.upperArmBone.getPos()
        wp = self.arm.wristBone.getPos()

        bones = (lap, uap, wp)

        start_point = (250, 250)
        color = (0, 255, 0)
        self.img = np.zeros((self.height, self.width, 3), np.uint8)
        for bone in bones:

            bone = bone.mul(-5).add(Vector3(250, 250, 0))
            end_point = (int(bone.x), int(bone.y))
            
            thickness = 1
            image = cv2.line(self.img, start_point, end_point, color, thickness)
            start_point = end_point
        
        viewTarget = (self.target[0] * -5 + 250, self.target[1]*-5+250)
        cv2.circle(self.img, viewTarget, 5, color, thickness)

    def setPos(self, x, y, w):
        self.target = (int(x), int(y))
    def show(self):
        plt.imshow(self.img)
        plt.pause(0.1)

    def showWindow(self):
        plt.show(block=False)
        plt.ion()

    def close(self):
        plt.close('all')

