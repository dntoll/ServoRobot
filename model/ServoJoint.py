import math


class ServoJoint:
    def __init__(self, kit, servoIndex, min, neutral, max):
        self.kit = kit
        self.index = servoIndex
        self.min = min 
        self.neutral = neutral
        self.max = max
        self.lastKnownAngle = neutral
        self.targetAngle = neutral
        self.setAngleDegrees(self.neutral)


    def setInterpolation(self, interpolatedValue):
        myRange = self.max - self.min
        angle = self.min + interpolatedValue * myRange

        self.setAngleDegrees(angle)

    def setAngleDegrees(self, newAngle):

        while newAngle < 0:
            newAngle = newAngle + 360
        while newAngle > 360:
            newAngle = newAngle - 360

        if newAngle < self.min:
            #print("minValue found", self.index, newAngle , self.min, flush=True)
            newAngle = self.min
        if newAngle > self.max:
            #print("maxValue found", self.index, newAngle , self.max, flush=True)
            newAngle = self.max
        
        
        self.targetAngle = newAngle

    def setAngleRadians(self, radians):
        degrees = (radians * 360.0) / (2.0 * math.pi)
        self.setAngleDegrees(degrees)
    
    def getAngleDegrees(self):
        return self.targetAngle

    def getAngleRadians(self):
        return self.targetAngle * math.pi * 2.0 / 360.0
    
    def addJoint(self, where, howRotate, joint):
        self.whereIsJointAttached = where
        self.howDoesItRotateAround = howRotate

    def update(self):

        isDone = False
        maxChangeAngle = 2
        if self.targetAngle > self.lastKnownAngle + maxChangeAngle:
            self.lastKnownAngle += maxChangeAngle
        elif self.targetAngle < self.lastKnownAngle - maxChangeAngle :
            self.lastKnownAngle -= maxChangeAngle
        else:
            self.lastKnownAngle = self.targetAngle
            isDone = True
            
        try:
            self.kit.servo[self.index].angle = self.lastKnownAngle
            
        except Exception as e:
            print("ServoJoint.update:", e, self.index, self.lastKnownAngle)
        
        return isDone
        

