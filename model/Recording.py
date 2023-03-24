from Lib import copy
import pickle


class Recording:
    def __init__(self, startState):
        self.startState = startState
        self.states = [startState]
        self.indicies = [0]
        self.fileName = ""

    def duplicateCurrentState(self, index):
        self.states.insert(index, copy.copy(self.states[index]))
        self._save()

    def setState(self, newState, index):
        self.states[index] = copy.copy(newState)
        self._save()

    def getNumStates(self):
        return len(self.states)
    
    def getNumIndicies(self):
        return len(self.indicies)

    def getState(self, index):
        return copy.copy(self.states[index])
    
    def getIndex(self, index):
        return copy.copy(self.states[self.indicies[index]])
    

    def setIndexToState(self, current_state_index, current_index_index):
        self.indicies[current_index_index] = current_state_index

    def appendAfterIndex(self, current_state_index, current_index_index):
        self.indicies.insert(current_index_index+1, current_state_index)


    def removeIndex(self, current_index_index):
        del self.indicies[current_index_index]

    def removeCurrentState(self, index):
        del self.states[index]
        self.wantsToAppend = True


        if self.getNumStates() == 0:
            self.states = [self.startState]
        self._save()
        

    def _save(self):
        with open(self.fileName, 'wb') as file:
            pickle.dump(self.states, file)
        with open(self.fileName + "st", 'wb') as file:
            pickle.dump(self.indicies, file)
        

    def load(self, fileName):
        self.fileName = fileName
        try:
            with open(fileName, 'rb') as file:
                self.states = pickle.load(file)
                if self.getNumStates() == 0:
                    self.states = [self.startState]
            with open(fileName + "st", 'rb') as file:
                self.indicies = pickle.load(file)
                if self.getNumStates() == 0:
                    self.indicies = [self.startState]
        except Exception as e:
            print("File Load error", e, flush=True)
            
