import cv2
import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH, ttk
from model.Vector3 import Vector3
from model.RobotArm import RobotArm
from Lib import copy

import math

class RobotArmView(Frame):

    def __init__(self, robotArm, root, recording, controller):
        super().__init__()
        self.arm = robotArm
        self.height = 384
        self.width = 1024
        self.controller = controller
        self.leftViewMiddlePoint = (self.width/4, 2* self.height /3)
        self.rightViewMiddlePoint = (3*self.width/4, self.height / 2)
        self.debug = "hej"
        
        self.recording = recording
        self.lastState = robotArm.getState()
        self.wantsToAppend = True

        self.scale = -5
        self.root = root
        self.initUI()
        
        self.gripIsOpen = False
        self.wristIsControlled = False
        self.wantsReplay = False
        self.wantsToSave = False
        self.wantsToRemove = False
        

    def initUI(self):
        
        self.root.geometry(str(self.width) + "x" + str(self.height))

        self.master.title("Robot")
        self.pack(fill=BOTH, expand=1)


        ttk.Button(self, text="Quit", command=self.root.destroy)

        self.canvas = Canvas(self)
        self.canvas.bind('<B1-Motion>', self.mouseMoveWithButtonDown)
        self.canvas.bind('<Button-1>', self.mouseMoveWithButtonDown)
        self.canvas.bind('<MouseWheel>', self.wrist)
        self.canvas.bind('<Button-2>', self.stopWristFromControl)
        self.canvas.bind('<Button-3>', self.grip)
        #self.bind('<KeyPress>', self.key_released )
        self.bind('<KeyRelease>', self.key_released )
        self.canvas.pack(fill=BOTH, expand=1)    
        self.focus_set()
    
    def stopWristFromControl(self, event):
        self.wristIsControlled = False

    def key_released(self, event):
        if event.char == 's':
            self.controller.save()
        elif event.char == 'r':
            self.wantsReplay = True
        elif event.char == 'c':
            self.controller.duplicateCurrentState()
        elif event.char == 'n':
            self.controller.setStateToRelax()
        elif event.char == 'd':
            self.controller.removeCurrentState()
        elif event.char == '+':
            self.controller.incrementState()
        elif event.char == '-':
            self.controller.decrementState()
        elif event.char > '0' and event.char < '9':
            num = int(event.char)
            distanceMoved = 0.5
            if num == 2:
                self.controller.alterState(0.0, -distanceMoved, 0.0, 0.0)
            elif num == 8:
                self.controller.alterState(0.0, distanceMoved, 0.0, 0.0)
            elif num == 4:
                self.controller.alterState(distanceMoved, 0.0, 0.0, 0.0)
            elif num == 6:
                self.controller.alterState(-distanceMoved, 0.0, 0.0, 0.0)
            else:
                return
            self.hasNewState = True


    def wrist(self, event):
        
        distanceMove = 0.17
        if event.delta > 0:
            self.controller.alterState(0, 0.0, 0.0, distanceMove)
        else:
            self.controller.alterState(0, 0.0, 0.0, -distanceMove)

        
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
            print("ydiff, xdiff, angle", ydiff, xdiff, angle*360/2.0*3.14)
            
            self.controller.setWrist(angle)
        if abs_coord_x < self.width/2:
            robotX = (abs_coord_x - self.leftViewMiddlePoint[0])/self.scale
            robotY = (abs_coord_y - self.leftViewMiddlePoint[1])/self.scale

            
            self.controller.setDistanceHeight(robotX, robotY)
            
        else:
            #mouse is on the right side
            x = abs_coord_x - self.rightViewMiddlePoint[0]
            y = abs_coord_y - self.rightViewMiddlePoint[1]

            distance = - math.sqrt(x*x + y*y) / self.scale

            rotationAngle = math.atan2(y, -x)
            while rotationAngle < 0:
                rotationAngle += 6.28

                
            self.controller.setDistanceRotation(distance, rotationAngle)        

        

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
        length = 30 * self.scale
        end_point = (self.rightViewMiddlePoint[0] +  math.cos(v) * length, math.sin(v) * length + self.rightViewMiddlePoint[1])
        self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])

        #Draw a clock like directional 
        v = -self.arm.rotate.getAngleRadians()
        length = self.arm.getState().distanceFromBase * self.scale
        end_point = (self.rightViewMiddlePoint[0] +  math.cos(v) * length, math.sin(v) * length + self.rightViewMiddlePoint[1])
        self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
        pos = str(self.arm.rotate.getAngleRadians())
        self.canvas.create_text(start_point[0], start_point[1]-30, text=pos, fill="black", font=('Helvetica 9'))


        self.canvas.create_text(20, 20, text=self.debug, fill="red", font=('Helvetica 9 bold'))

        #RecordingView
        i = 0
        for x in self.recording.recording:
            recording = str(x)
            
            
            self.canvas.create_text(self.width/2, 30 + i*10, text=recording, fill="red", font=('Helvetica 9 bold'))
            if self.recording.wantsToAppend is False and self.recording.editIndex == i:
                self.canvas.create_text(self.width/2 -120, 30+i*10, text="*", fill="red", font=('Helvetica 9 bold'))
            i += 1
             
    
        self.root.update_idletasks()
        self.root.update()

    
    def userWantsReplay(self):
        return self.wantsReplay
    
    def userWantsToSave(self):
        if self.wantsToSave:
            self.wantsToSave = False
            return True
        return False
    

