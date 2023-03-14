from Lib import copy

class Recording:
    def __init__(self, initialState):
        self.recording = []
        self.lastState = initialState
        self.editIndex = -1
        self.wantsToAppend = True

    def duplicateCurrentState(self):
        if self.wantsToAppend: #We dont have a current state
            return
        self.recording.insert(self.editIndex, copy.copy(self.recording[self.editIndex]))

    def removeCurrentState(self):
        
        if self.wantsToAppend is False:
            self.wantsToRemove = True
        
        del self.recording[self.editIndex]
        self.wantsToAppend = True

    def incrementState(self):
        self.wantsToAppend = False
        self.editIndex += 1
        if self.editIndex < 0 or self.editIndex >= len(self.recording):
            self.editIndex = -1
            self.wantsToAppend = True
        else:
            self.lastState = copy.copy(self.recording[self.editIndex])
            self.hasNewState = True

    def decrementState(self):
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