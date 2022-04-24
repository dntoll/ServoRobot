
from ServoJoint import ServoJoint

from Bone import Bone



import time 
import math 

class RobotArm:
    

    ROTATE_FULLY_LEFT = 180
    ROTATE_FULLY_RIGHT = 0
    ROTATE_NORMAL = 60

    GRIP_CLOSED = 180
    GRIP_OPEN = 60

    ELBOW_90_DEG = 90
    ELBOW_FULLY_OPEN = 10
    ELBOW_FULLY_CLOSED = 180

    SHOULDER_FORWARD = 60
    SHOULDER_UP = 90
    SHOULDER_BACKWARD = 145

    WRIST_FULLY_DOWN = 0
    WRIST_NEUTRAL = 90
    WRIST_FULLY_UP = 180

    def __init__(self, kit):
        self.kit = kit
        self.rotate = ServoJoint(self.kit, 15, 0, 60, 180)
        self.shoulder = ServoJoint(self.kit, 8, 60, 90, 145)
        self.elbow = ServoJoint(self.kit, 4, 10, 90, 180)
        self.wrist = ServoJoint(self.kit, 0, 0, 90, 180)
        self.grip = ServoJoint(self.kit, 12, 60, 120, 180)

        self.lowerArmBone = Bone(self.shoulder, 20, 1.0, 0)
        self.upperArmBone = Bone(self.elbow, 20, -1.0, 0)
        self.wristBone =    Bone(self.wrist, 5, 1.0, -math.pi/2)

        self.upperArmBone.setParent(self.lowerArmBone)  
        self.wristBone.setParent(self.upperArmBone)
    
        
        
    def setState(self, rotate, shoulder, elbow, wrist, grip):
        self.Rotate(rotate)
        self.Shoulder(shoulder)
        self.Elbow(elbow)
        self.Wrist(wrist)
        self.Grip(grip)

        print("shoulder straight", self.wristBone)

    
    def Shoulder(self, angle):
        self.shoulder.setAngle(angle)

    def Grip(self, angle):
        self.grip.setAngle(angle)

    def Wrist(self, angle):
        self.wrist.setAngle(angle)

    def Elbow(self, angle):
        self.elbow.setAngle(angle)

    def Rotate(self, angle):
        self.rotate.setAngle(angle)

    def demo(self):
        self.Grip(self.GRIP_OPEN)
        time.sleep(1.5)
        self.Grip(self.GRIP_CLOSED)
        time.sleep(1.5)
        self.Grip(self.GRIP_OPEN)
        

        time.sleep(1.5)
        self.Wrist(self.WRIST_FULLY_DOWN)
        print("wrist down", self.wristBone)
        time.sleep(1.5)
        self.Wrist(self.WRIST_FULLY_UP)
        print("wrist up", self.wristBone)
        time.sleep(1.5)
        self.Wrist(self.WRIST_NEUTRAL)
        print("wrist neutral", self.wristBone)

        time.sleep(1.5)
        self.Elbow(self.ELBOW_FULLY_OPEN)
        print("elbow open", self.wristBone)
        time.sleep(1.5)
        self.Elbow(self.ELBOW_FULLY_CLOSED)
        print("elbow closed", self.wristBone)
        time.sleep(1.5)
        self.Elbow(self.ELBOW_90_DEG)
        print("wrist neutral", self.wristBone)

        time.sleep(1.5)
        self.Shoulder(self.SHOULDER_FORWARD)
        print("shoulder forward", self.wristBone)
        time.sleep(1.5)
        self.Shoulder(self.SHOULDER_BACKWARD)
        print("shoulder back", self.wristBone)
        time.sleep(1.5)
        self.Shoulder(self.SHOULDER_UP)
        print("shoulder straight", self.wristBone)

        time.sleep(1.5)
        self.Rotate(self.ROTATE_FULLY_LEFT)
        time.sleep(1.5)
        self.Rotate(self.ROTATE_FULLY_RIGHT)
        time.sleep(1.5)
        self.Rotate(self.ROTATE_NORMAL)

        