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
    from model.FakeKit import FakeKit    
    kit = FakeKit()
    robot = RobotArm(kit)
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)


keyPressStart = time.time()
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


doContinue = True

def RobotUpdate(robot, cho):
    global doContinue
    while doContinue:
        try:
            robot.update()
            time.sleep(0.03)
        except Exception as e:
            print(e)
    print("ended update thread", flush=True)

def ServerUpdate(conn, robot):
    protocol = Protocol()
    data = conn.recv(1024)
    if not data:
        conn.close()
        return False
    state = protocol.getStateFromString(data)
    print("State Received: ", state)

    try:
        robot.setState(state)
        conn.sendall(protocol.getStringFromState(robot.getState()))
        return True
    except Exception as e:
        print(e)
    
    return False

cho = "cho"
updateThread = Thread(target=RobotUpdate, args=(robot, cho))
updateThread.start()

print("Waiting for client:", flush=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        
        while doContinue:
            try:
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}", flush=True)
                    doContinueServer = True
                    while True:
                        doContinueServer = ServerUpdate(conn, robot)
                        if doContinueServer is False:
                            break
                    print("Disconnected Client", flush=True)
            except KeyboardInterrupt:
                doContinue = False
                s.close()
                conn.close()
                updateThread.join()
            except Exception as e:
                print("Exception happened", e)
                conn.close()
    
