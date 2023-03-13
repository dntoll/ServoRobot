from model.RobotArm import RobotArm
from threading import Thread
from protocol import *


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


doContinue = True

def RobotUpdate(robot, doContinue):
    while doContinue:
        robot.update()
        time.sleep(0.1)
    print("ended update thread", flush=True)


protocol = Protocol()

updateThread = Thread(target=RobotUpdate, args=[robot, doContinue])
updateThread.start()

print("Waiting for client:", flush=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
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
            print("Keyboard interrupt catched", flush=True)
            doContinue = False
            print("Try to join", flush=True)
            updateThread.join()
            print("Thread joined", flush=True)
            # quit
            s.close()
            sys.exit()
            
            
            doContinue = False
        except Exception as e:
            
            print("shit happened", e)
