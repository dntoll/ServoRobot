import socket

class RemoteRobot:
    def __init__(self, protocol, adress, port):
        self.protocol = protocol
        self.adress = adress
        self.port = port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("try to join")
    
        self.s.connect((adress, port))

        print("connected")

    
    def sendPos(self, state):
        try:
            str = self.protocol.getStringFromState(state)
            self.s.send(str)
            data = self.s.recv(1024)
            state = self.protocol.getStateFromString(data)
            #robot.setState(state)
        except Exception as e:
            print("not possible", e, flush=True)

    
    def close(self):
        self.s.close()