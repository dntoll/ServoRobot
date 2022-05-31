import cv2
import numpy as np
from matplotlib import pyplot as plt
from Vector3 import Vector3

class RobotArmView:

    def __init__(self, robotArm):
        self.arm = robotArm
        height = 512
        width = 512
        self.img = np.zeros((height,width,3), np.uint8)

    def draw(self):
        



        lap = self.arm.lowerArmBone.getPos()
        uap = self.arm.upperArmBone.getPos()
        wp = self.arm.wristBone.getPos()

        bones = (lap, uap, wp)

        start_point = (250, 250)
        color = (0, 255, 0)

        for bone in bones:

            bone = bone.mul(-5).add(Vector3(250, 250, 0))
            end_point = (int(bone.x), int(bone.y))
            
            thickness = 1
            image = cv2.line(self.img, start_point, end_point, color, thickness)
            start_point = end_point
    def show(self):
        plt.imshow(self.img)

