import random
import os.path
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
M = 100
N = 50
TYPES = {'N': 0.5, 'H': 0.2, 'T': 0.2, 'B': 0.1}

# IMPORTANT: COORDINATES ARE IN (ROW, COL) FORMAT

# Creates file and writes information in specified format
def WriteToFile(initialPoint, myMap, actions, groundSensors, groundStates, filename):
    content = str(initialPoint) + '\n' + str(groundStates) + '\n' +str(actions) + '\n' +str(groundSensors)
    f = open(filename, "w")
    f.write(content) 
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
    for i in range(100):
        genActions.append(random.choice(possibleActions))
    return genActions

# Applys Transition Model to get the next position of the agent
# Params: currentState: Tuple(x, y), action: String
# Return: nextState: Tuple(x, y) postion of the agent after applying model
def GetNextState(currentState, action, myMap):
    nextState = (0, 0)
    rVal = random.random()
    if (rVal < 0.9):
        if(action == 'U'):
            nextState = (currentState[0] - 1, currentState[1])
        elif(action == 'D'):
            nextState = (currentState[0] + 1, currentState[1])
        elif(action == 'L'):
            nextState = (currentState[0], currentState[1] - 1)
        elif(action == 'R'):
            nextState = (currentState[0], currentState[1] + 1)
    else:
        return currentState
    
    if (nextState[0] < 0 or nextState[0] > M - 1):
        return currentState
    elif (nextState[1] < 0 or nextState[1] > N - 1):
        return currentState
    
    if (myMap[nextState[0]][nextState[1]] == 'B'):
        return currentState
    
    return nextState

# Applys Observation Model to get the sensor reading of the agent's position
# Params: currentState: Tuple(x, y)
# Return: reading: String -> sensor reading {N, H, T}
def GetSensorReading(currentState,myMap):
    locationX,locationY = currentState
    reading=myMap[locationX][locationY]
    return reading

# Prints a given 2D array row by row
def PrintMap(myMap):
    for line in myMap:
        print(line)
    return

def main():
    #generate list of maps
    mapStorage=[0 for j in range(10)]
    for k in range(10):
        mapStorage[k] = CreateMap()
        content = str(mapStorage[k]) 
        f = open("map_" + str(k + 1) + ".txt", "w")
        f.write(content) 
        """ print(mapStorage[k])
        print() """
    """ myMap = CreateMap()
    PrintMap(myMap)
    x0 = SelectStart(myMap)
    currentState=x0
    sensorList=[] """
    # print(x0)
    #generate list of actions
    actionStorage=[0 for j in range(100)]
    for i in range(100):
        actionsTaken=GenerateActions(['U', 'L', 'D', 'R'])
        actionStorage[i]=actionsTaken

#We need to use 10 maps 10 times so this first loop should itterate
    fileselector=0
    for m in range(10):
        myMap=mapStorage[m]
        #PrintMap(myMap)
        print("current map=")
        print(m)
        x0 = SelectStart(myMap)
        print("starting location =")
        print(x0)
        currentState=x0
        """ mvmtList=[0 for p in range(100)]
        mvmtList[0]=x0 """
        for a in range(10):
            sensorList=[]
            stateList = []
            actionList = GenerateActions(['U', 'L', 'D', 'R'])
            stateList.append(currentState)
            newState = currentState
            for x in range(100):
                #mvmtList[x]=currentState
                """ actionsTaken=actionStorage[x] """
                newState = GetNextState(newState, actionList[x], myMap)
                stateList.append(newState)
                currentReading = GetSensorReading(newState, myMap)
                sensorList.append(currentReading)
            filename="map_" + str(m + 1) + "path_" + str(a + 1) + ".txt"
            WriteToFile(x0, myMap, actionList, sensorList, stateList, filename)
    PrintMap(mapStorage[0])
    # TODO
    """ actionsTaken = GenerateActions(['U', 'L', 'D', 'R'])
    for i in range(100):
        newState = GetNextState(currentState, actionsTaken[i], myMap)
        print(newState)
        currentState=newState
        currentreading=GetSensorReading(currentState,myMap)
        sensorList.append(currentreading)
        print(GetSensorReading(currentState,myMap))
        WriteToFile(x0,myMap,actionsTaken,sensorList) """
    return

if __name__ == "__main__":
    main()