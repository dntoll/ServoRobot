
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
        return "S <X=" +  nts(self.distanceFromBase) + ", Y="+  nts(self.heightOverBase) + ", R="+  nts(self.rotationRadians) +", W="+  nts(self.wristWorldAngleRadians)+ ">"
    
def nts(number):
    return str(int(10*number)/10.0)