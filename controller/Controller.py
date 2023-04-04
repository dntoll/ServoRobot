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
    

    def duplicateCurrentState(self, index):
        self.recording.duplicateCurrentState(index)

    def setStateToRelax(self, index):
        oldname = self.lastState.name
        self.robot.Relax()
        self.lastState = self.robot.getState()
        self.lastState.name = oldname
        self.hasNewState = True

    def removeCurrentState(self, index):

        self.recording.removeCurrentState(index)


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

    def setDistanceHeight(self, newDistance, newHeight):
        self.lastState.heightOverBase = newHeight
        self.lastState.distanceFromBase = newDistance
        self.hasNewState = True
        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0

    def setDistanceRotation(self, newDistance, newRotation):
        self.lastState.distanceFromBase = newDistance
        self.lastState.rotationRadians = newRotation

        self.hasNewState = True
        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0

    def setState(self, state):
        self.lastState = state
        self.hasNewState = True

    def storeState(self, index):
        self.recording.setState(self.lastState, index)
    
    def grip(self):
        if self.lastState.grip == RobotArm.GRIP_CLOSED:
            self.lastState.grip = RobotArm.GRIP_OPEN
        else:
            self.lastState.grip = RobotArm.GRIP_CLOSED
        self.hasNewState = True

    
    def play(self):
        for index in range(0, self.recording.getNumIndicies()):
            self.remoteRobot.sendPos(self.recording.getIndex(index))
            self.robot.setState(self.lastState)
            time.sleep(0.75)
            while self.robot.update() is False:
                print("wait", flush=True)
    
    def setIndexToState(self, current_state_index, current_index_index):
        self.recording.setIndexToState(current_state_index, current_index_index)

    def appendAfterIndex(self, current_state_index, current_index_index):
        self.recording.appendAfterIndex(current_state_index, current_index_index)

    def removeIndex(self, current_index_index):
        self.recording.removeIndex(current_index_index)

    def update(self, view):
                

        if self.hasNewState:
            try:
                view.setState(self.lastState)
                self.robot.setState(self.lastState)
                self.remoteRobot.sendPos(self.lastState)
                self.hasNewState = False
            except Exception as e:
                print(e)

        
        self.robot.update()
            