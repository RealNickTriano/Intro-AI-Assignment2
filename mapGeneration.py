import random
"""
Rules:
    Large maps: 100 by 50
    Randomly assign types to each cell: 50% N, 20% H, 20% T, 10% B
    First, generate sequences of actions and sensor readings
        start at randomly selected non-blocked cell x_0
        then gen sequence of 100 actions: String of length 100 from {U, D, L, R}
        for each action apply transition model and observation model
            to get next state and sensor reading
    
    File Format:
    x0 y0 : coordinates of initial point
    x_i y_i : 100 coordinates of the consecutive points that the agent actually visits (the ground truth
    states) separated by a new line
    a_i : 100 characters indicating the type of action executed {U, L, D, R} separated by a new line
    e_i : 100 characters indicating the sensor reading {N, H, T} collected by the agent as it moves
"""

# GLOBAL VARIABLES
M = 10
N = 10
TYPES = {'N': 0.5, 'H': 0.2, 'T': 0.2, 'B': 0.1}

# IMPORTANT: COORDINATES ARE IN (ROW, COL) FORMAT

# Creates file and writes information in specified format
def WriteToFile(initialPoint, groundStates, actions, groundSensors):
    return 1

# Creates 2D array of size 100 x 50. 
# Each value is a character that corresponds to terrain type
def CreateMap():
    """
        Randomly assign types to each cell: 50% N, 20% H, 20% T, 10% B
    """
    nCount = 0
    hCount = 0
    tCount = 0
    bCount = 0
    myMap = []
    for x in range(M):
        row = []
        for y in range(N):
            assignment = None
            rVal = random.random()
            if (rVal <= 0.1):
                assignment = 'B'
                bCount += 1
            elif (rVal <= 0.3):
                assignment = 'T'
                tCount += 1
            elif (rVal <= 0.5):
                assignment = 'H'
                hCount += 1
            else:
                assignment = 'N'
                nCount += 1
            row.append(assignment)
        myMap.append(row)
            
    return myMap

# Params: 2D array representing our map
# Return: randomly selected non-blocked cell x_0
def SelectStart(myMap):
    
    x0 = (0, 0)
    row = random.randrange(0, M)
    col = random.randrange(0, N)
    if (myMap[row][col] != 'B'):
        return (row, col)
    else:
        row1 = row
        col1 = col
        while (myMap[row1][col1] == 'B'):
            print('B: {} map: {}'.format((row1,col1), myMap[row1][col1]))
            row1 = random.randrange(0, M)
            col1 = random.randrange(0, N)
        return (row1, col1)   

# Params: list of possible actions
# Return: sequence of 100 actions randomly selected from the list
def GenerateActions(possibleActions):
    genActions = []
    return genActions

# Applys Transition Model to get the next position of the agent
# Params: currentState: Tuple(x, y), action: String
# Return: nextState: Tuple(x, y) postion of the agent after applying model
def GetNextState(currentState, action):

    nextState = (0, 0)
    return nextState

# Applys Observation Model to get the sensor reading of the agent's position
# Params: currentState: Tuple(x, y)
# Return: reading: String -> sensor reading {N, H, T}
def GetSensorReading(currentState):
    
    nextState = (0, 0)
    return nextState

# Prints a given 2D array row by row
def PrintMap(myMap):
    for line in myMap:
        print(line)
    return

def main():
    myMap = CreateMap()
    PrintMap(myMap)
    x0 = SelectStart(myMap)
    print(x0)
    
    # TODO
    GenerateActions(['U', 'L', 'D', 'R'])
    GetNextState((0, 0), 'U')
    GetSensorReading((0,0))
    return

if __name__ == "__main__":
    main()