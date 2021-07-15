# __main__.py
# ------------------------------
# Author: Ankita Dhar <githubid: ankitadhar>
#
# This is a python program to implement toy robot movement on 5 x 5 unit table
# This file can be run using command line interface
# series of commands can be provided to the program, pressing "Enter/Return" key after each command
# to quit the program enter "exit"/"Exit" and press enter
# Following commands are accepted (All Caps):
# 1. PLACE <X,Y,DIRECTION>
#           X <- x coordinate of robot
#           Y <- y coordinate of robot
#           DIRECTION <- either of the four directions that the robot faces
# 2. MOVE
# 3. LEFT
# 4. RIGHT
# 5. REPORT
# 6. TRAVEL <X,Y>
#           X <- x coordinate of destination
#           Y <- y coordinate of destination
#

from simulator import Simulator
import argparse

def main():
    """
    Main function of the program.
    if --inputfile is provided then the commands are read and run from the file
    otherwise the code is run in interactive mode until 'exit' is entered from the standard input.
    """
    simulator = Simulator()

    parser = argparse.ArgumentParser()
    parser.add_argument("--inputfile", help="Filepath of tweets")
    args = parser.parse_args()
    if (not args.inputfile):
        # interactive mode
        clip = input()
        while("exit" != clip.lower()):
            try :
                # each command is simulated throught the simulator instance
                simulator.simulate(clip)
            except Exception as e:
                print(e)
            clip = input()
    else: 
        # non-interactive mode
        file = open(args.inputfile, 'r')
        cmd_list = file.readlines()
        
        # Strips the newline character
        for cmd in cmd_list:
            try :
                # each command from the file is simulated throught the simulator instance
                simulator.simulate(cmd)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()