import unittest

from simulator_basic import *


class TestCommands(unittest.TestCase):
    def testNoRobotOnBrd(self):
        cmd = "LEFT"
        result = extractCmd(cmd)
        print(result)
        self.assertEqual(result, ((-1, -1), None))

    def testPlaceCmd(self):
        """
        Test that it can sum a list of integers
        """
        cmd = "PLACE 0,0,NORTH"
        result = extractCmd(cmd)
        self.assertEqual(result, ((0, 0), 'NORTH'))
    
    def testLeftCmd(self):
        """
        Test that it can sum a list of integers
        """
        cmd1 = "PLACE 0,0,NORTH"
        cmd2 = "LEFT"
        extractCmd(cmd1)
        result = extractCmd(cmd2)
        self.assertEqual(result, ((0, 0), 'WEST'))

    def testRightCmd(self):
        """
        Test that it can sum a list of integers
        """
        cmd1 = "PLACE 0,0,NORTH"
        cmd2 = "RIGHT"
        extractCmd(cmd1)
        result = extractCmd(cmd2)
        self.assertEqual(result, ((0, 0), 'EAST'))

    def testMoveCmd(self):
        """
        Test that it can sum a list of integers
        """
        cmd1 = "PLACE 0,0,NORTH"
        cmd2 = "MOVE"
        extractCmd(cmd1)
        result = extractCmd(cmd2)
        self.assertEqual(result, ((0, 1), 'NORTH'))

    def testOutOfBrdMoveCmd(self):
        """
        Test that it can sum a list of integers
        """
        cmd1 = "PLACE 4,4,EAST"
        cmd2 = "MOVE"
        extractCmd(cmd1)
        result = extractCmd(cmd2)
        self.assertEqual(result, ((4, 4), 'EAST'))

    def testNoRobotOnBrd(self):
        cmd = "MOVE"
        result = extractCmd(cmd)
        self.assertEqual(result, ((-1, -1), None))

if __name__ == '__main__':
    unittest.main()