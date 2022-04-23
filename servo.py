from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

WRIST = 0
ELBOW = 4
SHOLDER_UP_DOWN = 8
GRIP = 12
ROTATE = 15

kit.servo[GRIP].angle = 180
kit.servo[WRIST].angle = 175
kit.servo[ELBOW].angle = 90
kit.servo[SHOLDER_UP_DOWN].angle = 90

kit.servo[ROTATE].angle = 90


