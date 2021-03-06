# constants.py
# ------------------------------
# Author: Ankita Dhar <githubid: ankitadhar>

NORTH = "NORTH"
EAST = "EAST"
SOUTH = "SOUTH"
WEST = "WEST"
DIRECTIONS = [NORTH,EAST,SOUTH,WEST] # directions allowed
PLACECOMMAND = "PLACE"
LEFTCOMMAND = "LEFT"
RIGHTCOMMAND = "RIGHT"
MOVECOMMAND = "MOVE"
REPORTCOMMAND = "REPORT"
COMMANDS = [PLACECOMMAND,LEFTCOMMAND,RIGHTCOMMAND,MOVECOMMAND,REPORTCOMMAND] # commands allowed
INIT_DIRECTION = None # No initial direction for the robot
INIT_POSITION = (-1,-1) # initial out of the table position of robot
GRID_HEIGHT = 5 # height of the table
GRID_WIDTH = 5 # width of the table


### for basic
YPOS_MIN = 0
XPOS_MIN = 0
YPOS_MAX = 4
XPOS_MAX = 4