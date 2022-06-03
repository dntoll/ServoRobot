from RobotArm import RobotArm
import json
import socket
import time

try:
    real = True
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)
    robot = RobotArm(kit)
    HOST = "0.0.0.0"  
except:
    from RobotArmView import RobotArmView
    real = False
    from FakeKit import FakeKit    
    kit = FakeKit()
    robot = RobotArm(kit)
    view = RobotArmView(robot)
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)


keyPressStart = time.time()
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def parseInput(payload):
    asStr = payload.decode("utf-8")
    print(asStr)
    jsonobj = json.loads(asStr)

    x, y, w = jsonobj["x"], jsonobj["y"], jsonobj["w"]
    return x, y, w


if real is False:
    view.draw()
    view.show()
    view.showWindow()


print("Waiting for client:", flush=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}", flush=True)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                x,y,w = parseInput(data)

                print("parsed", x, y, w, flush=True)
                robot.setPos(x, y, w)
                if real is False:
                    view.draw()
                    view.show()
                conn.sendall(data)
