import cv2
import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from Vector3 import Vector3

class RobotArmView(Frame):

    def __init__(self, robotArm, root):
        super().__init__()
        self.arm = robotArm
        self.height = 512
        self.width = 512
        self.target = (0, 0)
        self.initUI()
        self.root = root


    def initUI(self):
        self.master.title("Robot")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)    

    def draw(self):
        lap = self.arm.lowerArmBone.getPos()
        uap = self.arm.upperArmBone.getPos()
        wp = self.arm.wristBone.getPos()

        bones = (lap, uap, wp)

        self.canvas.delete('all')
        start_point = (250, 250)
        for bone in bones:

            bone = bone.mul(-5).add(Vector3(250, 250, 0))
            end_point = (int(bone.x), int(bone.y))
            
            thickness = 1
            self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
            start_point = end_point
        
        viewTarget = (self.target[0] * -5 + 250, self.target[1]*-5+250)
        self.canvas.create_arc(viewTarget[0], viewTarget[1], viewTarget[0], viewTarget[1])
        #cv2.circle(self.img, viewTarget, 5, color, thickness)

        self.root.update_idletasks()
        self.root.update()

    def setPos(self, x, y, w):
        self.target = (int(x), int(y))
    

