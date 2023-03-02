import cv2
import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from Vector3 import Vector3
import math

class RobotArmView(Frame):

    def __init__(self, robotArm, root):
        super().__init__()
        self.arm = robotArm
        self.height = 256
        self.width = 768
        self.leftViewMiddlePoint = (self.width/4, 256)
        self.rightViewMiddlePoint = (3*self.width/4, self.height / 2)
        root.geometry(str(self.width) + "x" + str(self.height))


        self.lastState = robotArm.getState()
        self.scale = -5
        self.initUI()
        self.root = root


    def initUI(self):
        self.master.title("Robot")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.bind('<B1-Motion>', self.mouseMoveWithButtonDown)
        self.canvas.pack(fill=BOTH, expand=1)    

    def mouseMoveWithButtonDown(self, event):
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 20


        if abs_coord_x < self.width/2:
            robotX = (abs_coord_x - self.leftViewMiddlePoint[0])/self.scale
            robotY = (abs_coord_y - self.leftViewMiddlePoint[1])/self.scale

            self.lastState.distanceFromBase = robotX
            self.lastState.heightOverBase = robotY
        else:
            #mouse is on the right side
            x = abs_coord_x - self.rightViewMiddlePoint[0]
            y = abs_coord_y - self.rightViewMiddlePoint[1]

            rotationAngle = -math.atan2(y, x)
            while rotationAngle < 0:
                rotationAngle += 6.28

            self.rotationRadians = rotationAngle

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
        
        #Draw a clock like directional 
        v = -self.arm.rotate.getAngleRadians()
        len = 120
        end_point = (self.rightViewMiddlePoint[0] +  math.cos(v) * len, math.sin(v) * len + self.rightViewMiddlePoint[1])
        self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
    
        self.root.update_idletasks()
        self.root.update()

    

    def hasNewTargetPosition(self):
        
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 20


        if abs_coord_x < 0 or abs_coord_y < 0 or abs_coord_x > self.width or abs_coord_y > self.height:
            return False
        
        return True
    
    def getTargetPosition(self):
        
        return self.lastSetPosition

