import random

class Node():
    def __init__(self, name, table):
        self.name = name
        self.table = table

def Normalize(a, b):
    alpha = 1/(a+b)
    normA = a * alpha
    normB = b * alpha
    
    return (normA, normB)
    
def main():
    A = Node('A', [[True, 0.0]])
    B = Node('B', [[True, 0.9]])
    C = Node('C', {(True, True): 0.2,
                   (True, False): 0.6,
                   (False, True): 0.5,
                   (False, False): 0.0})
    D = Node('D', {(True, True): 0.75,
                   (True, False): 0.1,
                   (False, True): 0.5,
                   (False, False): 0.2})
    print(A.name, A.table)
    print(B.name, B.table)
    print(C.name, C.table)
    print(D.name, D.table)
    # we want to find P(A,B,c,d)
    """
    Sample network 1000 times
    Reject samples which have not c or not d
    Normalize
    """
    """
    How to use:
    1) Identify Evidence variables (variables after | sign)
    2) Force these values to be true
    3) let w = w * P(Node.table[(parent, parent)])
    4) after for loop change D_value to ur desired value
    """
    results = []
    for i in range(1,11):
        samples = i * 100
        rejected = 0
        kept = 0
        wpassed = 0
        wfailed = 0
        weightArray = [0, 0]
        for i in range(samples):
            
            A_value = False
            B_value = None
            C_value = True
            D_value = True
            w = 1
            
            # Sample B
            B_distribution = (B.table[0][1], round(1 - B.table[0][1], 1))
            """ if (random.random() < B_distribution[0]):
                B_value = True
            else:
                B_value = False """
            B_value = False
            w = w * B.table[0][1]
            print(B_distribution)
            print(B_value)
            
            #Sample C
            C_distribution = (C.table[(A_value, B_value)], round(1 - C.table[(A_value, B_value)], 1))
            
            if (random.random() < C_distribution[0]):
                C_value = True
            else:
                C_value = False
                
            """ C_value = True
            w = w * C.table[(A_value, B_value)] """
            print(C_distribution)
            print(C_value)
            
            #Sample D
            D_distribution = (D.table[(B_value, C_value)], round(1 - D.table[(B_value, C_value)], 1))
            if (random.random() < D_distribution[0]):
                D_value = True
            else:
                D_value = False
            print(D_distribution)
            print(D_value)
            
            print('WEIGHT:')
            print(w)
            # Change value here
            if(D_value):
                weightArray[0] += w
            else:
                weightArray[1] += w
        
        total = weightArray[0] + weightArray[1]
        print('Rejected, Kept')        
        print(rejected, kept)
        print('Passed, Failed')        
        print(weightArray[0]/total, weightArray[1]/total)
        results.append((weightArray[0]/total, weightArray[1]/total))
    for res in results:
        print(res[0])
    
if __name__ == "__main__":
    main()
