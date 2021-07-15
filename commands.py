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

class NoPathToDestination(Exception):
    """
    Exception to handle inexistence of path from current position to destination
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
    PATTERN_PLACE = compile(
        r"""
            (?P<x>\d+),                  # x coord
            (?P<y>\d+),                  # y coord
            (?P<f>NORTH|EAST|SOUTH|WEST) # facing
            """, X
    )

    PATTERN_TRAVEL = compile(
        r"""
            (?P<x>\d+),                  # x coord
            (?P<y>\d+)                   # y coord
            """, X
    )

    v = set()

    def getSuccessors(self, pos):
        """
        given a position, all the legal adjacent positions to which robot can move to are returned
        """
        successors = set()

        for dir in self.directions:
            (cur_x,cur_y) = pos
            dx, dy = self._directions[dir]
            x, y = cur_x+dx, cur_y+dy
            if (x >= self.xmin and x <= self.xmax
                and y >= self.ymin and y <= self.ymax):
                if (x, y) not in self.potholes:
                    successors.add((x,y))
        return successors

        
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
        if not cmd_str: raise InvalidCommandFormatError("Invalid PLACE command argument format.")
        isPatternValid = self.PATTERN_PLACE.search(cmd_str)
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

    def transit(self, start, end, path):
        """
        a dfs algorithm is used to find a path from start position to destination (end) position.
        """
        if start == end: 
            # if destination is reached, return the accumulated path
            path.append(end)
            return path
        successors = self.getSuccessors(start)
        if start not in self.v:
            # if the position in the transition is not visited, mark it visited and add it to the path
            path.append(start)
            self.v.add(start)
            for child in successors:
                path = self.transit(child, end, path)
                if end == path[-1]: 
                    # check the last element on the path recieved, if it is destination then return the path
                    return path

                if start != path[-1]:
                    # check the last element on the path if it is not the current position in transition, then
                    # a path shift is in process. We need to remove the last element to proceed.
                    path = path[:-1]
        return path

    def travel(self, cmd_str, conf):
        """
        given the arguments of the travel command, first it is verified if the arguments for the destination
        are valid. If so then, it is tested if the robot is already at the destination.
        If robot is not at destination, if any path exists from current position of robot to destination, then
        a path is found and returned otherwise an exception is raised if no path exists. 
        """
        if not cmd_str: raise InvalidCommandFormatError("Invalid TRAVEL command argument format.")
        isPatternValid = self.PATTERN_TRAVEL.search(cmd_str)
        if isPatternValid:
            x, y = cmd_str.split(',')
            if (int(x),int(y)) in self.potholes: 
                raise IllegalCoordinateError("Co-ordinates are one of the potholes.")
            if (int(x) >= self.xmin and int(x) <= self.xmax and
                int(y) >= self.ymin and int(y) <= self.ymax):
                cur_pos = conf.getPosition()
                self.v = set()
                if cur_pos == (int(x),int(y)): print("Robot already at destination")
                path = self.transit(cur_pos, (int(x),int(y)), [])
                if path[-1] != (int(x),int(y)): raise NoPathToDestination("Path doesn't exist")
                return path
            else: 
                raise IllegalCoordinateError("Co-ordinates are not on the board.")
