
class RobotState:
    distanceFromBase = 25
    heightOverBase = 20
    rotationRadians  = 0
    wristWorldAngleRadians = 0
    grip =0


    def __init__(self, distance, height, rotationRadians, wristWorldAngleRadians, grip):
        self.distanceFromBase = distance
        self.heightOverBase = height
        self.rotationRadians = rotationRadians
        self.wristWorldAngleRadians = wristWorldAngleRadians
        self.grip = grip

