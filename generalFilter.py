
n = 100
filtersDict = {i: None for i in range(n + 1)}
print(filtersDict)        

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
        
        return normDist
    
def Filter(i, actions, priorDistribution, sensorData, observationModel, TransitionModel, myMap, M, N):
        if (i == 0):
            filtersDict[0] = priorDistribution
            return filtersDict[0]
        elif (filtersDict[i] is not None):
            return filtersDict[i]   
        
        filterRes = Filter(i - 1, actions, priorDistribution, sensorData, observationModel, TransitionModel, myMap, M, N)
        result = [[0] * N for _ in range(M)] # init result map
        print(len(result))
        for x in range(1, M + 1):
            for y in range(1, N + 1):
                position = (x, y)
                probAtPos = observationModel[sensorData[i-1]]
                pObserve = probAtPos[myMap[x-1][y-1]]
                print('Position Reading : {}\n At Position: {}\nProbability:{}'.format(sensorData[i-1], position, pObserve))
                summation = 0
                # X2, Y2 IS LAST POSTION IN RELATION TO X, Y GIVEN ACTION a
                if (actions[i-1] == 'D'):
                    x2 = x  - 1
                    y2 = y
                    x3 = x
                    y3 = y
                elif(actions[i-1] == 'U'):
                    x2 = x + 1
                    y2 = y 
                    x3 = x
                    y3 = y
                elif (actions[i-1] == 'L'):
                    x2 = x 
                    y2 = y + 1
                    x3 = x
                    y3 = y
                elif(actions[i-1] == 'R'):
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
                
        res = Normalize2D(result)
        filtersDict[i] = res
        print(len(res))
        return res