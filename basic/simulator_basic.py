import argparse
import constants

directions = constants.DIRECTIONS
cur_dir = constants.INIT_DIRECTION
cur_pos = constants.INIT_POSITION

def executeCmd(cmd, cmd_str):
    """
    executeCmd executes all the user commands
    """
    global cur_dir
    global cur_pos
    x,y = cur_pos
    index = -1
    if cur_dir: index = directions.index(cur_dir)

    if constants.LEFTCOMMAND == cmd:
        cur_dir = directions[index-1]
    elif constants.RIGHTCOMMAND == cmd:
        new_index = index + 1
        if 4 == new_index:
            new_index = 0
        cur_dir = directions[new_index]
    elif constants.MOVECOMMAND == cmd:
        move = 1
        if index in [2,3]: 
            move = -1
        if index in [0,2]:
            new_y = y + move
            if new_y >= constants.YPOS_MIN and new_y <= constants.YPOS_MAX:
                y = new_y
        else:
            new_x = x + move
            if new_x >= constants.XPOS_MIN and new_x <= constants.XPOS_MAX:
                x = new_x
        cur_pos = (x,y)
    elif constants.REPORTCOMMAND == cmd:
        if cur_pos == constants.INIT_POSITION:
            print("\nRobot not placed on the board.\nPlace the robot using PLACE command.\n")
        else:
            print(str(x)+','+str(y)+','+cur_dir)
    elif constants.PLACECOMMAND == cmd:
        x,y,dir = cmd_str.split(',')
        if dir in directions and x.isnumeric() and y.isnumeric():
            x = int(x)
            y = int(y)
            if y >= constants.YPOS_MIN and y <= constants.YPOS_MAX and x >= constants.XPOS_MIN and x <= constants.XPOS_MAX:
                cur_pos = (x,y)
                cur_dir = dir
    else:
        print("Command not implemented yet.")

def extractCmd(clip):
    """
    this function extracts command and calls the execute function.
    """
    clip = clip.strip()
    cmd_str = None
    cmd = clip.split(" ",1)[0]
    if len(clip.split(" ",1)) > 1:
        cmd_str = clip.split(" ",1)[1]
        cmd_str = "".join(cmd_str.split())
    if "" != cmd and cmd not in constants.COMMANDS:
        print("\nInvalid Command. Try again \n")
    elif "PLACE" != cmd and not cur_dir:
        print("\nRobot not placed on the board.\nPlace the robot using PLACE command.\n")
    elif "PLACE" == cmd and not cmd_str:
        print("\nPLACE command needs parameters in the following format:\nPLACE x,y,direction\n")
    else:
        executeCmd(cmd, cmd_str)
    
    return (cur_pos,cur_dir)

def interactive():
    """
    while running in the interactive mode this function is executed
    """
    clip = input()
    pos = (-1,-1)
    while("exit" != clip.lower()):
        extractCmd(clip)
        clip = input()

def main():
    """
    Main function of the program.
    if --inputfile is provided then the commands are read and run from the file
    otherwise the code is run in interactive mode until 'exit' is entered from the standard input.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputfile", help="Filepath of tweets")
    args = parser.parse_args()
    if (not args.inputfile):
        interactive()
    else: 
        file = open(args.inputfile, 'r')
        cmd_list = file.readlines()
        
        count = 0
        # Strips the newline character
        for cmd in cmd_list:
            count += 1
            extractCmd(cmd)

if __name__ == "__main__":
    main()