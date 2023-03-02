
class RobotState:
    distanceFromBase = 25
    heightOverBase = 20
    rotationRadians  = 0
    wristWorldAngleRadians = 3.14
    grip =0


    def __init__(self, distance, height, rotationRadians, wristWorldAngleRadians, grip):
        self.distanceFromBase = distance
        self.heightOverBase = height
        self.rotationRadians = rotationRadians
        self.wristWorldAngleRadians = wristWorldAngleRadians
        self.grip = grip


    def encode(self):
        return {"x": self.distanceFromBase, "y": self.heightOverBase, "r": self.rotationRadians, "w": self.wristWorldAngleRadians, "g": self.grip}
    
    def decode(obj):
        return RobotState(obj["x"], obj["y"], obj["r"], obj["w"], obj["g"])

    def __str__(self):
        return "State <" +  str(self.wristWorldAngleRadians) + ">"