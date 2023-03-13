class KeyView:
    def __init__(self, frame):
        self.wantsToSave = False
        self.wantsToAppend = True
        
        frame.bind('<KeyRelease>', self.key_released )


    def key_released(self, event):
        if event.char == 's':
            self.wantsToSave = True
        elif event.char == 'r':
            self.wantsReplay = True
        elif event.char == 'c':
            self.duplicateCurrentState()
        elif event.char == 'n':
            self.arm.Relax()
            self.lastState = self.arm.getState()
            self.hasNewState = True
        elif event.char == 'd':
            if self.wantsToAppend is False:
                self.wantsToRemove = True
        elif event.char == '+':
            self.wantsToAppend = False
            self.editIndex += 1
            if self.editIndex < 0 or self.editIndex >= len(self.recording):
                self.editIndex = -1
                self.wantsToAppend = True
            else:
                self.lastState = copy.copy(self.recording[self.editIndex])
                self.hasNewState = True
        elif event.char == '-':
            self.editIndex -= 1
            self.wantsToAppend = False

            #we start at the end
            if self.editIndex == -2:
                self.editIndex = len(self.recording)-1

            #check
            if self.editIndex < 0:
                self.editIndex = -1
                self.wantsToAppend = True
            else:
                self.lastState = copy.copy(self.recording[self.editIndex])
                self.hasNewState = True
        elif event.char > '0' and event.char < '9':
            num = int(event.char)

            if num == 2:
                self.lastState.heightOverBase -= 0.5
            elif num == 8:
                self.lastState.heightOverBase += 0.5
            elif num == 4:
                self.lastState.distanceFromBase -= 0.5
            elif num == 6:
                self.lastState.distanceFromBase += 0.5
            else:
                return
            self.hasNewState = True