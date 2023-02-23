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
view = RobotArmView(robot)

x = 20
y = 20
w = 0
globalS = None

HOST = "192.168.188.96"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

omx = 0
omy = 0
firstMove = True
def on_move(mx, my):
    global x
    global y
    global w
    global omx
    global omy 
    global firstMove
    print('Pointer moved to {0}'.format((mx, my)))

    if firstMove is False:
        dx = -(mx-omx)/10
        dy = -(my-omy)/10

        print("deltamove", dx, dy)

        x += dx
        y += dy
        sendPos(globalS, x, y, w)
    firstMove = False
    omx = mx
    omy = my

    x, y, w = robot.getPos()

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))


def handleAxis(keyPressed, moreKey, lessKey, oldValue, increase):

    if keyPressed == lessKey:
        newValue = oldValue - increase
    elif keyPressed == moreKey:
        newValue = oldValue + increase
    else:
        return oldValue
    return newValue

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
    




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("try to join")
        
    s.connect((HOST, PORT))

    view.draw()
    view.show()
    view.showWindow()

    mlistener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
    mlistener.start()

    print("connected")
    globalS = s
    while True:
        try:
            time.sleep(0.1)
            
            view.draw()
            view.show()
        except KeyboardInterrupt:
            sys.exit(0)
        
    

        

        