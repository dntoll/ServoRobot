import time
from model.RobotArm import RobotArm

class Controller:
    def __init__(self, robot, recording, remoteRobot):
        self.robot = robot
        self.recording = recording
        self.hasNewState = False
        self.wristIsControlled = False
        self.remoteRobot = remoteRobot
        self.lastState = self.robot.getState()
    

    def duplicateCurrentState(self):
        self.recording.duplicateCurrentState()

    def setStateToRelax(self):
        self.robot.Relax()
        self.lastState = self.robot.getState()
        self.hasNewState = True

    def removeCurrentState(self):

        self.recording.removeCurrentState()


    def incrementState(self):
        self.lastState = self.recording.incrementState(self.lastState)
        self.hasNewState = True

    def decrementState(self):
        self.lastState = self.recording.decrementState(self.lastState)
        self.hasNewState = True

    def alterState(self, distanceFromBaseModifier, heightModifier, rotationModifier, wristAngle):
        self.lastState.heightOverBase += heightModifier
        self.lastState.distanceFromBase += distanceFromBaseModifier
        self.lastState.rotationRadians +=  rotationModifier
        self.lastState.wristWorldAngleRadians += wristAngle

        if wristAngle != 0:
            self.wristIsControlled = True

        self.hasNewState = True
    
    def setWrist(self, newWrist):
        self.lastState.wristWorldAngleRadians = newWrist
        self.hasNewState = True
        print("wrist")

    def setDistanceHeight(self, newDistance, newHeight):
        self.lastState.heightOverBase = newHeight
        self.lastState.distanceFromBase = newDistance
        self.hasNewState = True
        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0
        print("distanceHeight")

    def setDistanceRotation(self, newDistance, newRotation):
        self.lastState.heightOverBase = newDistance
        self.lastState.rotationRadians = newRotation

        self.hasNewState = True
        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0

    def save(self):
        self.recording.add(self.lastState)
    
    def grip(self):
        if self.lastState.grip == RobotArm.GRIP_CLOSED:
            self.lastState.grip = RobotArm.GRIP_OPEN
        else:
            self.lastState.grip = RobotArm.GRIP_CLOSED
        self.hasNewState = True

    
    def play(self):
        for state in self.recording.recording:
            self.remoteRobot.sendPos(state)
            self.robot.setState(self.lastState)
            time.sleep(1.5)
            while self.robot.update() is False:
                print("wait", flush=True)
    

    def update(self):
                

        if self.hasNewState:
            try:
                self.robot.setState(self.lastState)
                self.remoteRobot.sendPos(self.lastState)
                self.hasNewState = False
            except Exception as e:
                print(e)

        
        self.robot.update()
            