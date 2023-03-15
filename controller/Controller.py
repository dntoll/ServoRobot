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

    def setDistanceRotation(self, newDistance, newHeight, newRotation, newWrist):
        self.lastState.heightOverBase = newDistance
        self.lastState.distanceFromBase = newHeight
        self.lastState.rotationRadians = newRotation
        self.lastState.wristWorldAngleRadians = newWrist

        self.hasNewState = True
        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0

    def save(self):
        self.recording.add(self.lastState)
        
        #with open(file_name, 'wb') as file:
        #    pickle.dump(recording, file)

    def update(self):
                

        if self.hasNewState:
            self.robot.setState(self.lastState)
            self.remoteRobot.sendPos(self.lastState)
            self.hasNewState = False
        
        #if view.userWantsReplay():
        #    print("Replay", flush=True)
        #    view.wantsReplay = False
        #    for state in recording:
        #        self.remoteRobot.sendPos(state)
        #        time.sleep(1.5)
        #        while robot.update() is False:
        #            print("wait", flush=True)
        #    print("Done", flush=True)

        
        self.robot.update()
            