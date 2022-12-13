import time


states=["s1","s2","s3","s4"]

actions=["a1","a2","a3","a4"]

transitionProb={
    's1': {
        'a1': {'s1': 0.2, 's2': 0.8},
        'a2': {'s1': 0.2, 's4': 0.8},
        
    },
    's2': {
    
        'a2': {'s2': 0.2, 's3': 0.8},
        'a3': {'s2': 0.2, 's1': 0.8}
    },
    's3': {
        'a3': {'s4': 1},
        'a4': {'s2': 1},
        
    },
    's4': {
    
        'a1': {'s4': 0.1, 's3': 0.9},
        'a4': {'s4': 0.2, 's1': 0.8}
    },
}

rewards=[0,0,1,0]

gama=.1

convergencediff=0.00001

stateVal=[0,0,1,0]
print('0)', stateVal)
print('')
startTime = time.time()
iterations = 0
while True:
    iterations += 1
    vkplus1StateVal=[0,0,0,0]
    for i in range(len(states)):
        stateholder=states[i]
        newReward = 0
        bestaction=[0, 0, 0, 0]
        actioncount=0
        p=0
        for j in range(len(actions)):
            actionholder=actions[j]
            val1 = 0
            if actionholder in transitionProb[stateholder]:
                for k in range(len(states)):
                    nextstateholder=states[k]
                    if nextstateholder in transitionProb[stateholder][actionholder]:
                        #the problem is here, its adding values from both actions and not just both outcomes
                        #from 1 action
                        #potential solution, a tuple containing both actions respective outcomes and 
                        #taking max on it
                        #s1,a1,s1 .2   s1,a1,s2 .6
                        "s1->s2+s1->s1" "s1->s4+s1->s4"
                        utility = stateVal[k]*transitionProb[stateholder][actionholder][nextstateholder]
                        val1 += utility
                bestaction[j] = val1 * gama + rewards[i]
                


        best = max(bestaction)
        #print(best)
        vkplus1StateVal[i] = best
        bestpolly=bestaction.index(best)
        print("for state" , states[i], "best policy is", actions[bestpolly])
        newReward =  best + rewards[i]
    
    largestDiff = 0
    for q in range(len(stateVal)):
        diff = abs(stateVal[q] - vkplus1StateVal[q])
        largestDiff = max(largestDiff,diff)
    stateVal = vkplus1StateVal
    print(iterations,')',stateVal)
    print('')
    if largestDiff <= convergencediff:
        break
    
print("The final utilities are", stateVal)
print('Iterations: {}'.format(iterations))
print('Time: {}'.format(time.time() - startTime))


