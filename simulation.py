import os
from generalFilter import *
from ast import literal_eval


# Folder Path
CUR_DIR = os.getcwd()
PATHS_FOLDER = CUR_DIR + '\GroundTruths'
MAPS_FOLDER = CUR_DIR + '\Maps'
M = 100
N = 50

# Params: lastPostion Tuple(x, y), nextPosition Tuple(x, y), action = String
# return: P(X_i | X_{i-1}) according to transition model
def TransitionModel(lastPostion, nextPosition, action):
    print('Evaluating with Transition Model: lastPos: {}, nextPos: {}, action: {}'.format(lastPostion, nextPosition, action))
    
    if (lastPostion == nextPosition):
        return 0.1
    else:
        if(action == 'U'):
            if(nextPosition[0] == lastPostion[0] - 1 and nextPosition[1] == lastPostion[1]):
                return 0.9
            else:
                return 0
        elif(action == 'D'):
            if(nextPosition[0] == lastPostion[0] + 1 and nextPosition[1] == lastPostion[1]):
                return 0.9
            else:
                return 0
        elif(action == 'L'):
            if(nextPosition[1] == lastPostion[1] - 1 and nextPosition[0] == lastPostion[0]):
                return 0.9
            else:
                return 0
        elif(action == 'R'):
            if(nextPosition[1] == lastPostion[1] + 1 and nextPosition[0] == lastPostion[0]):
                return 0.9
            else:
                return 0
        else:
            print('Unknown Action!')
    return -1

def main():
    print(PATHS_FOLDER)
    
    initialProbability = 1 / (M * N) 
    priorDistribution = [[initialProbability] * N for _ in range(M)]
    
    observationModel = {'N':{'N': 0.9, 'H': 0.05, 'T': 0.05, 'B': 0},
                        'H':{'N': 0.05, 'H': 0.9, 'T': 0.05, 'B': 0},
                        'T':{'N': 0.05, 'H': 0.05, 'T': 0.9, 'B': 0}}
            
    # Loop 10 times for each map
    #for i in range(10):
    # Load map from file: 2D array of H, N, T, B strings
    filename = MAPS_FOLDER + '\map_' + str(1) + '.txt'
    items = []
    with open(filename, 'r') as f1:
        readData = f1.read()
        
    # If file did not close something went wrong
    if (not f1.closed):
        return -1
    
    myMap = literal_eval(readData)
    
    # Loop 10 times for each path
    #for k in range(10):
    filename = PATHS_FOLDER + '\map_' + str(1) + 'path_' + str(1) + '.txt'
    # Load ground truth file
    with open(filename) as f2:
        readData = f2.read()
        items = readData.split('\n')
        
    # If file did not close something went wrong
    if (not f2.closed):
        return -1
    
    """
    (x0, y0): coordinates of initial point (Tuple)
    [(xi, yi)]: coordinates of the consecutive points that the 
                agent actually visits (Array of Tuples)
    ai: 100 characters indicating the type of action executed
        {U, L, D, R}
    ei: 100 characters indicating the sensor reading {N, H, T}
    """
    
    initialPoint = literal_eval(items[0]) # Tuple
    groundCoords = literal_eval(items[1]) # Array: Tuple
    actions = literal_eval(items[2]) # Array: String
    groundSensorReadings = literal_eval(items[3]) # Array: String
    print(groundSensorReadings)
    
    # Imported from generalFilter.py
    result = Filter(3, actions, priorDistribution, groundSensorReadings, observationModel, TransitionModel, myMap, M, N)
    
    for line in result:
        print(line)
            
    print(len(priorDistribution[0]), len(priorDistribution), priorDistribution[0][0])
    return

if __name__ == "__main__":
    main()