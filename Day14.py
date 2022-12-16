from datetime import datetime
from collections import deque
import math
import copy
import re

#### Main
print("2022 --- Day 14: Regolith Reservoir ---")
start_time = datetime.now()

regExp = "(?P<w_col>-?\d*),(?P<w_row>-?\d*)"

def displayCave(start, boudaries, walls):
    elements = walls.keys()
    for row in range(boudaries[0]+5):
        line = ""
        for col in range(boudaries[1]-5, boudaries[2]+5):
            if (row,col) in elements:
                line += walls[(row,col)]
                continue
            if (row,col) == start:
                line += '+'
                continue
            line += ' '
        print(line)


def addSand(start, boundaries, walls):
    sandPos = start
    if start in walls:
        return(start)

    positionned = False
    while not positionned:
        positionned = True
        nextPos = (sandPos[0]+1, sandPos[1])
        if nextPos in walls:
            ## blocked, try to keep falling on left
            nextPos = (sandPos[0]+1, sandPos[1]-1)
            if nextPos in walls:
                ## blocked, try to keep falling on right
                nextPos = (sandPos[0]+1, sandPos[1]+1)
                if nextPos in walls:
                    ## blocked --> staying on initial attemp
                    return((sandPos[0], sandPos[1]))
                else:
                    ## empty space, keep falling
                    sandPos = nextPos
                    positionned = False     
            else:
                ## empty space, keep falling
                sandPos = nextPos
                positionned = False     
        else:
            ## empty space, keep falling
            sandPos = nextPos
            positionned = False
        
        if nextPos[0] > boundaries[0]:
            ## falling outside the last wall
            return(tuple(nextPos))


def firstStar(start, boundaries, walls):
    finished = False
    unitAdded = 0
    while not finished:
        ## Adding Sans (which behave like wall once added)
        sandPos = addSand(start, boundaries, walls)
        if sandPos[0] >= boundaries[0] or sandPos == start:
            ## falling outside the last wall
            finished = True
        else:
            unitAdded += 1
            walls[sandPos] = 'o'
            #print(f"unit {unitAdded} added to position {sandPos}")
        #displayCave((0,500), boundaries, walls)
    #displayCave((0,500), boundaries, walls)
    print(f"** First Star = {unitAdded}")

def secondStar(start, boundaries, walls):
    finished = False
    unitAdded = 0
    while not finished:
        ## Adding Sans (which behave like wall once added)
        sandPos = addSand(start, boundaries, walls)

        if sandPos == start:
            ## entry point is recovered - stopping
            finished = True
        else:
            if sandPos[0] >= boundaries[0]:
                ## falling outside the last wall --> extending the cave horizontally
                ## determining if extention to right or to left
                if sandPos[1] >= boundaries[2]:
                    ## extendingRight
                    sandPos = (sandPos[0]-1, sandPos[1]-1)
                    boundaries[2] += 10
                    for i in range(boundaries[1], boundaries[2]):
                        walls[(boundaries[0],i)] = '#'
                else:
                    ## extendingLeft
                    sandPos = (sandPos[0]-1, sandPos[1]+1)
                    boundaries[1] -= 10
                    for i in range(boundaries[1], boundaries[2]):
                        walls[(boundaries[0],i)] = '#'
            unitAdded += 1
            walls[sandPos] = 'o'
            #print(f"unit {unitAdded} added to position {sandPos}")
    #displayCave((0,500), boundaries, walls)
    print(f"** Second Star = {unitAdded+1}")


f = open(".\Day14.txt", "r")
walls = []
lowest_row = 0
lowest_col = 1000
highest_col = 0
for line in f:
    line = line.rstrip()
    matches = re.finditer(regExp, line)

    wall = []
    for match in matches:
        w_row = int(match.group('w_row'))
        w_col = int(match.group('w_col'))
        wall.append([w_row, w_col])
        if w_row > lowest_row:
            lowest_row = w_row
        if w_col < lowest_col:
            lowest_col = w_col
        if w_col > highest_col:
            highest_col = w_col

    #print(f"line={line} --> wall={wall}")
    walls.append(wall)

#print(f"{len(walls)} walls read - lowestRow={lowest_row} - lowestCol={lowest_col} - highestCol={highest_col}")
boundaries=[lowest_row, lowest_col, highest_col]

## creating the full list of wall : 
completeWall = {}
for wall in walls:
    for i in range(len(wall)-1):
        currentPos = wall[i]
        nextPos = wall[i+1]
        if currentPos[0] == nextPos[0]:
            ## horizontal wall
            minCol = min(currentPos[1], nextPos[1])
            maxCol = max(currentPos[1], nextPos[1])
            for j in range(minCol, maxCol+1):
                completeWall[(currentPos[0], j)] = '#'
        else:
            ## vertical wall
            minRow = min(currentPos[0], nextPos[0])
            maxRow = max(currentPos[0], nextPos[0])
            for j in range(minRow, maxRow+1):
                completeWall[(j, currentPos[1])] = '#'


#displayCave((0,500), boundaries, completeWall)
completeWallStar2 = copy.deepcopy(completeWall)

firstStar((0,500), boundaries, completeWall)

## adding floor to list of wall
boundaries[0] += 2
boundaries[1] -= 500
boundaries[2] += 500
for i in range(boundaries[1], boundaries[2]):
    completeWallStar2[(boundaries[0],i)] = '#'

#displayCave((0,500), boundaries, completeWallStar2)
secondStar((0,500), boundaries, completeWallStar2)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))