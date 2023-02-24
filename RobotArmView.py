import cv2
import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from Vector3 import Vector3

class RobotArmView(Frame):

    def __init__(self, robotArm, root):
        super().__init__()
        self.arm = robotArm
        self.height = 256
        self.width = 1024
        self.leftViewMiddlePoint = (256, 256)
        self.rightViewMiddlePoint = (768, 256)
        root.geometry(str(self.width) + "x" + str(self.height))
        self.target = (0, 0)
        self.scale = -5
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

        start_point = self.leftViewMiddlePoint
        
        for bone in bones:
            bone = bone.mul(self.scale).add(Vector3(self.leftViewMiddlePoint[0], self.leftViewMiddlePoint[1], 0))
            end_point = (int(bone.x), int(bone.y))
            
            thickness = 1
            self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
            start_point = end_point
        
        
        start_point = self.rightViewMiddlePoint
        
        for bone in bones:
            bone = bone.mul(self.scale).add(Vector3(self.rightViewMiddlePoint[0], self.rightViewMiddlePoint[1], 0))
            end_point = (int(bone.x), int(bone.z))
            
            thickness = 1
            self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
            start_point = end_point
        #viewTarget = (self.target[0] * -5 + 250, self.target[1]*-5+250)
        #self.canvas.create_arc(viewTarget[0], viewTarget[1], viewTarget[0], viewTarget[1])
        #cv2.circle(self.img, viewTarget, 5, color, thickness)

        self.root.update_idletasks()
        self.root.update()

    def setPos(self, x, y, w):
        self.target = (int(x), int(y))

    def hasNewTargetPosition(self):
        
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 20
        if abs_coord_x < 0 or abs_coord_y < 0 or abs_coord_x > self.width or abs_coord_y > self.height:
            return False
        return True
    
    def getTargetPosition(self):
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 20

        robotX = (abs_coord_x - self.leftViewMiddlePoint[0])/self.scale
        robotY = (abs_coord_y - self.leftViewMiddlePoint[1])/self.scale
        return (robotX,robotY,0)

    

