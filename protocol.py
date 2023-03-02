from RobotState import RobotState
import json


def getStateFromString(payload):
    asStr = payload.decode("utf-8")
    jsonobj = json.loads(asStr)
    return RobotState.decode(jsonobj)

def getStringFromState(state):
    payload = state.encode()
    jsonString = json.dumps(payload)
    jsonString += "\n"
    return jsonString.encode('utf-8')