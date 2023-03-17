from Lib import copy
import pickle

class Recording:
    def __init__(self):
        self.recording = []
        self.fileName = "";

    def duplicateCurrentState(self, index):
        self.recording.insert(index, copy.copy(self.recording[index]))

        with open(self.fileName, 'wb') as file:
            pickle.dump(self.recording, file)

    def save(self, newState, index):
        self.recording[index] = copy.copy(newState)

        with open(self.fileName, 'wb') as file:
            pickle.dump(self.recording, file)

    def get(self, index):
        return copy.copy(self.recording[index])
        

    def removeCurrentState(self, index):
        del self.recording[index]
        self.wantsToAppend = True

        with open(self.fileName, 'wb') as file:
            pickle.dump(self.recording, file)
    
    def load(self, fileName):
        self.fileName = fileName
        try:
            with open(fileName, 'rb') as file:
                print("load")
                self.recording = pickle.load(file)
        except Exception as e:
            print("File Load error", e, flush=True)
            
