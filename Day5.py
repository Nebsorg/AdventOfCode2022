import copy
from datetime import datetime
from re import finditer
import re
from collections import defaultdict

#### Main
print("2022 --- Day 5: Supply Stacks ---")
start_time = datetime.now()

regExpStacks = "([\w])"
regExpMove = "move (?P<nb>\d*) from (?P<col_source>\d*) to (?P<col_dest>\d*)"

def firstStar(stacks, instructions):
    for instruction in instructions:
        nbCrate = instruction[0]
        col_source = instruction[1]
        col_dest = instruction[2]

        stack_source = stacks[col_source]
        ## get last nbCrate element
        movedCrates = stack_source[-nbCrate:]
        movedCrates.reverse()
        stacks[col_dest] += movedCrates
        del stack_source[-nbCrate:]

    # get last element of each stack :
    max_column_id = max(stacks.keys())

    star = ""
    for i in range(1, max_column_id + 1):
        star += stacks[i][-1]
    print(f"  ** First Star : {star}")

def secondStar(stacks, instructions):
    for instruction in instructions:
        nbCrate = instruction[0]
        col_source = instruction[1]
        col_dest = instruction[2]

        stack_source = stacks[col_source]
        ## get last nbCrate element
        movedCrates = stack_source[-nbCrate:]
        stacks[col_dest] += movedCrates
        del stack_source[-nbCrate:]

    # get last element of each stack :
    max_column_id = max(stacks.keys())

    star = ""
    for i in range(1, max_column_id + 1):
        star += stacks[i][-1]
    print(f"  ** Second Star : {star}")



stacksFinised = False
stacks = defaultdict(lambda:[])
instructions = []
f = open(".\Day5.txt", "r")
for line in f:
    line = line.rstrip()
    if not stacksFinised:
        if line[1] == '1':
            stacksFinised = True
        else:
            ## read stack data
            for match in finditer(regExpStacks, line):
                column = int((match.span()[1]+2)/4)
                crate = match.group()
                stacks[column][:0] = [crate]
    else:
        ## reading instruction
        match = re.match(regExpMove, line)
        if match:
            instruction = (int(match.group('nb')), int(match.group('col_source')), int(match.group('col_dest')))
            instructions.append(instruction)

print(f"Initial stacks = {stacks}")
print(f"instruction = {instructions}")

firstStarStacks = copy.deepcopy(stacks)
secondStarStacks = copy.deepcopy(stacks)

firstStar(firstStarStacks, instructions)
secondStar(secondStarStacks, instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))