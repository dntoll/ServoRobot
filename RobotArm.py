from ServoJoint import ServoJoint
from RobotState import RobotState
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
        self.rotate = ServoJoint(self.kit, 15, self.ROTATE_FULLY_RIGHT, self.ROTATE_NORMAL, self.ROTATE_FULLY_LEFT)
        self.shoulder = ServoJoint(self.kit, 8, 30, 90, 160)
        self.elbow = ServoJoint(self.kit, 5, 10, 90, 180)
        self.wrist = ServoJoint(self.kit, 0, 0, 90, 180)
        self.grip = ServoJoint(self.kit, 12, 60, 120, 180)

        self.lowerArmBone = Bone(self.shoulder, 20, 1.0, 0)
        self.upperArmBone = Bone(self.elbow, 20, -1.0, 0)
        self.wristBone =    Bone(self.wrist, 5, 1.0, -math.pi/2)

        self.upperArmBone.setParent(self.lowerArmBone)  
        self.wristBone.setParent(self.upperArmBone)
    
        
        
    #def setState(self, rotate, shoulder, elbow, wrist, grip):
    #    self.Rotate(rotate)
    #    self.Shoulder(shoulder)
    #    self.Elbow(elbow)
    #    self.Wrist(wrist)
    #    self.Grip(grip)

        #print("shoulder straight", self.wristBone)

    def getState(self):
        wp = self.wristBone.getPos()
        return RobotState(wp.x, wp.y, self.rotate.getAngleRadians(), self.wristBone.getWorldAngleRadians(), self.grip.getAngleRadians())
    
    def update(self):
        self.rotate.update()
        self.shoulder.update()
        self.elbow.update()
        self.wrist.update()
        self.grip.update()
    
    def setState(self, state): 
        
        try:
            dy = self.wristBone.length * math.sin(state.wristWorldAngleRadians)
            dx = self.wristBone.length * math.cos(state.wristWorldAngleRadians)

            x = state.distanceFromBase-dx
            y = state.heightOverBase-dy

            #print(tipx, tipy, x, y)
            #https://www.researchgate.net/publication/328583527_A_Geometric_Approach_to_Inverse_Kinematics_of_a_3_DOF_Robotic_Arm

            r = math.sqrt(x*x + y*y)

            d1 = self.lowerArmBone.length
            d2 = self.upperArmBone.length

            #https://en.wikipedia.org/wiki/Law_of_cosines
            #temp = (x*x + y*y - d1*d1*d2*d2) / (2.0 * d1 * d2)
            temp = (d1*d1+d2*d2-r*r) / (2.0 * d1 * d2)


            if 1 < temp < -1:
                print("not possible, value error", temp)
                return
            elbow = math.pi - math.acos( temp )
            shoulder = math.asin(y/r) + math.atan(d2*math.sin(elbow)/(d1 + d2*math.cos(elbow)))

            self.elbow.setAngleRadians(elbow)
            self.shoulder.setAngleRadians(shoulder)
            self.wristBone.setWorldAngleRadians(state.wristWorldAngleRadians)
            self.rotate.setAngleRadians(state.rotationRadians)
            self.grip.setAngleRadians(state.grip)


        except Exception as e:
            print("Value error", e)

    
    def Shoulder(self, angle):
        self.shoulder.setAngleDegrees(angle)

    def Grip(self, angle):
        self.grip.setAngleDegrees(angle)

    def Wrist(self, angle):
        self.wrist.setAngleDegrees(angle)

    def Elbow(self, angle):
        self.elbow.setAngleDegrees(angle)

    def Rotate(self, angle):
        self.rotate.setAngleDegrees(angle)

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

