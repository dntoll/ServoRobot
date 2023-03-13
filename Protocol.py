from model.RobotState import RobotState
import json

class Protocol: 

    def getStateFromString(self, payload):
        asStr = payload.decode("utf-8")
        jsonobj = json.loads(asStr)
        return RobotState.decode(jsonobj)

    def getStringFromState(self, state):
        payload = state.encode()
        jsonString = json.dumps(payload)
        jsonString += "\n"
        return jsonString.encode('utf-8')