from RobotArm import RobotArm
from adafruit_servokit import ServoKit
from getkey import getkey, keys
import time

kit = ServoKit(channels=16)
keyPressStart = time.time()
robot = RobotArm(kit)
numSame = 0

s = 90
r = 60
e = 90
w = 90

lastKey = 0

def handleAxis(keyPressed, lessKey, moreKey, increase, axisFunction, getValueFunction):
    oldValue = getValueFunction()



    if keyPressed == lessKey:
        newValue = oldValue - increase
        axisFunction(newValue)
    elif keyPressed == moreKey:
        newValue = oldValue + increase
        axisFunction(newValue)

while True: 

    key = getkey()

    if key != lastKey:
        keyPressStart = time.time()
        numSame = 1
    else:
        numSame += 1

    keyPressLast = time.time()


    handleAxis(key, keys.UP, keys.DOWN, numSame, robot.Shoulder, robot.shoulder.getAngle)
    handleAxis(key, keys.LEFT, keys.RIGHT, numSame, robot.Elbow, robot.elbow.getAngle)
    handleAxis(key, 'w', 's', numSame, robot.Wrist, robot.wrist.getAngle)
    
    lastKey = key