import math


class ServoJoint:
    def __init__(self, kit, servoIndex, min, neutral, max):
        self.kit = kit
        self.index = servoIndex
        self.min = min 
        self.neutral = neutral
        self.max = max

        self.setAngle(self.neutral)

    def setAngle(self, newAngle):
        if newAngle < self.min:
            newAngle = self.min
        if newAngle > self.max:
            newAngle = self.max

        self.kit.servo[self.index].angle = newAngle
        self.lastKnownAngle = newAngle

    
    def getAngleRadians(self):
        return self.lastKnownAngle * math.pi * 2.0 / 360.0
    
    def addJoint(self, where, howRotate, joint):
        self.whereIsJointAttached = where
        self.howDoesItRotateAround = howRotate

