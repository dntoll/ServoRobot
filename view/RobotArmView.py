import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from model.Vector3 import Vector3
from view.KeyView import KeyView
from view.MouseView import MouseView
from view.RobotEditorView import RobotEditorView
from model.RobotArm import RobotArm
from model.FakeKit import FakeKit    
from Lib import copy

import math

class RobotArmView(tk.Frame):

    def __init__(self, robotArm, root, recording, controller):
        super().__init__()
        self.arm = robotArm
        self.height = 1024
        self.width = 1024
        self.controller = controller
        self.leftViewMiddlePoint = (self.width/4, self.height /4)
        self.rightViewMiddlePoint = (self.width/4, 3*self.height / 4)
        self.debug = "hej"
        
        self.recording = recording
        self.lastState = robotArm.getState()
        self.wantsToAppend = True
        self.scale = -5
        
        self.root = root
        self.initUI()
        
        

    def initUI(self):
        
        self.root.geometry(str(self.width) + "x" + str(self.height))

        self.master.title("Robot")
        self.pack(fill=tk.BOTH, expand=1)


        ttk.Button(self, text="Quit", command=self.root.destroy)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.editor_view = RobotEditorView(self, self.recording.recording, self.controller)
        self.editor_view.pack(side=tk.RIGHT, fill=tk.Y)

        self.keyView = KeyView(self, self.controller)
        self.mouseView = MouseView(self.canvas, self.controller, self.root, self.leftViewMiddlePoint, self.rightViewMiddlePoint, self.height, self.scale)

        self.canvas.pack(fill=tk.BOTH, expand=1)    
        self.focus_set()
        

    def draw(self):
        lap = self.arm.lowerArmBone.getPos()
        uap = self.arm.upperArmBone.getPos()
        wp = self.arm.wristBone.getPos()
        bones = (lap, uap, wp)

        self.canvas.delete('all')

        

            
        start_point = self.leftViewMiddlePoint
        pos = str(int(wp.x*10)/10) + ", " + str(int(wp.y*10)/10)
        self.canvas.create_text(start_point[0], start_point[1]-30, text=pos, fill="black", font=('Helvetica 9'))
        start_point = self.rightViewMiddlePoint
        

        
        self.drawSideView(bones)

        #Draw a clock like directional 
        self.drawTopView()

             
    
        self.root.update_idletasks()
        self.root.update()

    def drawSideView(self, bones):
        

        for state in self.recording.recording:
            r = RobotArm(FakeKit())
            r.setState(state)
            
            self.drawRobot(self.leftViewMiddlePoint, r, "gray")    


        self.drawRobot(self.leftViewMiddlePoint, self.arm, "red")

        start_point = self.leftViewMiddlePoint

        #Ground
        self.canvas.create_line(0, start_point[1]-self.scale*5, self.width/2, start_point[1] -self.scale*5)
        

    def drawRobot(self, start_point, arm, color):
        r = arm
        lap = r.lowerArmBone.getPos()
        uap = r.upperArmBone.getPos()
        wp = r.wristBone.getPos()
        bones = (lap, uap, wp)
        for bone in bones:
            bone = bone.mul(self.scale).add(Vector3(self.leftViewMiddlePoint[0], self.leftViewMiddlePoint[1], 0))
            end_point = (int(bone.x), int(bone.y))
            
            thickness = 1
            self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1], fill=color)
            start_point = end_point


    def drawTopView(self):
        
        start_point = self.rightViewMiddlePoint
        v = -60/360/(2.0*math.pi)
        length = 30 * self.scale
        end_point = (self.rightViewMiddlePoint[0] +  math.cos(v) * length, math.sin(v) * length + self.rightViewMiddlePoint[1])
        self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])


        v = -self.arm.rotate.getAngleRadians()
        length = self.arm.getState().distanceFromBase * self.scale
        end_point = (self.rightViewMiddlePoint[0] +  math.cos(v) * length, math.sin(v) * length + self.rightViewMiddlePoint[1])
        self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1])
        pos = str(self.arm.rotate.getAngleRadians())
        self.canvas.create_text(start_point[0], start_point[1]-30, text=pos, fill="black", font=('Helvetica 9'))


        self.canvas.create_text(20, 20, text=self.debug, fill="red", font=('Helvetica 9 bold'))

    
    def userWantsReplay(self):
        return self.wantsReplay
    
    def userWantsToSave(self):
        if self.wantsToSave:
            self.wantsToSave = False
            return True
        return False
    

