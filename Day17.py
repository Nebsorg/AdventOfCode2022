from datetime import datetime
import math
import copy


def displayPlayZone(playZone):
    nbRow = len(playZone)
    nbCol = len(playZone[0])
    renderRow = nbRow + 10

    for row in range(renderRow-1, -1, -1):
        if row in playZone.keys():
            line = f'{row:5d}|' + ''.join(playZone[row]) + '|'
        else:
            line = f'{row:5d}|       |'
        print(line)
    print()


def convertRockToCoordinate(rock, spawnCoordinate):
    result = {}
    nbRow = len(rock)
    nbCol = len(rock[0])

    for row in range(nbRow):
        for col in range(nbCol):
            result[(spawnCoordinate[0]+row, spawnCoordinate[1]+col)] = rock[nbRow - row - 1][col]
    return(result)

def collision(rockCoord, playZone):
    for coord in rockCoord.keys():
        if coord[1] > 6 or coord[1] < 0: 
            ## out of the zone
            return(True)

        if rockCoord[coord] == '#':
            if coord[0] in playZone.keys(): 
                if playZone[coord[0]][coord[1]] == '#':
                    return(True)
    return(False)

## moving horizontally -> updating col
def moveHorizontally(rockCoord, playZone, direction):
    newRockCoord = {}
    
    for coord, type in rockCoord.items():
        newRockCoord[(coord[0], coord[1]+direction)] = type

    if collision(newRockCoord, playZone):
        return(False, rockCoord)
    return(True, newRockCoord)

## moving Down -> updating row
def moveDown(rockCoord, playZone):
    newRockCoord = {}
    
    for coord, type in rockCoord.items():
        newRockCoord[(coord[0]-1, coord[1])] = type

    if collision(newRockCoord, playZone):
        return(False, rockCoord)
    return(True, newRockCoord)

def updatePlayZone(playZone, rockCoord):
    for coord, type in rockCoord.items():
        if type == '.':
            continue

        if coord[0] not in playZone.keys():
            playZone[coord[0]] = list('       ')
            ## ligne déjà existante, on met à jour les coordonées du rocher dans la ligne

        playZone[coord[0]][coord[1]] = type


def getColumnMaxHeight(playZone):
    result = []
    maxRow = list(playZone.keys())[-1]

    for col in range(7):
        row = maxRow
        found = False
        while not found:
            if playZone[row][col] == '#':
                found = True
                result.append(row)
                if col == 0:
                    minRowFound = row
                else: 
                    if row <= minRowFound:
                        minRowFound = row
            row -= 1
    
    result = map(lambda x: x-minRowFound, result)
    return(tuple(result))



def playGame(jet, rocks, nbRocks):
    ## playzone is a dict, key is the row, element is the values
    memory = {}
    playZone = {}
    playZone[0] = list("#######")


    currentMaxRow = 0
    currentJetPosition = 0
    maxJet = len(jet)
    
    cycleFound = False
    rock_number = 1
    while rock_number <= nbRocks:
        ## spawning new rocks : 
        rock = rocks[(rock_number-1)%5]
        jetId = currentJetPosition%maxJet

        spawnCoordinates = [currentMaxRow+4, 2]
        rockCoord = convertRockToCoordinate(rock, spawnCoordinates)
        #print(f" --=== Round {rockID+1} : Spawning Rock {rockID%5+1} at coordinate {spawnCoordinates} - MAxCol = {maxcolHeight}")
        

        canMove = True
        while canMove:
            ## pushing rock : 
            jetId = currentJetPosition%maxJet
            direction = jet[jetId]
            currentJetPosition+=1
            ## moving left or right -> updating col
            _, rockCoord = moveHorizontally(rockCoord, playZone, direction)
            
            ## moving down
            canMove, rockCoord = moveDown(rockCoord, playZone)
        
        updatePlayZone(playZone, rockCoord)
        currentMaxRow = max(list(playZone.keys()))


        ##### Creating a dict memory to detect paterns
        # Keys : tuple
        #    0 : relative high of different columns,
        #    1 : current rock in rock cycle,
        #    2 : current jet in jet cycle
        # Values: tuple
        #   0 : row reached for this pattern
        #   1 : nomber of rock fall
        maxcolHeight = getColumnMaxHeight(playZone)
        mem = (maxcolHeight, (rock_number-1)%5, jetId)
        if not cycleFound:
            if mem in memory.keys(): 
                cycleFound = True
                #### Cycle detected
                ## max row will be : (row reached at beginning of the cycle) + (number of time the cylce will repeat) * (nb row added by the cycle) + (row reach by the rest to reach the target)
                firstInsertion = memory[mem][1]
                firstInsertionMaxRow = memory[mem][0]
                cycleSize = rock_number-firstInsertion
                cycleIncreaseSize = currentMaxRow-firstInsertionMaxRow
                print(f" --=== LOOP found on Round {rock_number} : firstInsertion={firstInsertion} -- MAx row reached at first insertion : {firstInsertionMaxRow} - current max row={currentMaxRow} - cycle size = {cycleSize} - cycle increase high={cycleIncreaseSize}")
                nbOfCycleToExecute = int(math.floor((nbRocks-firstInsertion)/cycleSize))
                rock_number = firstInsertion + cycleSize * nbOfCycleToExecute + 1
                remainingRound = (nbRocks-firstInsertion)%cycleSize
                remainingRound = nbRocks - rock_number
                print(f"    --> nbOfCycleToExecute={nbOfCycleToExecute} - remainingRound={remainingRound}")

                ### setting the world as it will be after cycle execution : 
                
                currentMaxRow = firstInsertionMaxRow + nbOfCycleToExecute * cycleIncreaseSize
                print(f"    --> new rock number : {rock_number} - newMaxRow={currentMaxRow}")
                ## adding the last 5 line
                last10Rows = list(playZone.keys())
                last10Rows.sort()
                last10Rows = last10Rows[-6:]
                for i in range(6):
                    playZone[currentMaxRow-(5-i)] = playZone[last10Rows[i]]
                
            else:
                memory[mem] = (currentMaxRow, rock_number)
                rock_number += 1
        else:
            ## finalising last rock, no need to memorise the previous one : the cycle has already been managed
            rock_number += 1    

        #print(f" --=== Round {rockID+1} : END {rockID%5+1} at coordinate {spawnCoordinates} - MAxCol = {maxcolHeight}")

        

    return(currentMaxRow)

#### Main
print("2022 --- Day 17: Pyroclastic Flow ---")
start_time = datetime.now()


network = {}
f = open(".\Day17.txt", "r")
for line in f:
    line = line.rstrip()
    gaz = [1 if x=='>' else -1 for x in list(line)]

rocks={}
rocks[0] = [list("####")]
rocks[1] = [list(".#."), list("###"), list(".#.")]
rocks[2] = [list("..#"), list("..#"), list("###")]
rocks[3] = [list("#"), list("#"), list("#"), list("#")]
rocks[4] = [list("##"), list("##")]


star = playGame(gaz, rocks, 2022)
print(f"****** First Star = {star}")                
star = playGame(gaz, rocks, 1000000000000)
print(f"****** Second Star = {star}")                

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 