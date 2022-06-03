from RobotArm import RobotArm


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

import time


keyPressStart = time.time()



import socket



PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def parseInput(bytes):
    x, y, w = bytes[0], bytes[1], 6.28*float((bytes[2]))/255.0
    return x, y, w


if real is False:
    view.draw()
    view.show()
    view.showWindow()

while True:
    print("Waiting for client:", flush=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
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
