from model.RobotArm import RobotArm
from threading import Thread
from Protocol import *


import socket
import time
import sys

try:
    real = True
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)
    
    robot = RobotArm(kit)
    HOST = "0.0.0.0"  
except:
    from view.RobotArmView import RobotArmView
    real = False
    from FakeKit import FakeKit    
    kit = FakeKit()
    robot = RobotArm(kit)
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)


keyPressStart = time.time()
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)



def RobotUpdate(robot):
    while True:
        robot.update()
        time.sleep(0.1)


protocol = Protocol()

t = Thread(target=RobotUpdate, args=[robot])
t.start()

print("Waiting for client:", flush=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    doContinue = True
    while doContinue:
        try:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}", flush=True)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("no data baby!");
                        break
                    state = protocol.getStateFromString(data)
                    robot.setState(state)
                    conn.sendall(protocol.getStringFromState(robot.getState()))
        except KeyboardInterrupt:
            print("keyboard shit")
            # quit
            sys.exit()
            doContinue = False
        except Exception as e:
            
            print("shit happened", e)
