class Controller:
    def __init__(self, robot, recording):
        self.robot = robot
        self.recording = recording
        self.hasNewState = False
        self.wristIsControlled = False
    

    def duplicateCurrentState(self):
        self.recording.duplicateCurrentState()

    def setStateToRelax(self):
        self.robot.Relax()
        self.lastState = self.robot.getState()
        self.hasNewState = True

    def removeCurrentState(self):

        self.recording.removeCurrentState()


    def incrementState(self):
        self.recording.incrementState()

    def decrementState(self):
        self.recording.decrementState()

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
        self.lastState.heightOverBase = newDistance
        self.lastState.distanceFromBase = newHeight
        self.hasNewState = True
        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0

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
         if view.userWantsToSave():
                

        if view.hasNewTargetState():
            state = view.getTargetState()
            sendPos(globalS, state)
        
        if view.userWantsReplay():
            print("Replay", flush=True)
            view.wantsReplay = False
            for state in recording:
                sendPos(globalS, state)
                time.sleep(1.5)
                while robot.update() is False:
                    print("wait", flush=True)
            print("Done", flush=True)
        view.draw()
        robot.update()
            