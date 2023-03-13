from model.Vector3 import Vector3
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


    def getWorldAngleRadians(self):

        relativeAngle = self.joint.getAngleRadians() * self.angleConversion + self.angleAddition
        if self.parent != False:
            return self.parent.getWorldAngleRadians() + relativeAngle
        else:
            return relativeAngle

    def setWorldAngleRadians(self, worldAngle):

        while worldAngle > math.pi*2.0:
            worldAngle -= math.pi*2.0
        while worldAngle < 0:
            worldAngle += math.pi*2.0

        if self.parent != False:
            relativeAngle = worldAngle - self.parent.getWorldAngleRadians()

            actualAngle = (relativeAngle - self.angleAddition)/self.angleConversion
            self.joint.setAngleRadians(actualAngle)
        else:
            self.joint.setAngleRadians(worldAngle)

    def getPos(self):
        worldAngle = self.getWorldAngleRadians()

        if self.parent != False:
            return self.parent.getPos().add( Vector3(math.cos(worldAngle), math.sin(worldAngle), 0).mul(self.length) )
        else:
            return Vector3(math.cos(worldAngle), math.sin(worldAngle), 0).mul(self.length)

    def __str__(self):
        return "<" + str(self.getPos()) + " " + str(self.getWorldAngle()) + ">"
