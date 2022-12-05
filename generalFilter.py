
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
            return priorDistribution
        filterRes = Filter(i - 1, actions, priorDistribution, sensorData, observationModel, TransitionModel, myMap, M, N)
        result = [[] * M] * N # init result map
        for x in range(1, M + 1):
            for y in range(1, N + 1):
                position = (x, y)
                probAtPos = observationModel[sensorData[i-1]]
                pObserve = probAtPos[myMap[x-1][y-1]]
                print('Position Reading : {}\n At Position: {}\nProbability:{}'.format(sensorData[i-1], position, pObserve))
                summation = 0
                for x2 in range(1, M + 1):
                    for y2 in range(1, N + 1):
                        # Issue filter recalculated  everytime we want 1 value
                        transitionVal = TransitionModel((x2, y2), (x, y), actions[i-1]) * filterRes[x2-1][y2-1]
                        print('Transition Model * Filtering: {}'.format((transitionVal, actions[i-1])))
                        summation += transitionVal
                print('Summation after iteration: {} : {}'.format(i, summation))
                result[x - 1].append(pObserve * summation)
                
        res = Normalize2D(result)
        return res