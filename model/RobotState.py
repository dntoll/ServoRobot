
class RobotState:
    distanceFromBase = 25
    heightOverBase = 20
    rotationRadians  = 0
    wristWorldAngleRadians = 3.14
    grip =0
    name = "unnamed"


    def __init__(self, distance, height, rotationRadians, wristWorldAngleRadians, grip, name):
        self.distanceFromBase = distance
        self.heightOverBase = height
        self.rotationRadians = rotationRadians
        self.wristWorldAngleRadians = wristWorldAngleRadians
        self.grip = grip
        self.name = name


    def encode(self):
        return {"x": self.distanceFromBase, "y": self.heightOverBase, "r": self.rotationRadians, "w": self.wristWorldAngleRadians, "g": self.grip, "n": self.name}
    
    def decode(obj):
        return RobotState(obj["x"], obj["y"], obj["r"], obj["w"], obj["g"], obj["n"])

    def __str__(self):
        return self.name  + " <X=" +  nts(self.distanceFromBase) + ", Y="+  nts(self.heightOverBase) + ", R="+  nts(self.rotationRadians) +", W="+  nts(self.wristWorldAngleRadians)+ "," + nts(self.grip) + ">"
    
def nts(number):
    return str(int(10*number)/10.0)