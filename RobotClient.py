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

def sendPos(s, x, y, w):
    global robot
    print(f"sendpos {x} {y} {w}", flush=True)
    robot.setPos(x, y, w)
    if w < 0:
        w += 6.28

    payload = {"x": x, "y":y, "w": w}
    jsonString = json.dumps(payload)
    jsonString += "\n"
    s.send(jsonString.encode('utf-8'))
    data = s.recv(1024)
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
            if view.hasNewTargetPosition():
                pos = view.getTargetPosition()
                sendPos(globalS, pos[0], pos[1], pos[2])
            view.draw()
            
            
        except KeyboardInterrupt:
            sys.exit(0)
        
    

        

        