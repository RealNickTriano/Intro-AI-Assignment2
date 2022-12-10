import os
from tkinter.ttk import Combobox
#from generalFilter import *
from ast import literal_eval
import math
from tkinter import *
import time
from numpy import argmax
import random

# Folder Path
CUR_DIR = os.getcwd()
PATHS_FOLDER = CUR_DIR + '\GroundTruths'
MAPS_FOLDER = CUR_DIR + '\Maps'
M = 100
N = 50

#Tkinter constants
SIDE_LENGTH = 20
PADDING_X = 20
PADDING_Y = 20

# Globals for filtering
n = 100
filtersDict = {i: None for i in range(n + 1)}

# Globals for experiments
correctEstimationsArray = [] # Array containing arrays of 0s and 1s for each file
correctTotalsArray = [] # Array containing int for total correct guesses by filtering
errorsArray = []

root = Tk()
root.title('Filtering Visualization')
root.geometry("1920x1080")
    
# ---------------- TKINTER METHODS ----------------
def create_square(my_canvas, number, i, k):
    center = ((k * (SIDE_LENGTH)) + PADDING_X, (i * (SIDE_LENGTH)) + PADDING_Y)
    x1 = center[0] - (SIDE_LENGTH / 2)
    y1 = center[1] - (SIDE_LENGTH / 2)
    x2 = center[0] + (SIDE_LENGTH / 2)
    y2 = center[1] + (SIDE_LENGTH / 2)
    
    my_canvas.create_rectangle(x1, y1, x2, y2, outline = "black", fill='#fef2f2', width = 2, tags='({},{})'.format(i, k))
    return

def updateSquare(my_canvas, number, i, k):
    colorPicks = ['#fef2f2', '#fee2e2', '#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d', '#c2410c']
    if (number < 0.0002):
        color = 'white'
    elif (number < 0.025):
        color = colorPicks[0]
    elif (number < 0.05):
        color = colorPicks[1]
    elif (number < 0.075):
        color = colorPicks[2]
    elif (number < 0.1):
        color = colorPicks[3]
    elif (number < 0.15):
        color = colorPicks[4]
    elif (number < 0.175):
        color = colorPicks[5]
    elif (number < 0.2):
        color = colorPicks[6]
    elif (number < 0.3):
        color = colorPicks[7]
    elif (number < 0.4):
        color = colorPicks[8]
    elif (number < 0.5):
        color = colorPicks[9]
    else:
        color = colorPicks[10]
        
    tag = '({},{})'.format(i, k)
    my_canvas.itemconfigure(tag, fill=color)
    return
# -----------------------------------------------------------------

# Params: lastPostion Tuple(x, y), nextPosition Tuple(x, y), action = String
# return: P(X_i | X_{i-1}) according to transition model
def TransitionModel(lastPostion, nextPosition, action):
    #print('Evaluating with Transition Model: lastPos: {}, nextPos: {}, action: {}'.format(lastPostion, nextPosition, action))
    
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

# ---------------- FILTERING ----------------------
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
    
def Filter(i, actions, priorDistribution, sensorData, observationModel, TransitionModel, myMap, M, N, my_canvas, speed, groundCoords, collectData):
        if (i == 0):
            filtersDict[0] = priorDistribution
            return filtersDict[0]
        elif (filtersDict[i] is not None):
            return filtersDict[i]   
        
        filterRes = Filter(i - 1, actions, priorDistribution, sensorData, observationModel, TransitionModel, myMap, M, N, my_canvas, speed, groundCoords, collectData)
        result = [[0] * N for _ in range(M)] # init result map
        #print(len(result))
        for x in range(1, M + 1):
            for y in range(1, N + 1):
                position = (x, y)
                probAtPos = observationModel[sensorData[i-1]]
                pObserve = probAtPos[myMap[x-1][y-1]]
                #print('Position Reading : {}\n At Position: {}\nProbability:{}'.format(sensorData[i-1], position, pObserve))
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
                if(x2 < M and x2 > 0 and y2 < N and y2 > 0):
                    transitionVal = TransitionModel((x2, y2), (x, y), actions[i-1]) * filterRes[x2-1][y2-1]
                else:
                    transitionVal = 0
                #print('Transition Model X2 * Filtering: {}'.format((transitionVal, actions[i-1])))
                transitionValAlt = TransitionModel((x3, y3), (x, y), actions[i-1]) * filterRes[x3-1][y3-1]
                #print('Transition Model X3 * Filtering: {}'.format((transitionValAlt, actions[i-1])))
                summation += transitionVal + transitionValAlt
                #print('Summation after iteration: {} : {}'.format(i, summation))
                result[x - 1][y - 1] = pObserve * summation
                
        res = Normalize2D(result)
        filtersDict[i] = res
        for q in range(M):
            for k in range(N):
                updateSquare(my_canvas, res[q][k], q, k)
        tag = '({},{})'.format(groundCoords[i - 1][0], groundCoords[i - 1][1])
        my_canvas.itemconfigure(tag, fill='green')
        root.update_idletasks()
        root.update()
        maxi = max(map(max, res))
        print('Max: {}'.format(maxi))
        for j in range(M):
            for q in range(N):
                if(res[j][q] == maxi):
                    print('Pos: {}, {}'.format(j, q))
        time.sleep(speed)
        print(len(res))
        return res
# -------------------------------------------------

#TODO
def FilterWithFile(fileName, iteration, my_canvas, speed, collectData):
    global filtersDict
    filtersDict = {i: None for i in range(n + 1)}
    splits = fileName.split('path')
    print()
    myFile = MAPS_FOLDER + '\\' + splits[0] + '.txt'
    items = []
    with open(myFile, 'r') as f1:
        readData = f1.read()
        
    # If file did not close something went wrong
    if (not f1.closed):
        return -1
    
    myMap = literal_eval(readData)
    
    # Loop 10 times for each path
    #for k in range(10):
    myFile = PATHS_FOLDER + '\\' + fileName
    # Load ground truth file
    with open(myFile) as f2:
        readData = f2.read()
        items = readData.split('\n')
        
    # If file did not close something went wrong
    if (not f2.closed):
        return -1
    
    initialProbability = 1 / (M * N) 
    priorDistribution = [[initialProbability] * N for _ in range(M)]
    
    observationModel = {'N':{'N': 0.9, 'H': 0.05, 'T': 0.05, 'B': 0},
                        'H':{'N': 0.05, 'H': 0.9, 'T': 0.05, 'B': 0},
                        'T':{'N': 0.05, 'H': 0.05, 'T': 0.9, 'B': 0}}
                        
    initialPoint = literal_eval(items[0]) # Tuple
    groundCoords = literal_eval(items[1]) # Array: Tuple
    actions = literal_eval(items[2]) # Array: String
    groundSensorReadings = literal_eval(items[3]) # Array: String
    print(groundSensorReadings)
    
    result = Filter(iteration, actions, priorDistribution, groundSensorReadings, observationModel, TransitionModel, myMap, M, N, my_canvas, speed, groundCoords, collectData)
    
    print(len(priorDistribution[0]), len(priorDistribution), priorDistribution[0][0])
    maxi = max(map(max, result))
    maxiIndex = (0, 0)
    print(maxi)
    """ for j in range(M):
        for q in range(N):
            if(result[j][q] == maxi):
                maxiIndex = (j, q)
                print(j, q) """
    
    # Experiment Data collection
    if (collectData):
        # track distance from truth to guess at each iteration
        # track when guess is equal to ground truth at each iteration
        correctEstimate = 0
        correctionArray = []
        currErrors = []
        print('Collecting Data')
        for iter in range(6, iteration + 1):
            maxArray = []
            # Find max in result
            maxRes = max(map(max, filtersDict[iter]))
            for j in range(M):
                for q in range(N):
                    if(filtersDict[iter][j][q] == maxRes):
                        maxArray.append((j, q))
            # Get ground truth at iter
            truthPos = groundCoords[iter - 1]
            maxiResPos = random.choice(maxArray)
            # Compute distance
            distX = abs(truthPos[0] - maxiResPos[0])
            distY = abs(truthPos[1] - maxiResPos[1])
            error = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)) # Error = straight line distance
            print(error)
            currErrors.append(error)
            # If equal increase counter
            print('Truth: {}'.format(truthPos))
            print('Estimate: {}'.format(maxiResPos))
            if (truthPos == maxiResPos):
                correctEstimate += 1
                correctionArray.append(1)
            else:
                correctionArray.append(0) 
            # Else continue 
        # Calculate     
        correctEstimationsArray.append(correctionArray)
        correctTotalsArray.append(correctEstimate)
        errorsArray.append(currErrors)
        print('Correct Estimations By Iteration:')
        print(correctEstimationsArray)
        print('Correct Estimation Totals:')
        print(correctTotalsArray)
        print('All Errors:')
        print(errorsArray)
    
    return

def main():
    print(PATHS_FOLDER)

    my_canvas = Canvas(root, width=1920, height=1080, bg="white")
    my_canvas.pack(pady=20)
           
    def _on_mousewheel(event):
        if event.delta < 0:
            my_canvas.yview_scroll(1, "units")
        else:
            my_canvas.yview_scroll(-1, "units")

    root.bind("<MouseWheel>", _on_mousewheel)
    
    def _on_filterbutton():
        iterations = int(iterationSelect.get())
        if (iterations not in range(1, 101)):
            print('Number should be 1-100')
            return
        print(iterations)
        return
    
    def _on_mapbutton():
        fileToDisplay = mapPathSelection.get()
        if (fileToDisplay == ''):
            print('Select a File to proceed.')
            return
        FilterWithFile(fileToDisplay, int(iterationSelect.get()), my_canvas, int(speedSelect.get()), False)
        return
    
    def _on_experiment():
        print('Running 100 Experiments. Its gonna be a while.')
        # collectData = Flag to start collecting error estimates and stuff
        # What do we need to keep track off?
        """
            1) For each file, compute error, as 
                distance in grid world between true 
                location and maxi value at each iteration (ties broken randomly)
            2) For each file, keep track of when maxi cell is actual cell,
                at each iteration
        """
        fileToDisplay = mapPathSelection.get()
        if (fileToDisplay == ''):
            print('Select a File to proceed.')
            return
        FilterWithFile(fileToDisplay, int(iterationSelect.get()), my_canvas, int(speedSelect.get()), True)
        # After we get all values filled in array
        # For correctEstimationsArray sum all values of the same iteration
            # totals = []
            # For each line in correctEstimationsArray:
                # totals.append(totals[i] += line[0])Sum line[0]
            # Take average so, for each in totals, totals[i] / 100
                
        # For correctTotalsArray
            # Sum all and average
            
        # For errorsArray
            # Do same as correctEstimationsArray
        return
        
    files = os.listdir(PATHS_FOLDER)
    
    iterationSelect = Spinbox(my_canvas, justify="left",from_=1, to=100)
    iterationSelect.place(relx=0.9, rely=0.1, anchor=CENTER)
    
    filterButton = Button(my_canvas, justify=CENTER, text='Filter', command=_on_filterbutton)
    filterButton.place(relx=0.95, rely=0.1, anchor=CENTER)
    
    
    mapPathSelection = Combobox(my_canvas, justify='left', text='Filter', values=files)
    mapPathSelection.place(relx=0.90, rely=0.15, anchor=CENTER)
    
    filterButton = Button(my_canvas, justify=CENTER, text='Load Map', command=_on_mapbutton)
    filterButton.place(relx=0.96, rely=0.15, anchor=CENTER)
    
    speedSelectLabel = Label(my_canvas, text='Select time between steps', bg='white')
    speedSelectLabel.place(relx=0.83, rely=0.2, anchor=CENTER)
    
    speedSelect = Spinbox(my_canvas, justify="left",from_=0, to=5)
    speedSelect.place(relx=0.92, rely=0.2, anchor=CENTER)
    
    pathSelectLabel = Label(my_canvas, text='Select Map/Path', bg='white')
    iterationSelectLabel = Label(my_canvas, text='Select Iteration', bg='white')
    iterationSelectLabel.place(relx=0.82, rely=0.1, anchor=CENTER)
    pathSelectLabel.place(relx=0.82, rely=0.15, anchor=CENTER)
    
    experimentButton = Button(my_canvas, justify=CENTER, text='Run Experiment', command=_on_experiment)
    experimentButton.place(relx=0.90, rely=0.25, anchor=CENTER)
    
    
            
    # Loop 10 times for each map
    #for i in range(10):
    # Load map from file: 2D array of H, N, T, B strings
    
    
    """
    (x0, y0): coordinates of initial point (Tuple)
    [(xi, yi)]: coordinates of the consecutive points that the 
                agent actually visits (Array of Tuples)
    ai: 100 characters indicating the type of action executed
        {U, L, D, R}
    ei: 100 characters indicating the sensor reading {N, H, T}
    """
    
    # Draw Grid
    for i in range(M):
        for k in range(N):
            create_square(my_canvas, 0, i, k)
            
    """  """
    
    # Imported from generalFilter.py
    
    
    """ for line in result:
        print(line)
            
     """
    
     
    
    
    root.mainloop()
    
    return

if __name__ == "__main__":
    main()