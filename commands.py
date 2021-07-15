# commands.py
# ------------------------------
# Author: Ankita Dhar <githubid: ankitadhar>

from robo import Grid 
import constants
from re import compile, X

class InvalidCommandFormatError(Exception):
    """
    Exception to handle invalid command format for PLACE command.
    """
    pass

class IllegalCoordinateError(Exception):
    """
    Exception to handle out of the table coordinates
    """
    pass

class Commands(Grid):
    """
    A collection of methods for manipulating robot's movement.
    """
    # Directions
    directions = constants.DIRECTIONS
    
    # vector for movement towards different directions
    _directions = {constants.NORTH: (0, 1),
                   constants.SOUTH: (0, -1),
                   constants.EAST:  (1, 0),
                   constants.WEST:  (-1, 0)}
    
    # pattern to validate arguments of PLACE command
    PATTERN = compile(
        r"""
            (?P<x>\d+),                  # x coord
            (?P<y>\d+),                  # y coord
            (?P<f>NORTH|EAST|SOUTH|WEST) # facing
            """, X
    )
        
    def nextIndex(self, index):
        """
        implemented circular queue for accessing next index of stored directions
        """
        if index == len(self.directions) - 1: return 0
        return index + 1

    def directionToVector(self, direction, speed = 1.0):
        """
        given a direction, finding the vector of displacement
        """
        dx, dy =  Commands._directions[direction]
        return (dx * speed, dy * speed)

    def turnLeft(self, dir):
        """
        given a direction, returns the direction of the robot upon turning left
        """
        index = self.directions.index(dir)
        return self.directions[index-1]

    def turnRight(self, dir):
        """
        given a direction, returns the direction of the robot upon turning right
        """
        index = self.directions.index(dir)
        return self.directions[self.nextIndex(index)]

    def move(self, position, dir):
        """
        given the position and direction of robot, returns new position of the robot
        # when it moves by one step towards the direction the robot faces, provided the robot
        # does not fall from the table upon taking the step; otherwise the original position is
        returned unaltered.
        """
        x, y = position
        dx, dy = self.directionToVector(dir)
        
        if ((dy > 0 and y < self.ymax) or (dy < 0 and y > self.ymin)) and ((x, int(y + dy)) not in self.potholes): 
            return x, int(y + dy)
        if ((dx > 0 and x < self.xmax) or (dx < 0 and x > self.xmin)) and ((int(x + dx), y) not in self.potholes): 
            return (int(x + dx), y)
        return (x,y)
    
    def place(self, cmd_str):
        """
        given the arguments of the place commands, it is first verified to be valid and then the robot
        is placed at the location, facing the direction as per the arguments.
        """
        isPatternValid = self.PATTERN.search(cmd_str)
        if isPatternValid:
            # if the pattern of the argument is valid
            x,y,dir = cmd_str.split(',')
            if (int(x),int(y)) in self.potholes: 
                raise IllegalCoordinateError("Co-ordinates are one of the potholes.")
            if (int(x) >= self.xmin and int(x) <= self.xmax and
                int(y) >= self.ymin and int(y) <= self.ymax):
                # if the co-ordinates provided in the argument are valid
                pos = (int(x),int(y))
                return pos, dir
            else:
                raise IllegalCoordinateError("Co-ordinates are out of the table.")
        else:
            raise InvalidCommandFormatError("Invalid PLACE command argument format.")

