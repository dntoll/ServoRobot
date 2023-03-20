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
import traceback

from tkinter import Tk
import sys
from Protocol import *

fake = FakeKit()
robot = RobotArm(fake)
robot.Relax()
recording = Recording(robot.getState())
protocol = Protocol()


x = 20
y = 20
w = 0
globalS = None

HOST = "192.168.188.96"  # The server's hostname or IP address
#HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

remoteRobot = RemoteRobot(protocol, HOST, PORT)
recording.load('recordings/rubber.pkl')

root = Tk()
controller = Controller(robot, recording, remoteRobot)
view = RobotArmView(robot, root, recording, controller)
while True:
    try:
        time.sleep(0.1)
        controller.update(view.editor_view)
        view.draw()
    except KeyboardInterrupt:
        remoteRobot.close()
        sys.exit(0)
    except Exception as e:
        print("RobotClient", e)
        traceback.print_exc()
        remoteRobot.close()
        sys.exit(0)
        
    

        

        