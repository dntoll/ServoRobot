from RobotArm import RobotArm


class RobotState:
    distanceFromBase = 25
    heightOverBase = 20
    rotationRadians  = RobotArm.ROTATE_NORMAL
    wristWorldAngleRadians = RobotArm.WRIST_NEUTRAL
    grip = RobotArm.GRIP_OPEN


    def __init__(self, distance, height, rotationRadians, wristWorldAngleRadians, grip):
        self.distanceFromBase = distance
        self.heightOverBase = height
        self.rotationRadians = rotationRadians
        self.wristWorldAngleRadians = wristWorldAngleRadians
        self.grip = grip

