from adafruit_servokit import ServoKit
from RobotArm import RobotArm
import time

kit = ServoKit(channels=16)
a = RobotArm(kit)

#while True:
time.sleep(0.5)
a.setState(RobotArm.ROTATE_NORMAL, 0.5, 0.5, 0.5, 0)

#a.downShoulder()
#time.sleep(0.5)
#kit.servo[WRIST].angle = 175
#kit.servo[ELBOW].angle = 90
#kit.servo[SHOLDER_UP_DOWN].angle = 90

#kit.servo[ROTATE].angle = 90


