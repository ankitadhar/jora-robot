import unittest
from nose.tools import raises
from commands import Commands, IllegalCoordinateError, NoPathToDestination
from robo import Configuration
from simulator import Simulator
import constants

class TestRobotSetup(unittest.TestCase):
    grid_height = constants.GRID_HEIGHT
    grid_width = constants.GRID_WIDTH
    command = Commands(grid_width, grid_height, constants.GRID_POTHOLES)
    configuration = Configuration(constants.INIT_POSITION, constants.INIT_DIRECTION)
    simulator = Simulator()


    def testPlaceCmd1(self):
        x = 0
        y = 3
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos, dir = self.simulator.executeCmd("PLACE", cmd_str)
        assert pos == (x, y)
        assert dir == direction

    def testPlaceCmd2(self):
        x = 1
        y = 3
        direction = "EAST"
        cmd_str = str(x)+','+str(y)+','+direction
        pos, dir = self.simulator.executeCmd("PLACE", cmd_str)
        assert pos == (x, y)
        assert dir == direction

    def testMOVECmd1(self):
        x = 0
        y = 0
        dx = 1
        dy = 1
        direction = "EAST"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        pos, dir = self.simulator.executeCmd("MOVE", None)
        assert pos == (x + dx, y)
        assert dir == direction

    def testMOVECmd2(self):
        x = 0
        y = 0
        direction = "WEST"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        pos, dir = self.simulator.executeCmd("MOVE", None)
        # print(pos, dir)
        assert pos == (x, y)
        assert dir == direction

    def testMOVECmdToPothole(self):
        x = 3
        y = 2
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        pos, dir = self.simulator.executeCmd("MOVE", None)
        # print(pos, dir)
        assert pos == (x, y)
        assert dir == direction

    def testMOVECmd3(self):
        x = 2
        y = 3
        dx = 1
        dy = 1
        direction = "SOUTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        pos, dir = self.simulator.executeCmd("MOVE", None)
        # print(pos, dir)
        assert pos == (x, y - dy)
        assert dir == direction

    def testMOVECmd4(self):
        x = 2
        y = 2
        dx = 1
        dy = 1
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        pos, dir = self.simulator.executeCmd("MOVE", None)
        # print(pos, dir)
        assert pos == (x, y + dy)
        assert dir == direction

    def testTurnLeft(self):
        x = 2
        y = 2
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        pos, dir = self.simulator.executeCmd("LEFT", None)

        assert pos == (x, y)
        assert dir == "WEST"

        self.simulator.configuration.setDirection(dir)
        pos, dir = self.simulator.executeCmd("LEFT", None)

        assert pos == (x, y)
        assert dir == "SOUTH"

        self.simulator.configuration.setDirection(dir)
        pos, dir = self.simulator.executeCmd("LEFT", None)

        assert pos == (x, y)
        assert dir == "EAST"

        self.simulator.configuration.setDirection(dir)
        pos, dir = self.simulator.executeCmd("LEFT", None)

        assert pos == (x, y)
        assert dir == "NORTH"

    def testTurnRight(self):
        x = 2
        y = 2
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        pos, dir = self.simulator.executeCmd("RIGHT", None)

        assert pos == (x, y)
        assert dir == "EAST"

        self.simulator.configuration.setDirection(dir)
        pos, dir = self.simulator.executeCmd("RIGHT", None)

        assert pos == (x, y)
        assert dir == "SOUTH"

        self.simulator.configuration.setDirection(dir)
        pos, dir = self.simulator.executeCmd("RIGHT", None)

        assert pos == (x, y)
        assert dir == "WEST"

        self.simulator.configuration.setDirection(dir)
        pos, dir = self.simulator.executeCmd("RIGHT", None)

        assert pos == (x, y)
        assert dir == "NORTH"   

    #### Code Pairing Test Cases #### 
        
    @raises(IllegalCoordinateError)
    def testTravelOutofBoard(self):
        x = 0
        y = 0
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        to_pos = f"{constants.GRID_WIDTH + 1},3"
        path = self.simulator.executeCmd("TRAVEL", to_pos)
        assert path == [(0, 0), (1, 0)]

    @raises(NoPathToDestination)
    def testTravelWNoPath(self):
        x = 0
        y = 0
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        to_pos = "4,4"
        path = self.simulator.executeCmd("TRAVEL", to_pos)
        assert path == [(0, 0), (1, 0)]

    def testTravel(self):
        x = 0
        y = 0
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        pos1, dir1 = self.simulator.executeCmd("PLACE", cmd_str)
        self.simulator.configuration.setPosition(pos1)
        self.simulator.configuration.setDirection(dir1)
        to_pos = "1,0"
        path = self.simulator.executeCmd("TRAVEL", to_pos)
        assert path == [(0, 0), (1, 0)]

    def testGetSucc(self):
        x = 0
        y = 0
        succ = self.command.getSuccessors((x,y))
        assert succ == {(0, 1), (1, 0)}


if __name__ == '__main__':
    unittest.main()