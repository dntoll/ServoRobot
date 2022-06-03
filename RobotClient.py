from RobotArm import RobotArm
from FakeKit import FakeKit    
from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import time
import socket
import json

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
def on_move(mx, my):
    global x
    global y
    global w
    global omx
    global omy 
    global firstMove
    print('Pointer moved to {0}'.format(
        (mx, my)))

    if firstMove is False:
        dx = mx-omx
        dy = -(my-omy)

        print("deltamove", dx, dy)

        x += dx/10
        y += dy/10
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

def on_press(key):
    global x
    global y
    global w
    try:
        w = handleAxis(key.char, 'w', 's', w, 0.1)
        print('alphanumeric key {0} pressed'.format(
            key.char), flush=True)
    except AttributeError:
        y = handleAxis(key, Key.up, Key.down, y, 1)
        x = handleAxis(key, Key.left, Key.right, x, 1)
        print('special key {0} pressed'.format(
            key), flush=True)

    sendPos(globalS, x, y, w)

def on_release(key):
    #print('{0} released'.format(
    #    key), flush=True)
    if key == keyboard.Key.esc:
        # Stop listener
        return False

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
    print(f"Received {data!r}", flush=True)

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    
        mlistener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll)
        mlistener.start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("try to join")
                
            s.connect((HOST, PORT))
            globalS = s
            listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
            listener.start()
            listener.join()
    
    

        

        