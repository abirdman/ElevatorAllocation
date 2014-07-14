# Python implemenation of Elevator Allocation Algorithm
# Written by Austin G. Walters for austingwalters.com
# July 2014 - Python 2.7

peoplePerFloor = 100.0
timePerFloor = 5
timePerWait = 20

# 3600 seconds per hours
rushHour = 3600.0

floorCount = 12
elevatorCount = 5

# Sets up the building, filling all the floors with people
def fillBuilding(floorCount):
    building = []
    for i in range(floorCount - 1):
        building.append(peoplePerFloor)
    return building


def eleLoop(e, i):
    floorsServiced = e[i] - e[i-1] + 1
    curr = timePerFloor * e[i] * 2
    curr += timePerWait * floorsServiced
    avgCarry = curr * peoplePerFloor / rushHour * floorsServiced
    if curr < 0:
        curr = 0
    return curr, avgCarry

# (Index * 5 seconds) + (20 seconds * (Index - PrevIndex))
# If previous elevators loops/stops add up to be greater than,
# (timePerFloor * 2) + timePerWait, then increase floor of previous
# elevators loop. i.e. elevator[2]+=1   
def addFloor(e):
    choiceIndex = 0
    best = 9999
    for i in range(1, len(e)):
        curr, avgCarry = eleLoop(e, i)
        if curr * avgCarry < best:
            choiceIndex = i
            best = curr * avgCarry
    for i in range(choiceIndex, len(e)):
        e[i] += 1
    return e


def printeleLoop(e):
    print ''
    print e
    print ''
    for i in range(1, len(e)):
        floorsServiced = e[i] - e[i-1] + 1
        curr = timePerFloor * e[i] * 2
        curr += timePerWait * floorsServiced
        avgCarry = curr * peoplePerFloor / rushHour * floorsServiced
        str = 'Elevator #%d, time for loop %d seconds' % (i, curr)
        str += 'carrying an average of '
        str += '%3.2f people per carry' % avgCarry
        print str
    print ''
    

def elevatorAllocation(building, elevatorCount):

    # Allocate elevators
    # Elevator[] represents the starting
    # group of stops. 
    #
    # i.e. 
    # If elevator[0]= 3 and elevator[1] = 5,
    # elevator[0] visits floors 3 and 4.
    # If elevator[1] = 7 instead,
    # elevator[0] visits 3, 4, 5, and 6
    elevator = []
    for i in range(elevatorCount + 1):
        elevator.append(0)
    for i in range(1, floorCount):
        elevator = addFloor(elevator)
    printeleLoop(elevator)
    return elevator

def simulate(e, building):

    eCircuit = []
    for i in range(len(e)):
        curr, avgCarry = eleLoop(e, i)
        eCircuit.append(float(curr))

    emptyFloors = 0
    totalTime = 0.0

    while emptyFloors is not len(building):
        for i in range(1, len(e)):
            for j in range(e[i-1], e[i]):
                if 0.0 > building[j]: 
                    building[j] = 0.0
                    emptyFloors += 1
                elif building[j] > 0.0:
                    persons = eCircuit[i] * peoplePerFloor / rushHour
                    building[j] = building[j] - persons
        printApprox(building)
    print ''

def printApprox(building):
    str = '[ '
    for i in range(len(building)):
        if building[i] < 0:
            str += '%06.2f ' % (0.00)
        else:
            str += '%06.2f ' % building[i]
    str += ']'
    print str

building = fillBuilding(floorCount)
elevator = elevatorAllocation(building, elevatorCount)
simulate(elevator, building)
