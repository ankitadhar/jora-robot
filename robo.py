# robo.py
# ------------------------------
# Author: Ankita Dhar <githubid: ankitadhar>

class IllegalGridStructure(Exception):
    """
    Exception to handle illegal grid structures
    """
    pass

class Grid:
    """
    Object to store the table structure
    """
    def __init__(self, width, height, potholes):
        if width > 0 and height > 0:
            self.xmax = width - 1
            self.ymax = height - 1
            self.potholes = potholes
            self.xmin = 0
            self.ymin = 0
        else:
            raise IllegalGridStructure()

class Configuration:
    """
    A Configuration holds the (x,y) coordinate of a character, along with its
    traveling direction.

    The convention for positions, like a graph, is that (0,0) is the lower left corner, x increases
    horizontally and y increases vertically.  Therefore, north is the direction of increasing y, or (0,1).
    """

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def getPosition(self):
        return (self.pos)

    def getDirection(self):
        return self.direction

    def setPosition(self, pos):
        self.pos = pos

    def setDirection(self, direction):
        self.direction = direction

