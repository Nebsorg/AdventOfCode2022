from datetime import datetime
from collections import deque
import math
import copy
import re
import itertools


#### Main
print("2022 --- Day 16: Proboscidea Volcanium ---")
start_time = datetime.now()

regExp = "Valve (?P<valve>\w{2}) has flow rate=(?P<rate>\d*); tunnel(s?) lead(s?) to valve(s?) (?P<valves>.*)"

def floydMarchal(network):
    # Number of vertices
    INF = 100000
    nodeList = network.keys()

    ## matrix initialisation
    FMMatrix = {}
    for nodeSource in nodeList:
        for nodeDest in nodeList:
            if nodeSource == nodeDest:
                FMMatrix[(nodeSource, nodeDest)] = 0
                continue
            
            if nodeDest in network[nodeSource][1]:
                FMMatrix[(nodeSource, nodeDest)] = 1
            else: 
                FMMatrix[(nodeSource, nodeDest)] = INF

    ## Adding vertices individually
    for r in nodeList:
        for p in nodeList:
            for q in nodeList:
                FMMatrix[(p,q)] = min(FMMatrix[(p,q)], FMMatrix[(p,r)] + FMMatrix[(r,q)])
    return(FMMatrix)

def exploreNetwork(currentValve, network, timeRemaining, currentScore, closedValves, FMMatrix, followedPath):
    #print(f"currentValve={currentValve} - Time Remaining : {timeRemaining} -  currentScore = {currentScore} - closedValve = {closedValves} - followedPath={followedPath}")

    newFollowedPath = followedPath.copy()
    newFollowedPath.append(currentValve)

    if timeRemaining < 0: 
        #print(f"   ** currentValve={currentValve} - Time Remaining : {timeRemaining} - no more time")
        return(currentScore, newFollowedPath)

    if len(closedValves) == 0:
        #print(f"   ** currentValve={currentValve} - Time Remaining : {timeRemaining} - no more valves closes")
        return(currentScore, newFollowedPath)

    maxScore = currentScore
    maxPath = []
    for dest in closedValves:
        ## remaining time is currenttime - time to go there - 1 min to openit
        newTime = timeRemaining - FMMatrix[(currentValve, dest)] - 1
        if newTime <= 0: 
            ## no time to go there and open the valve
            #print(f"   ** currentValve={currentValve} - no time to go {dest} Time Remaining : {timeRemaining} // new time remaining {newTime}")
            continue

        ## score to go there : currentscore + remaining time there * releasing gaz value
        newScore = currentScore + (newTime * network[dest][0])
        
        newClosedValves = [x for x in closedValves if x != dest]
        #print(f"   ** currentValve={currentValve} - moving to {dest} - New Time Remaining : {newTime} - new Closed={newClosedValves} - newScore{newScore} - FollwedPath={newFollowedPath}")
        score, scorePath = exploreNetwork(dest, network, newTime, newScore, newClosedValves, FMMatrix, newFollowedPath)
        if score >= maxScore:
            maxScore = score
            maxPath = scorePath.copy()
 
    return(maxScore, maxPath)


def secondStar(network, FMMatrix):
    print(f"  Starting second Star")    
    closedValves = [x for x in network.keys() if network[x][0]>0]

    globalLists = two_partitions(set(closedValves))
    #print(globalLists)
    size = len(globalLists)
    maxScore = 0
    for i, repartition in enumerate(globalLists):
        elephValves = repartition[0]
        myValves = repartition[1]
        ElephPath = []
        myPath = []
        scoreEleph, ElephPath = exploreNetwork('AA', network, 26, 0, elephValves, FMMatrix, ElephPath)
        myScore, myPath = exploreNetwork('AA', network, 26, 0, myValves, FMMatrix, myPath)
        teamScore = scoreEleph + myScore
        print(f" ** Repartition {i+1}/{size} : I have closed {len(myValves)} - {myValves} - and elephant have closed {len(elephValves)} - {elephValves} ** MyScore={myScore} - ElefScore={scoreEleph} - teamScore = {teamScore}")
        if teamScore > maxScore:
            maxScore = teamScore
            maxMyPath = list(myPath)
            maxElephPath = list(ElephPath)
            print(f" -====== BEST SCORE ======- Repartition {i+1}/{size} : I have closed {len(myValves)} - {myValves} - and elephant have closed {len(elephValves)} - {elephValves} ** MyScore={myScore} - ElefScore={scoreEleph} - teamScore = {teamScore}")
        
    print(f"  **** Second Star = {maxScore} - myPath = {len(maxMyPath)} valves -> {maxMyPath} ***  ElephPath = {len(maxElephPath)} valves --> {maxElephPath}")

## crée toutes les combinaisons de deux listes a partir d'une liste
def two_partitions(listeSource):
    res_list = []
    for membre in range(0,int(len(listeSource)/2)+1):
        combinaisons = set(itertools.combinations(listeSource,membre))
        for combi in combinaisons:
            res_list.append((sorted(list(combi)), sorted(list(listeSource-set(combi)))))
    return res_list

network = {}
f = open(".\Day16.txt", "r")
for i, line in enumerate(f):
    line = line.rstrip()
    match = re.match(regExp, line)
    if match:
        valve = match.group('valve')
        rate = int(match.group('rate'))
        valves = match.group('valves').replace(' ', '').split(',')
        network[valve] = [rate, valves]
        print(f"line {i+1} : {line} --> valve={valve} - rate={rate} - valves={valves} == {network[valve]}")

closedValves = [x for x in network.keys() if network[x][0]>0]

print(f"Closed Valves : {len(closedValves)} - {closedValves}")

FMMatrix = floydMarchal(network)

#followedPath = []
#score, path = exploreNetwork('AA', network, 30, 0, closedValves, FMMatrix, followedPath)
#print(f"  **** First Star = {score} - Path = {path}")

secondStar(network, FMMatrix)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 