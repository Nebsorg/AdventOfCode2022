import copy
from datetime import datetime
from re import finditer
import re


#### Main
print("2022 --- Day 6: Tuning Trouble ---")
start_time = datetime.now()

def firstStar(line):
    markerFound = False
    i = 0
    while not markerFound:
        testedPart = line[i:i+4]
        if len(testedPart) == len(set(testedPart)):
            ## all unique !
            markerFound = True
            star = i+4
        i += 1
    print(f"  ** First Star : {star}")

def secondStar(line):
    markerFound = False
    i = 0
    while not markerFound:
        testedPart = line[i:i+14]
        if len(testedPart) == len(set(testedPart)):
            ## all unique !
            markerFound = True
            star = i+14
        i += 1
    print(f"  ** Second Star : {star}")


f = open(".\Day6.txt", "r")
for line in f:
    line = line.rstrip()
    firstStar(line)
    secondStar(line)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))