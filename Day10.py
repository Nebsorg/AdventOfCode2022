import copy
from datetime import datetime
from collections import deque

#### Main
print("2022 --- Day 10: Cathode-Ray Tube ---")
start_time = datetime.now()



def firstStar(instructions):
    currentInstruction = None
    register = 1
    signalStrenght = 0
    mesures = [20,60,100,140,180,220]
    currentInstructionModification = 0

    for i in range(1,221):
        #print(f"Cyle {i} - Beginning - Register = {register} - modificator = {currentInstructionModification}")

        if i in mesures:
            #print(f"   *** Signal Mesurement on Cyle {i} - Register = {register} - signal Streght = {i*register}")
            signalStrenght += i*register

        ## GET Instruction if no instruction ongoing
        if currentInstruction == None:
            currentInstruction = instructions.popleft()
            
            if currentInstruction[0] == 'addx':
                updateRegisterCycle = i+1
                currentInstructionModification = currentInstruction[1]
            else:
                updateRegisterCycle = i
                currentInstructionModification = 0
            #print(f"Cyle {i} - Loading Instruction {currentInstruction[0]} - modificator = {currentInstructionModification} - applying Cycle = {updateRegisterCycle}")

        ## Execute instruction before finishing Cycle
        if updateRegisterCycle == i:
            #print(f"Cyle {i} - End of Cycle - Applying instruction - modificator = {currentInstructionModification}")
            register += currentInstructionModification
            currentInstruction = None
    print(f"  ** First Star : {signalStrenght}")


def secondStar(instructions):
    screen = [[' ' for x in range(40)] for y in range(6)] 

    currentInstruction = None
    register = 1
    currentInstructionModification = 0

    for i in range(1,241):
        #print(f"Cyle {i} - Beginning - Register = {register} - modificator = {currentInstructionModification}")

        ## GET Instruction if no instruction ongoing
        if currentInstruction == None:
            currentInstruction = instructions.popleft()
            
            if currentInstruction[0] == 'addx':
                updateRegisterCycle = i+1
                currentInstructionModification = currentInstruction[1]
            else:
                updateRegisterCycle = i
                currentInstructionModification = 0
            #print(f"Cyle {i} - Loading Instruction {currentInstruction[0]} - modificator = {currentInstructionModification} - applying Cycle = {updateRegisterCycle}")
        
        ##Draw CRT
        column = (i-1)%40
        row = int((i-1)/40)
        if register-1 <= column <= register+1:
            toDraw = '#'
        else:
            toDraw = '.'

        #print(f"Cyle {i} - Draw {toDraw} on CRT on corrd {(row, column)}")
        screen[row][column] = toDraw

        ## Execute instruction before finishing Cycle
        if updateRegisterCycle == i:
            register += currentInstructionModification
            #print(f"Cyle {i} - End of Cycle - Applying instruction - modificator = {currentInstructionModification} - New Register Value = {register}")
            currentInstruction = None

    for line in screen:
        print(''.join(line))


instructionsFirstStar = deque()
instructionsSecondStar = deque()
currentRow = 0
f = open(".\Day10.txt", "r")
for line in f:
    line = line.rstrip()
    instruction = line.split(' ')
    if instruction[0] == 'addx':
        instruction[1] = int(instruction[1])
    instructionsFirstStar.append(instruction)
    instructionsSecondStar.append(instruction)

firstStar(instructionsFirstStar)
secondStar(instructionsSecondStar)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))