# simulator.py
# ------------------------------
# Author: Ankita Dhar <githubid: ankitadhar>


from commands import Commands
from robo import Configuration
import constants # constants for the program are defined here

class CommandNotFoundError(Exception):
    """
    Exception to handle illegal commands.
    """
    pass

class CommandNotImplementedError(Exception):
    """
    Exception to handle legal but not implemented commands.
    """
    pass

class RobotNotPlacedOnTable(Exception):
    """
    Exception to handle REPORT command when robot is not placed on the table.
    """
    pass

class Simulator:
    """
    Simulator class is an interface between the main function and the executable functions.
    This class accepts the command, removes all unnecessary spaces, extracts and identifies the commands
    and calls specific functions from the Commands class to execute the user's commands.
    After execution, the results are stored using Configuration class.
    """
    def __init__(self):
        grid_height = constants.GRID_HEIGHT
        grid_width = constants.GRID_WIDTH
        self.command = Commands(grid_width, grid_height, constants.GRID_POTHOLES)
        # instantiating Commands class with the grid height and width, on which commands are to be executed.
        self.configuration = Configuration(constants.INIT_POSITION, constants.INIT_DIRECTION)
        # initializing the robot's position as out of the table and direction as None

    def executeCmd(self, cmd, cmd_str):
        """
        executeCmd identifies the commands and calls respective functions from Commands class instance.
        cmd <- command to execute
        cmd_str <- arguments to the command (ignored if command is not PLACE)
        """
        # fetching current position and direction of the robot
        pos = self.configuration.getPosition()
        dir = self.configuration.getDirection()

        if cmd == constants.REPORTCOMMAND:
            # if command is REPORT and the robot is not on the table, an exception is raised
            # otherwise robot's position and direction is printed on the standard ouput
            if pos == constants.INIT_POSITION:
                raise RobotNotPlacedOnTable("Robot not found on table.")
            x, y = pos
            print(str(x)+','+str(y)+','+dir)
        elif constants.TRAVEL == cmd:
            # if command is TRAVEL and the robot is not on the table, an exception is raised
            # otherwise the path that can be travelled to reach the destination is returned
            if pos == constants.INIT_POSITION:
                raise RobotNotPlacedOnTable("Robot not found on table.")
            path = self.command.travel(cmd_str, self.configuration)
            return path
        elif cmd != constants.PLACECOMMAND and pos == constants.INIT_POSITION:
            # All the commands (except PLACE command) are ignored until the robot is placed on the table.
            return (pos, dir)
        elif constants.LEFTCOMMAND == cmd:
            # if command is LEFT
            dir = self.command.turnLeft(dir)
        elif constants.RIGHTCOMMAND == cmd:
            # if command is RIGHT
            dir = self.command.turnRight(dir)
        elif constants.MOVECOMMAND == cmd:
            # if command is MOVE
            pos = self.command.move(pos, dir)
        elif constants.PLACECOMMAND == cmd:
            # if command is PLACE
            ret_val = self.command.place(cmd_str)
            if ret_val :
                # if the returned value is not None.
                pos, dir = ret_val
        else:
            raise CommandNotImplementedError(cmd + ": Command not implemented yet.")
        return (pos, dir)

    def extractCmd(self, clip):
        """
        extractCmd extracts the command and it's arguments.
        """
        clip = clip.strip()
        cmd_str = None
        cmd = clip.split(" ",1)[0]
        if len(clip.split(" ",1)) > 1:
            cmd_str = clip.split(" ",1)[1]
            cmd_str = "".join(cmd_str.split())
        
        return cmd, cmd_str

    def simulate(self, clip):
        """
        simulate function takes the raw command from the main function and 
        co-ordinates between extractCmd function and executeCmd function.
        """
        cmd, cmd_str = self.extractCmd(clip)

        if cmd in constants.COMMANDS:
            if cmd == constants.TRAVEL:
                # if command is TRAVEL a path will be returned
                path = self.executeCmd(cmd, cmd_str)
                print(f"path: {path}")
            else:
                pos, dir = self.executeCmd(cmd, cmd_str)
                # after executing the commands, update the configuration object 
                # with new position and direction of the robot.
                self.configuration.setPosition(pos)
                self.configuration.setDirection(dir)
        else:
            raise CommandNotFoundError(cmd + ": command not found.")
            
