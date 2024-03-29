
#GLOBAL VARIABLES
import time

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
    print('Evaluating with Transition Model: lastPos: {}, nextPos: {}, action: {}'.format(lastPostion, nextPosition, action))
    
    if (lastPostion == nextPosition):
        return 0.1
    else:
        if(action == 'up'):
            if(nextPosition[0] == lastPostion[0] - 1 and nextPosition[1] == lastPostion[1]):
                return 0.9
            else:
                return 0
        elif(action == 'down'):
            if(nextPosition[0] == lastPostion[0] + 1 and nextPosition[1] == lastPostion[1]):
                return 0.9
            else:
                return 0
        elif(action == 'left'):
            if(nextPosition[1] == lastPostion[1] - 1 and nextPosition[0] == lastPostion[0]):
                return 0.9
            else:
                return 0
        elif(action == 'right'):
            if(nextPosition[1] == lastPostion[1] + 1 and nextPosition[0] == lastPostion[0]):
                return 0.9
            else:
                return 0
        else:
            print('Unknown Action!')
    return -1


    
def main():
    start_time = time.time()
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
    
    def Normalize2D(distribution):
        total = 0
        for line in distribution:
            total += sum(line)
        alpha = 1 / total
        print('total: {}'.format(total))
        
        normDist = []
        for line in distribution:
            newLine = []
            for value in line:
                newVal = alpha * value
                newLine.append(newVal)
            normDist.append(newLine)  

        print('Before Normalize:')
        print(distribution)
        print('After Normalize:')
        print(normDist)
        
        return normDist
    
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
        result = [[0] * 3 for _ in range(3)] # init result map
        print(result)
        for x in range(1,4):
            for y in range(1,4):
                position = (x, y)
                probAtPos = observationModel[sensorData[i-1]]
                pObserve = probAtPos[myMap[x-1][y-1]]
                print('Position Reading : {}\n At Position: {}\nProbability:{}'.format(sensorData[i-1], position, pObserve))
                summation = 0
                # X2, Y2 IS LAST POSTION IN RELATION TO X, Y GIVEN ACTION a
                if (actions[i-1] == 'down'):
                    x2 = x  - 1
                    y2 = y
                    x3 = x
                    y3 = y
                elif(actions[i-1] == 'up'):
                    x2 = x + 1
                    y2 = y 
                    x3 = x
                    y3 = y
                elif (actions[i-1] == 'left'):
                    x2 = x 
                    y2 = y + 1
                    x3 = x
                    y3 = y
                elif(actions[i-1] == 'right'):
                    x2 = x
                    y2 = y - 1
                    x3 = x
                    y3 = y
                
                # Issue filter recalculated  everytime we want 1 value
                if(x2 < 4 and x2 > 0 and y2 < 4 and y2 > 0):
                    transitionVal = TransitionModel((x2, y2), (x, y), actions[i-1]) * filterRes[x2-1][y2-1]
                else:
                    transitionVal = 0
                print('Transition Model X2 * Filtering: {}'.format((transitionVal, actions[i-1])))
                transitionValAlt = TransitionModel((x3, y3), (x, y), actions[i-1]) * filterRes[x3-1][y3-1]
                print('Transition Model X3 * Filtering: {}'.format((transitionValAlt, actions[i-1])))
                summation += transitionVal + transitionValAlt
                print('Summation after iteration: {} : {}'.format(i, summation))
                result[x - 1][y - 1] = pObserve * summation
                    
                """ for x2 in range(1,4):
                    for y2 in range(1,4):
                        # Issue filter recalculated  everytime we want 1 value
                        transitionVal = TransitionModel((x2, y2), (x, y), actions[i-1]) * filterRes[x2-1][y2-1]
                        print('Transition Model * Filtering: {}'.format((transitionVal, actions[i-1])))
                        summation += transitionVal
                print('Summation after iteration: {} : {}'.format(i, summation))
                result[x - 1].append(pObserve * summation) """
                
        res = Normalize2D(result)
        return res
    
    res = Filter(3)
    print('------------ FILTERING ANSWER --------------\n')
    for line in res:
        print(line)
    
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()