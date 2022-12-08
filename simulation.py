import os
from generalFilter import *
from ast import literal_eval
import math
from tkinter import *

# Folder Path
CUR_DIR = os.getcwd()
PATHS_FOLDER = CUR_DIR + '\GroundTruths'
MAPS_FOLDER = CUR_DIR + '\Maps'
M = 100
N = 50

#Tkinter constants
SIDE_LENGTH = 30
PADDING_X = 20
PADDING_Y = 20

# ---------------- TKINTER METHODS ----------------
def create_square(my_canvas, number, i, k):
    center = ((k * (SIDE_LENGTH)) + PADDING_X, (i * (SIDE_LENGTH)) + PADDING_Y)
    print(center)
    x1 = center[0] - (SIDE_LENGTH / 2)
    y1 = center[1] - (SIDE_LENGTH / 2)
    x2 = center[0] + (SIDE_LENGTH / 2)
    y2 = center[1] + (SIDE_LENGTH / 2)
    colorPicks = []
    if (number < 0.2):
        color = 'red'
    else:
        color = 'green'
    my_canvas.create_rectangle(x1, y1, x2, y2, outline = "black", fill=color, width = 2)
    
    return



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
    
    root = Tk()
    root.title('Codemy.com -  Canvas')
    root.geometry("1920x1080")
    root.wm_attributes("-transparentcolor", 'grey')

    my_canvas = Canvas(root, width=1920, height=1080, bg="white")
    my_canvas.pack(pady=20)
           
    def _on_mousewheel(event):
        if event.delta < 0:
            my_canvas.yview_scroll(1, "units")
        else:
            my_canvas.yview_scroll(-1, "units")

    root.bind("<MouseWheel>", _on_mousewheel)
    
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
    result = Filter(100, actions, priorDistribution, groundSensorReadings, observationModel, TransitionModel, myMap, M, N)
    
    for line in result:
        print(line)
            
    print(len(priorDistribution[0]), len(priorDistribution), priorDistribution[0][0])
    print(max(map(max, result)))
    
    for i in range(M):
        for k in range(N):
            create_square(my_canvas, result[i][k], i, k)
    
    root.mainloop()
    
    return

if __name__ == "__main__":
    main()