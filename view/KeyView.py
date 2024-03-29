class KeyView:
    def __init__(self, frame, controller):
        self.wantsToSave = False
        self.wantsToAppend = True
        self.controller = controller
        
        frame.bind('<KeyRelease>', self.key_released )



    def key_released(self, event):
        print("KeyEvent:", event)

        if event.char > '0' and event.char < '9':
            num = int(event.char)
            distanceMoved = 0.5
            if num == 2:
                self.controller.alterState(0.0, -distanceMoved, 0.0, 0.0)
            elif num == 8:
                self.controller.alterState(0.0, distanceMoved, 0.0, 0.0)
            elif num == 4:
                self.controller.alterState(distanceMoved, 0.0, 0.0, 0.0)
            elif num == 6:
                self.controller.alterState(-distanceMoved, 0.0, 0.0, 0.0)
            else:
                return
            self.hasNewState = True