import unittest
from nose.tools import raises
from robo import Grid, IllegalGridStructure
from commands import Commands, IllegalCoordinateError, InvalidCommandFormatError
from simulator import Simulator, RobotNotPlacedOnTable, CommandNotFoundError
import constants

class TestRobotSetup(unittest.TestCase):
    grid_height = constants.GRID_HEIGHT
    grid_width = constants.GRID_WIDTH
    command = Commands(grid_width, grid_height, constants.GRID_POTHOLES)
    simulator = Simulator()

    @raises(InvalidCommandFormatError)
    def testPlaceCmdFormat1(self):
        self.simulator.executeCmd("PLACE", "illegal,format")

    @raises(InvalidCommandFormatError)
    def testPlaceCmdFormat2(self):
        self.simulator.executeCmd("PLACE", "1,2,north")

    @raises(IllegalCoordinateError)
    def testPlaceCmdPosition1(self):
        self.simulator.executeCmd("PLACE", "-1,2,NORTH")
    
    @raises(IllegalCoordinateError)
    def testPlaceCmdPosition2(self):
        x = constants.GRID_WIDTH + 1
        y = 3
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        self.simulator.executeCmd("PLACE", cmd_str)

    @raises(IllegalCoordinateError)
    def testPlaceCmdPosPothole(self):
        (x,y) = constants.GRID_POTHOLES[1]
        direction = "NORTH"
        cmd_str = str(x)+','+str(y)+','+direction
        self.simulator.executeCmd("PLACE", cmd_str)

    @raises(IllegalGridStructure)
    def testIllegalGridSetup(self):
        Grid(-1,2,constants.GRID_POTHOLES)
    
    def testLegalGridSetup(self):
        Grid(5,5,constants.GRID_POTHOLES)

    @raises(RobotNotPlacedOnTable)
    def testReportNoRobotOnTable(self):
        self.simulator.simulate("REPORT")

    @raises(CommandNotFoundError)
    def testIllegalCmd(self):
        self.simulator.simulate("JUMP")

    #### Code Pairing Test Cases #### 

    @raises(RobotNotPlacedOnTable)
    def testTravelWNoRobot(self):
        to_pos = "4,4"
        self.simulator.executeCmd(constants.TRAVELCOMMAND, to_pos)

if __name__ == '__main__':
    unittest.main()
