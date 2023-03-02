import cv2
import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from Vector3 import Vector3
from RobotArm import RobotArm

import math

class RobotArmView(Frame):

    def __init__(self, robotArm, root):
        super().__init__()
        self.arm = robotArm
        self.height = 384
        self.width = 1024
        self.leftViewMiddlePoint = (self.width/4, 2* self.height /3)
        self.rightViewMiddlePoint = (3*self.width/4, self.height / 2)
        root.geometry(str(self.width) + "x" + str(self.height))
        self.debug = "hej"

        self.lastState = robotArm.getState()
        self.scale = -5
        self.initUI()
        self.root = root
        self.hasNewState = False
        self.gripIsOpen = False
        self.wristIsControlled = False


    def initUI(self):
        self.master.title("Robot")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.bind('<B1-Motion>', self.mouseMoveWithButtonDown)
        self.canvas.bind('<Button-1>', self.mouseMoveWithButtonDown)
        self.canvas.bind('<MouseWheel>', self.wrist)
        self.canvas.bind('<Button-2>', self.stopWristFromControl)
        self.canvas.bind('<Button-3>', self.grip)
        self.canvas.pack(fill=BOTH, expand=1)    
    
    def stopWristFromControl(self, event):
        self.wristIsControlled = False

    def wrist(self, event):
        
        distanceMove = 0.17
        if event.delta > 0:
            self.lastState.wristWorldAngleRadians = self.arm.getState().wristWorldAngleRadians +distanceMove
        else:
            self.lastState.wristWorldAngleRadians = self.arm.getState().wristWorldAngleRadians -distanceMove

        self.wristIsControlled = True
        self.hasNewState = True

        print("arm state", self.arm.getState().wristWorldAngleRadians, flush=True)
        print("target state", self.lastState.wristWorldAngleRadians, flush=True)

    def grip(self, event):
        if self.gripIsOpen:
            self.lastState.grip = RobotArm.GRIP_OPEN
        else:
            self.lastState.grip = RobotArm.GRIP_CLOSED
        self.hasNewState = True
        self.gripIsOpen = not self.gripIsOpen
        

    def mouseMoveWithButtonDown(self, event):
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x() -10
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 30

        if self.wristIsControlled is False:

            ydiff = self.leftViewMiddlePoint[1]-150 - abs_coord_y
            xdiff = self.leftViewMiddlePoint[0] - abs_coord_x
            angle = math.atan2(ydiff, xdiff)
            self.lastState.wristWorldAngleRadians = angle

        if abs_coord_x < self.width/2:
            robotX = (abs_coord_x - self.leftViewMiddlePoint[0])/self.scale
            robotY = (abs_coord_y - self.leftViewMiddlePoint[1])/self.scale

            

            self.lastState.distanceFromBase = robotX
            self.lastState.heightOverBase = robotY
            self.hasNewState = True
        else:
            #mouse is on the right side
            x = abs_coord_x - self.rightViewMiddlePoint[0]
            y = abs_coord_y - self.rightViewMiddlePoint[1]

            distance = - math.sqrt(x*x + y*y) / self.scale

            rotationAngle = math.atan2(y, -x)
            while rotationAngle < 0:
                rotationAngle += 6.28

                

            self.lastState.rotationRadians = rotationAngle
            self.lastState.distanceFromBase = distance
            self.hasNewState = True
        

        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0

    def draw(self):
        lap = self.arm.lowerArmBone.getPos()
        uap = self.arm.upperArmBone.getPos()
        wp = self.arm.wristBone.getPos()

        

        bones = (lap, uap, wp)

        self.canvas.delete('all')

        start_point = self.leftViewMiddlePoint

        #Ground
        self.canvas.create_line(0, start_point[1]-self.scale*5, self.width/2, start_point[1] -self.scale*5)
        
        for bone in bones:
            bone = bone.mul(self.scale).add(Vector3(self.leftViewMiddlePoint[0], self.leftViewMiddlePoint[1], 0))
            end_point = (int(bone.x), int(bone.y))
            
            thickness = 1
            self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
            start_point = end_point

            
        
        pos = str(int(wp.x*10)/10) + ", " + str(int(wp.y*10)/10)
        self.canvas.create_text(start_point[0], start_point[1]-30, text=pos, fill="black", font=('Helvetica 9'))
        start_point = self.rightViewMiddlePoint
        

        v = -60/360/(2.0*math.pi)
        len = 30 * self.scale
        end_point = (self.rightViewMiddlePoint[0] +  math.cos(v) * len, math.sin(v) * len + self.rightViewMiddlePoint[1])
        self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])

        #Draw a clock like directional 
        v = -self.arm.rotate.getAngleRadians()
        len = self.arm.getState().distanceFromBase * self.scale
        end_point = (self.rightViewMiddlePoint[0] +  math.cos(v) * len, math.sin(v) * len + self.rightViewMiddlePoint[1])
        self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
        pos = str(self.arm.rotate.getAngleRadians())
        self.canvas.create_text(start_point[0], start_point[1]-30, text=pos, fill="black", font=('Helvetica 9'))

        self.canvas.create_text(20, 20, text=self.debug, fill="red", font=('Helvetica 9 bold'))
             
    
        self.root.update_idletasks()
        self.root.update()

    

    def hasNewTargetState(self):
        
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 30


        if abs_coord_x < 0 or abs_coord_y < 0 or abs_coord_x > self.width or abs_coord_y > self.height:
            return False
        
        return self.hasNewState
    
    def getTargetState(self):
        self.hasNewState = False
        return self.lastState

