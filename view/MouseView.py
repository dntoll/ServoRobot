class MouseView:
    

    def __init__(self, canvas):

        canvas.bind('<Button-2>', self.stopWristFromControl)
        canvas.bind('<Button-3>', self.grip)
        canvas.bind('<B1-Motion>', self.mouseMoveWithButtonDown)
        canvas.bind('<Button-1>', self.mouseMoveWithButtonDown)
        canvas.bind('<MouseWheel>', self.wrist)


    def stopWristFromControl(self, event):
        self.wristIsControlled = False
        
    def wrist(self, event):
        
        distanceMove = 0.17
        if event.delta > 0:
            self.lastState.wristWorldAngleRadians = self.arm.getState().wristWorldAngleRadians +distanceMove
        else:
            self.lastState.wristWorldAngleRadians = self.arm.getState().wristWorldAngleRadians -distanceMove

        self.wristIsControlled = True
        self.hasNewState = True

        print("arm state", self.arm.getState().wristWorldAngleRadians, flush=True)
        print("target state", self.lastState.wristWorldAngleRadians, flush=True)

    def grip(self, event):
        if self.gripIsOpen:
            self.lastState.grip = RobotArm.GRIP_OPEN
        else:
            self.lastState.grip = RobotArm.GRIP_CLOSED
        self.hasNewState = True
        self.gripIsOpen = not self.gripIsOpen
        

    def mouseMoveWithButtonDown(self, event):
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x() -10
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 30

        if self.wristIsControlled is False:

            ydiff = self.leftViewMiddlePoint[1]-150 - abs_coord_y
            xdiff = self.leftViewMiddlePoint[0] - abs_coord_x
            angle = math.atan2(ydiff, xdiff)
            self.lastState.wristWorldAngleRadians = angle

        if abs_coord_x < self.width/2:
            robotX = (abs_coord_x - self.leftViewMiddlePoint[0])/self.scale
            robotY = (abs_coord_y - self.leftViewMiddlePoint[1])/self.scale

            

            self.lastState.distanceFromBase = robotX
            self.lastState.heightOverBase = robotY
            self.hasNewState = True
        else:
            #mouse is on the right side
            x = abs_coord_x - self.rightViewMiddlePoint[0]
            y = abs_coord_y - self.rightViewMiddlePoint[1]

            distance = - math.sqrt(x*x + y*y) / self.scale

            rotationAngle = math.atan2(y, -x)
            while rotationAngle < 0:
                rotationAngle += 6.28

                

            self.lastState.rotationRadians = rotationAngle
            self.lastState.distanceFromBase = distance
            self.hasNewState = True
        

        if self.lastState.distanceFromBase < 0:
            self.lastState.distanceFromBase = 0