import random
import time
import math

# File Format:
# Each line format should be "Order,A,B"
# Ex.
# 1,0.43,0.52
# 2,0.59,0.678
# 3,0.023,0.134
# ...

#--------- Classes -----------#

class Vane:

    def __init__(self, order, A, B):
        self.order = order
        self.A = A
        self.B = B

#-------- Functions ---------#

def compute_avg_area(vanes):
    totalArea = 0.0
    numVanes = len(vanes)
    
    for i in range(numVanes):
        totalArea += vanes[i].A + vanes[i].B
        
    return totalArea / numVanes
    
def compute_dist(vanes, avgArea):
    score = 0.0
    numVanes = len(vanes)
    
    for i in range(numVanes - 1):
        score += abs(avgArea - vanes[i].A - vanes[i+1].B)
        
    score += abs(avgArea - vanes[numVanes - 1].A - vanes[0].B)
    
    return score

def reduce_temp(temp, min_temp, alpha):
    if (temp*alpha <= min_temp):
        return min_temp
    else:
        return temp * alpha

def random_swap(vanes):
    a = random.randrange(0, len(vanes))
    b = random.randrange(0, len(vanes) - 1)
    
    if b >= a:
        b = b + 1
    
    temp = vanes[a]
    vanes[a] = vanes[b]
    vanes[b] = temp

def check_acceptance(nextDist, bestDist, temp):
    if nextDist <= bestDist:
        return True
    else:
        delta = bestDist - nextDist
        p_acceptance = math.exp(delta/temp)
        x = random.uniform(0, 1)
        
        if x < p_acceptance:
            return True
        else:
            return False

def check_match(set1, set2):
    if len(set1) != len(set2):
        return False
    
    for i in range(len(set1)):
        if set1[i].order != set2[i].order:
            return False
    
    return True
    
def get_input_vanes():
    file = input("Enter input file name (press enter to default to \"dataset.txt\"): ")

    if file == "":
        file = "dataset.txt"

    fin = open(file)

    vanes = []

    for line in fin:
        spline = line.split(",")
        vanes.append(Vane(int(spline[0]), float(spline[1]), float(spline[2])))
    
    fin.close()
    
    return vanes

#--------- Program ----------#

vanes = get_input_vanes()

start = time.perf_counter()

avgArea = compute_avg_area(vanes)

bestVanes = vanes
random.shuffle(bestVanes)
bestDist = compute_dist(bestVanes, avgArea)

alpha = 0.9
temp = 10
final_temp = 0.0001
numIterations = 1000
numSwaps = 1

done = False

while not(done):
    curVanes = list(bestVanes)

    for i in range(numIterations):
        nextVanes = list(bestVanes)
        for j in range(numSwaps):
            random_swap(nextVanes)
        
        nextDist = compute_dist(nextVanes, avgArea)
        
        if check_acceptance(nextDist, bestDist, temp):
            bestDist = nextDist
            bestVanes = nextVanes
    
    if temp == final_temp and check_match(bestVanes, curVanes):
        done = True
    
    temp = reduce_temp(temp, final_temp, alpha)

end = time.perf_counter()

elapsed = "%.12f" % (end - start)

fout = open("output.txt", "wt")
fout.write("Elapsed Time: " + elapsed + " sec\n")
fout.write("Solution's Deviation Score: " + str(bestDist) + "\n")

for i in range(len(bestVanes)):
    fout.write(str(bestVanes[i].order) + "," + str(bestVanes[i].A) + "," + str(bestVanes[i].B) + "\n")
    
fout.close()

print("Results outputted to \"output.txt\"")