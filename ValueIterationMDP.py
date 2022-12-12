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

convergencediff=0.001

stateVal=[0,0,1,0]

while True:
    largestDiff=0
    for i in range(len(states)):
        stateholder=states[i]
        val=0
        bestaction=[0,0]
        actioncount=0
        for j in range(len(actions)):
            actionholder=actions[j]
            if actionholder in transitionProb[stateholder]:
                for k in range(len(states)):
                    nextstateholder=states[k]
                    if actionholder in transitionProb[stateholder] and nextstateholder in transitionProb[stateholder][actionholder]:                   
                        #the problem is here, its adding values from both actions and not just both outcomes
                        #from 1 action
                        #potential solution, a tuple containing both actions respective outcomes and 
                        #taking max on it
                        utility=gama*stateVal[k]*transitionProb[stateholder][actionholder][nextstateholder]
                        val+=utility
                bestaction[actioncount]=val
                actioncount+=1
            
        test=max(bestaction)
        print(test)
        val+=rewards[i]
        diff=abs(stateVal[i]-val)
        largestDiff=max(largestDiff,diff)
        stateVal[i]=val
        print(stateVal)
    if largestDiff<=convergencediff:
        break
print(stateVal)

for i in range(len(states)):
    stateholder=states[i]
    utilities=[]
    for j in range(len(actions)):
        actionholder=actions[j]
        newutilityshort=0
        for k in range(len(states)):
                nextstateholder=states[k]
                if actionholder in transitionProb[stateholder] and nextstateholder in transitionProb[stateholder][actionholder]:
                    newutilityshort=newutilityshort+transitionProb[stateholder][actionholder][nextstateholder]*rewards[k]
        newutilitylong=0    
        for j in range(len(states)):
                nextstateholder=states[j]
                if actionholder in transitionProb[stateholder] and nextstateholder in transitionProb[stateholder][actionholder]:
                    newutilitylong=newutilitylong+transitionProb[stateholder][actionholder][nextstateholder]*stateVal[j]
        utilityofnextstate= gama*newutilitylong+newutilityshort
        utilities.append(utilityofnextstate)
        

