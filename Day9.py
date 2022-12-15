import copy
from datetime import datetime

#### Main
print("2022 --- Day 9: Rope Bridge ---")
start_time = datetime.now()


def moveRope(instructions, ropeLenght):
    tailPositionList = set()

    rope = {}
    for i in range(ropeLenght):
        rope[i] = [0,0]

    tailPositionList.add(tuple(rope[ropeLenght-1]))

    for instruction in instructions:
        ##moving the rope piece by piece, starting with head
        #print(f"##### INSTRUCTION = {instruction} - rope = {rope}")
        for step in range(instruction[2]):
            vector = instruction[1]
            rope[0][0] += vector[0]
            rope[0][1] += vector[1]
            #print(f"step {step} - new headPosition = {rope[0]}")

            ## moving all piece of the rope until the tail
            for i in range(1,ropeLenght):
                headPosition = rope[i-1]
                tailPosition = rope[i]
                ## is tail still touching head ? :
                distance = pow(headPosition[0] - tailPosition[0], 2) + pow(headPosition[1] - tailPosition[1], 2)
                if distance > 2:
                    #print(f"RopePiece#{i} : distance between head {headPosition} and tail {tailPosition} to big: {distance} - moving tail to close the gap")
                    ## compute moving vector
                    vector = [headPosition[0] - tailPosition[0], headPosition[1] - tailPosition[1]]
                    if abs(vector[0]) == 2:
                        vector[0] = int(vector[0]/2)
                    if abs(vector[1]) == 2:
                        vector[1] = int(vector[1]/2)

                    tailPosition[0] += vector[0]
                    tailPosition[1] += vector[1]
                    #print(f"RopePiece#{i} : new tail position : {tailPosition}")
            tailPositionList.add(tuple(rope[ropeLenght-1]))

    return(len(tailPositionList))

instructions = []
currentRow = 0
f = open(".\Day9.txt", "r")
for line in f:
    line = line.rstrip()
    instruction = line.split(' ')
    match instruction[0]:
        case 'R':
            vector = (0, 1)
        case 'L':
            vector = (0,-1)
        case 'U':
            vector = (-1,0)
        case _:
            vector = (1,0)
    instructions.append((instruction[0], vector, int(instruction[1])))

print(f"  ** First Star : {moveRope(instructions,2)}")
print(f"  ** Second Star : {moveRope(instructions,10)}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))