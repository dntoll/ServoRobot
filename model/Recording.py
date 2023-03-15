from Lib import copy
import pickle

class Recording:
    def __init__(self):
        self.recording = []
        self.editIndex = -1
        self.wantsToAppend = True

    def duplicateCurrentState(self):
        if self.wantsToAppend: #We dont have a current state
            return
        self.recording.insert(self.editIndex, copy.copy(self.recording[self.editIndex]))

    def add(self, newState):
        if self.wantsToAppend:
            self.recording.append(copy.copy(newState))
        else:
            self.recording[self.editIndex] = copy.copy(newState)
        

    def removeCurrentState(self):
        
        if self.wantsToAppend is False:
            self.wantsToRemove = True
        
        del self.recording[self.editIndex]
        self.wantsToAppend = True

    def incrementState(self, lastState):
        self.wantsToAppend = False
        self.editIndex += 1
        if self.editIndex < 0 or self.editIndex >= len(self.recording):
            self.editIndex = -1
            self.wantsToAppend = True
            return lastState
        else:
            return copy.copy(self.recording[self.editIndex])

    def decrementState(self, lastState):
        self.editIndex -= 1
        self.wantsToAppend = False

        #we start at the end
        if self.editIndex == -2:
            self.editIndex = len(self.recording)-1

        #check
        if self.editIndex < 0:
            self.editIndex = -1
            self.wantsToAppend = True
            return lastState
        else:
            return copy.copy(self.recording[self.editIndex])
    
    def load(self, fileName):
        try:
            with open(fileName, 'rb') as file:
                print("load")
                recording = pickle.load(file)
        except Exception as e:
            print("File Load error", e, flush=True)
