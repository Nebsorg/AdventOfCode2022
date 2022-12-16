from datetime import datetime
from collections import deque
import math
import copy

WRONG = -1
RIGHT = 1
KEEP_GOING = 0
#### Main
print("2022 --- Day 13: Distress Signal ---")
start_time = datetime.now()

def isRightOrder(left, right, indentation):
    #print(f"{' '*indentation} - Comparing {left} and {right}")
    if type(left) == list:
        if type(right) == list:
            ## both are list, cycling:
            for i in range(len(left)):
                leftValue = left[i]
                if i < len(right):
                    rightValue = right[i]
                    result = isRightOrder(leftValue, rightValue, indentation+2)
                    if result == WRONG or result == RIGHT:
                        return(result)
                else:
                    ## no more element on right --> Wrong Order
                    #print(f"{' '*indentation} - Right side ran out of items, so inputs are NOT in the right order")
                    return(WRONG)
            else:
                ## is there still element on right side ? 
                if len(right) > len(left):
                    #print(f"{' '*indentation} - Left side ran out of items, so inputs are in the right order")
                    return(RIGHT)
                else:
                    return(KEEP_GOING)
        else:
            #print(f"{' '*indentation} - mixed type; convert right to {[right]} and retry comparison")
            result = isRightOrder(left, [right], indentation+2)
            if result == WRONG or result == RIGHT:
                return(result)
    else:
        if type(right) == list:
            #print(f"{' '*indentation} - mixed type; convert left to {[left]} and retry comparison")
            result = isRightOrder([left], right, indentation+2)
            if result == WRONG or result == RIGHT:
                return(result)
        else:
            ## both term are numbers
            if left < right:
                #print(f"{' '*indentation} - left side is smaller, so input are in RIGHT order")
                return(RIGHT)
            elif left > right:
                #print(f"{' '*indentation} - right side is smaller, so input are NOT in RIGHT order")
                return(WRONG)
            else:
                ## both term are equal -> continue to check
                return(KEEP_GOING)
    return(RIGHT)


def firstStar(pairs):
    rightOrderedPair = []
    for id, values in enumerate(pairs):
        left = values[0]
        right = values[1]
        #print(f"== Treating Pair {id} == left={left} - right={right}")
        result = isRightOrder(left, right, 0)
        if result == RIGHT:
            rightOrderedPair.append(id+1)

    print(f"** First Star = {sum(rightOrderedPair)}")

def secondStar(pairs):
    ## no pairs any more, putting all the line in a single list
    globalList = []
    for pair in pairs: 
        globalList.append(pair[0])
        globalList.append(pair[1])

    ## Adding the two keys
    globalList.append([[2]])
    globalList.append([[6]])

    ## try to rearrange all the pair until all are RIGHT two by two
    classee = False
    iteration = 1

    while not classee:
        classee = True
        #print(f"== Iteration {iteration}")
        for i in range(len(globalList)-1):
            for j in range (i+1, len(globalList)):
                signal1 = globalList[i]
                signal2 = globalList[j]

                if isRightOrder(signal1, signal2,0) != RIGHT:
                    #print(f"   - signals {i} and {i+1} are not RIGHT, switching them")
                    classee = False
                    globalList[i], globalList[j] = globalList[j], globalList[i]
        iteration += 1
    #print(f" Iteration {iteration} : all signals are in the right order !")

    firstKey = globalList.index([[2]])+1
    secondKey = globalList.index([[6]])+1

    print(f"** Second Star = {firstKey*secondKey}")


pairs = []
pairId = 1
f = open(".\Day13.txt", "r")
pair = []
for i, line in enumerate(f):
    line = line.rstrip()
    if i%3 != 2: 
        pair.append(eval(line))
    else: 
        pairs.append(pair)
        pair = []
        pairId += 1


firstStar(pairs)
secondStar(pairs)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))