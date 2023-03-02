from RobotArm import RobotArm
from FakeKit import FakeKit    
from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
from RobotArmView import RobotArmView
import time
import socket
import json
import sys

fake = FakeKit()
robot = RobotArm(fake)


x = 20
y = 20
w = 0
globalS = None

HOST = "192.168.188.96"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

omx = 0
omy = 0
firstMove = True

def sendPos(s, state):
    global robot
    try:
        robot.setState(state)
        payload = state.encode() 
        jsonString = json.dumps(payload)
        jsonString += "\n"
        s.send(jsonString.encode('utf-8'))
        data = s.recv(1024)
    except Exception as e:
        print("not possible", e, flush=True)
    
    #print(f"Received {data!r}", flush=True)

print("Hej")
    

from tkinter import Tk


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("try to join")
        
    s.connect((HOST, PORT))

    root = Tk()
    view = RobotArmView(robot, root)

    print("connected")
    globalS = s
    while True:
        try:
            time.sleep(0.1)
            if view.hasNewTargetState():
                state = view.getTargetState()
                sendPos(globalS, state)
            view.draw()
            robot.update()
            
        except KeyboardInterrupt:
            s.close()
            sys.exit(0)
        
    

        

        