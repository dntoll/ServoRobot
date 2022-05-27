from RobotArm import RobotArm
from adafruit_servokit import ServoKit
import time
import random
import os


class FakeServo:
    angle = 0

class FakeKit:
    servo = []

    def __init__(self):
        for i in range(16):
            self.servo.append(FakeServo())
    

fake = FakeKit()
kit = ServoKit(channels=16)
a = RobotArm(kit)
b = RobotArm(fake)

NUM_CASES = 1000

def randomizeUntilValid():
    
    s = random.randrange(a.shoulder.min, a.shoulder.max)
    e = random.randrange(a.elbow.min, a.elbow.max)
    w = random.randrange(a.wrist.min, a.wrist.max)

    b.setState(RobotArm.ROTATE_NORMAL, s,e,w, 0)

    if b.wristBone.getPos().y > 0:
        return s, e, w
    else:
        return randomizeUntilValid()


def takeImage(i, s, e, w):
    
    os.system('fswebcam -r 1280x720 --no-banner ./images/%d_s%d_e%d_w%d.jpg' % (i, s, e, w) )
    return

for i in range(NUM_CASES):
    s, e, w = randomizeUntilValid()
    a.setState(RobotArm.ROTATE_NORMAL, s,e,w, 0)
    time.sleep(3)
    takeImage(i, s, e, w)