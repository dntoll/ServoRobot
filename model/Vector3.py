

class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def mul(self, scalar):
        return Vector3(self.x * scalar,  self.y * scalar, self.z * scalar)
    
    def add(self, other):
        return Vector3(self.x + other.x,  self.y + other.y , self.z + other.z)

    def __str__(self):
        return "[{:.2f}".format(self.x) + ", {:.2f}".format(self.y) + ", {:.2f}]".format(self.z)