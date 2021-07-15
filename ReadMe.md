# Toy Robot Simulator

## Description:

The application is a simulation of a toy robot moving on a square tabletop, of dimensions 5 units x 5 units. There are some potholes which are pre-defined, the movement of the robot needs to keep that in consideration and avoid falling into them. There are no other obstructions on the table surface.

* The robot is free to roam around the surface of the table, but must be prevented from falling to destruction. Any movement that would result in the robot falling from the table must be prevented, however further valid movement commands must still be allowed.

* This application can read in commands of the following form -
* * PLACE X,Y,F
* * MOVE
* * LEFT
* * RIGHT
* * REPORT
* * TRAVEL X,Y

- PLACE will put the toy robot on the table in position X,Y and facing NORTH, SOUTH, EAST or WEST.
The origin (0,0) can be considered to be the SOUTH WEST most corner.
The first valid command to the robot is a PLACE command, after that, any sequence of commands may be issued, in any order, including another PLACE command. The application should discard all commands in the sequence until a valid PLACE command has been executed.

- MOVE will move the toy robot one unit forward in the direction it is currently facing.

- LEFT and RIGHT will rotate the robot 90 degrees in the specified direction without changing the position of the robot.

- REPORT will announce the X,Y and orientation of the robot.

- TRAVEL with co-ordinates to travel to (destination) will announce one of the paths (sequence of co-ordinates) leading to the destination, if there exists a path from robots current position to destination.

* A robot that is not on the table can choose to ignore the MOVE, LEFT, RIGHT and REPORT commands.

* Constraints:
The toy robot must not fall off the table (either from the edges or into the potholes) during movement. This also includes the initial placement of the toy robot.
* * Any move that would cause the robot to fall must be ignored.

## Requirements:

Python 3

To run the test cases, install nose

## How to Run:

You can run the program using following command after git clone from command line interface:

1. To run in the interactive mode, run :-
    python __main__.py

    In this mode the program will accept, process and wait for commands from standard input until the command "Exit" or "exit" is entered.

2. To run using input files, run :-
    python __main__.py --inputfile filepath

    In this project there are 4 example input files inside "data" folder.

- Example inputs and outputs:
a)

PLACE 0,0,NORTH

MOVE

REPORT

Output: 0,1,NORTH

b)

PLACE 0,0,NORTH

LEFT

REPORT

Output: 0,0,WEST

c)

PLACE 0,0,NORTH

TRAVEL 1,0

Output: path: [(0, 0), (1, 0)]


* * All the commands are expected in capital, except "exit" command.

## Implementation:

- __main__.py file is the main file to start the program. Decision about interactive or non-interactive method of execution is taken here. Based on the method of execution the commands are either read from the file provided in the argument or are read from standard input.

- simulator.py file accepts the input from __main__.py file in the string format, further trims the input to extract commands.

- commands.py file executes all the commands.

- robo.py file keeps track of the table and robot (direction and position) information.

- basic folder contains a simple python program to implement the Robot Simulator with some basic test cases.
