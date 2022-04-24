from RobotArm import RobotArm
from getkey import getkey, keys
import time


keyPressStart = time.time()
robot = RobotArm()

s = 90
r = 60
e = 90
w = 90

lastKey = 0

while True: 

    key = getkey()

    if key != lastKey:
        keyPressStart = time.time()

    if key == keys.UP:
        s += 1
        robot.Shoulder(s)
    elif key == keys.DOWN:
        s -= 1
        robot.Shoulder(s)
    elif key == keys.LEFT:
        r -= 1
        robot.Rotate(r)
    elif key == keys.RIGHT:
        r += 1
        robot.Rotate(r)
    elif key == 'w':
        e -= 1
        robot.Elbow(e)
    elif key == 's':
        e += 1
        robot.Elbow(e)
    lastKey = key