from Vector3 import Vector3
import math

class Bone:        
        
    def __init__(self, joint, length, angleConversion, angleAddition):
        self.joint = joint
        self.length = length
        self.parent = False
        self.angleConversion = angleConversion
        self.angleAddition = angleAddition


    def setParent(self, parent):
        self.parent = parent


    def getWorldAngle(self):

        relativeAngle = self.joint.getAngleRadians() * self.angleConversion + self.angleAddition
        if self.parent != False:
            return self.parent.getWorldAngle() + relativeAngle
        else:
            return relativeAngle

    def getPos(self):
        worldAngle = self.getWorldAngle()

        if self.parent != False:
            return self.parent.getPos().add( Vector3(math.cos(worldAngle), math.sin(worldAngle), 0).mul(self.length) )
        else:
            return Vector3(math.cos(worldAngle), math.sin(worldAngle), 0).mul(self.length)

    def __str__(self):
        return "<" + str(self.getPos()) + " " + str(self.getWorldAngle()) + ">"
