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