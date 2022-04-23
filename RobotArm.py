from adafruit_servokit import ServoKit
import time 

class RobotArm:
    kit = ServoKit(channels=16)

    WRIST = 0
    ELBOW = 4
    SHOLDER_UP_DOWN = 8
    GRIP = 12
    ROTATE = 15

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

    def __init__(self):

        self.kit.servo[self.ROTATE].angle = self.ROTATE_NORMAL # 
        self.kit.servo[self.GRIP].angle = self.GRIP_OPEN
        self.kit.servo[self.ELBOW].angle = self.ELBOW_90_DEG

        self.kit.servo[self.SHOLDER_UP_DOWN].angle = self.SHOULDER_UP
        self.kit.servo[self.WRIST].angle = self.WRIST_NEUTRAL = 90

        

    def Shoulder(self, angle):
        self.kit.servo[self.SHOLDER_UP_DOWN].angle = angle

    def Grip(self, angle):
        self.kit.servo[self.GRIP].angle = angle

    def Wrist(self, angle):
        self.kit.servo[self.WRIST].angle = angle

    def Elbow(self, angle):
        self.kit.servo[self.ELBOW].angle = angle

    def Rotate(self, angle):
        self.kit.servo[self.ROTATE].angle = angle
