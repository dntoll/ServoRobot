import cv2
import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH, ttk
from model.Vector3 import Vector3
from view.KeyView import KeyView
from view.MouseView import MouseView

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
        
        self.wantsReplay = False
        self.wantsToSave = False
        self.wantsToRemove = False
        

    def initUI(self):
        
        self.root.geometry(str(self.width) + "x" + str(self.height))

        self.master.title("Robot")
        self.pack(fill=BOTH, expand=1)


        ttk.Button(self, text="Quit", command=self.root.destroy)

        self.canvas = Canvas(self)

        self.keyView = KeyView(self.canvas, self.controller)
        self.mouseView = MouseView(self.canvas, self.controller, self.root, self.leftViewMiddlePoint, self.rightViewMiddlePoint, self.width, self.scale)

        self.canvas.pack(fill=BOTH, expand=1)    
        self.focus_set()
        

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
    

