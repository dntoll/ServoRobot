from model.RobotArm import RobotArm
from model.FakeKit import FakeKit    
from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
from view.RobotArmView import RobotArmView
from model.RobotState import RobotState
from model.Recording import Recording
from model.RemoteRobot import RemoteRobot
from controller.Controller import Controller 

import time


import sys
from Protocol import *

fake = FakeKit()
robot = RobotArm(fake)
robot.Relax()
recording = Recording()
protocol = Protocol()


x = 20
y = 20
w = 0
globalS = None

#HOST = "192.168.188.96"  # The server's hostname or IP address
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

remoteRobot = RemoteRobot(protocol, HOST, PORT)



omx = 0
omy = 0
firstMove = True




    
    

from tkinter import Tk



recording.load('recordings/rubber.pkl')

root = Tk()
controller = Controller(robot, recording, remoteRobot)
view = RobotArmView(robot, root, recording, controller)
while True:
    try:
        time.sleep(0.1)
        controller.update()
        view.draw()
    except KeyboardInterrupt:
        remoteRobot.close()
        sys.exit(0)
        
    

        

        