import cv2
import numpy as np
from matplotlib import pyplot as plt
from Vector3 import Vector3

class RobotArmView:

    def __init__(self, robotArm):
        self.arm = robotArm

    def draw(self):
        

        height = 512
        width = 512
        img = np.zeros((height,width,3), np.uint8)

        lap = self.arm.lowerArmBone.getPos()
        uap = self.arm.upperArmBone.getPos()
        wp = self.arm.wristBone.getPos()

        bones = (lap, uap, wp)

        start_point = (250, 250)

        for bone in bones:

            bone = bone.mul(5).add(Vector3(250, 250, 0))
            end_point = (int(bone.x), int(bone.y))
            color = (0, 255, 0)
            thickness = 9
            image = cv2.line(img, start_point, end_point, color, thickness)
            start_point = end_point

        plt.imshow(img)

