import math

class MouseView:
    

    def __init__(self, canvas, controller, root, leftViewMiddlePoint, rightViewMiddlePoint, width, scale):
        self.leftViewMiddlePoint = leftViewMiddlePoint
        self.rightViewMiddlePoint = rightViewMiddlePoint
        self.root = root
        self.width = width
        self.controller = controller
        canvas.bind('<Button-2>', self.stopWristFromControl)
        canvas.bind('<Button-3>', self.grip)
        canvas.bind('<B1-Motion>', self.mouseMoveWithButtonDown)
        canvas.bind('<Button-1>', self.mouseMoveWithButtonDown)
        canvas.bind('<MouseWheel>', self.wrist)
        self.scale = scale

        


    def stopWristFromControl(self, event):
        self.controller.wristIsControlled = False

    


    def wrist(self, event):
        
        distanceMove = 0.17
        if event.delta > 0:
            self.controller.alterState(0, 0.0, 0.0, distanceMove)
        else:
            self.controller.alterState(0, 0.0, 0.0, -distanceMove)

        self.controller.wristIsControlled = True

        
    def grip(self, event):
        self.controller.grip()
        
        

    def mouseMoveWithButtonDown(self, event):
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_x() -10
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_y() - 30

        if self.controller.wristIsControlled is False:

            ydiff = self.leftViewMiddlePoint[1]-150 - abs_coord_y
            xdiff = self.leftViewMiddlePoint[0] - abs_coord_x
            angle = math.atan2(ydiff, xdiff)
            print("ydiff, xdiff, angle", ydiff, xdiff, angle*360/2.0*3.14)
            
            self.controller.setWrist(angle)
        
        if abs_coord_x < self.width/2:
            robotX = (abs_coord_x - self.leftViewMiddlePoint[0])/self.scale
            robotY = (abs_coord_y - self.leftViewMiddlePoint[1])/self.scale

            
            self.controller.setDistanceHeight(robotX, robotY)
            
        else:
            #mouse is on the right side
            x = abs_coord_x - self.rightViewMiddlePoint[0]
            y = abs_coord_y - self.rightViewMiddlePoint[1]

            distance = - math.sqrt(x*x + y*y) / self.scale

            rotationAngle = math.atan2(y, -x)
            while rotationAngle < 0:
                rotationAngle += 6.28

                
            self.controller.setDistanceRotation(distance, rotationAngle)    