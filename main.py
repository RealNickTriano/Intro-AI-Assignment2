
#GLOBAL VARIABLES


class Space:
    
    # Attributes: 
        # pos Tuple(x, y), 
        # prob Float(proability of being at this space)
        # terrainType String in ['N', 'H', 'T', 'B']
    def __init__(self, pos, prob, terrainType):
        self.pos = pos
        self.prob = prob
        self.terrainType = terrainType

# Params: lastPostion Tuple(x, y), nextPosition Tuple(x, y), action = String
# return: P(X_i | X_{i-1}) according to transition model
def TransitionModel(lastPostion, nextPosition, action):
    if (lastPostion == nextPosition):
        return 0.1
    else:
        if(action == 'up'):
            if(nextPosition[1] + 1 == lastPostion[1]):
                return 0.9
            else:
                return 0
        elif(action == 'down'):
            if(nextPosition[1] - 1 == lastPostion[1]):
                return 0.9
            else:
                return 0
        elif(action == 'left'):
            if(nextPosition[0] - 1 == lastPostion[0]):
                return 0.9
            else:
                return 0
        elif(action == 'right'):
            if(nextPosition[0] + 1 == lastPostion[0]):
                return 0.9
            else:
                return 0
        else:
            print('Unknown Action!')
    return -1


    
def main():
    possibleActions = ['up, down, left, right']
    possibleTerrainType = ['N', 'H', 'T', 'B']
    observationModel = {'N':{'N': 0.9, 'H': 0.05, 'T': 0.05, 'B': 0},
                        'H':{'N': 0.05, 'H': 0.9, 'T': 0.05, 'B': 0},
                        'T':{'N': 0.05, 'H': 0.05, 'T': 0.9, 'B': 0}}
    actions = ['right', 'right', 'down', 'down']
    sensorData = ['N', 'N', 'H', 'H']
    myMap = [['H', 'H', 'T'],
             ['N', 'N', 'N'],
             ['N', 'B', 'H']]
    
    # Calculates Filtering for iteration i
    # Params: i Int: number of iterations
    # Return: Probabiltiy Distribution for iteration i
    # Ex: [0.2, 0.23, 0.42,
    # 0.02, 0.023, 0.42,
    # 0.024, 0, 0.0042]
    def Filter(i):
        if (i == 0):
            return [[0.125, 0.125, 0.125],
                    [0.125, 0.125, 0.125],
                    [0.125, 0.125, 0.125]]
        filterRes = Filter(i - 1)
        result = [[],
                  [],
                  []]
        for x in range(1,4):
            for y in range(1,4):
                position = (x, y)
                pObserve = observationModel[sensorData[i-1]][myMap[x-1][y-1]]
                summation = 0
                for x2 in range(1,4):
                    for y2 in range(1,4):
                        # Issue filter recalculated  everytime we want 1 value
                        summation += TransitionModel((x2, y2), (x, y), actions[i-1]) * filterRes[x2-1][y2-1]
                result[x - 1].append(pObserve * summation)
        return result
    
    res = Filter(1)
    for line in res:
        print(line)
    
    

if __name__ == "__main__":
    main()