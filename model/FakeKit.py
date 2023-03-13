class FakeServo:
    angle = 0

class FakeKit:
    servo = []

    def __init__(self):
        for i in range(16):
            self.servo.append(FakeServo())