from datetime import datetime
from collections import deque
import math
import copy
import re


#### Main
print("2022 --- Day 15: Beacon Exclusion Zone ---")
start_time = datetime.now()

regExp = "Sensor at x=(?P<s_col>-?\d*), y=(?P<s_row>-?\d*): closest beacon is at x=(?P<b_col>-?\d*), y=(?P<b_row>-?\d*)"

def getCoordinateWithinDistance_Range(pos, distance):
    result = {}
    for delta_row in range(distance, -1, -1):
        delta_col = distance - delta_row
        result[pos[0]+delta_row] = [pos[1]-delta_col, pos[1]+delta_col]
        result[pos[0]-delta_row] = [pos[1]-delta_col, pos[1]+delta_col]
    return(result)

def doesOverlap(a, b):
    return(min(a[1], b[1]) >= max(a[0], b[0]))

def positionCoveredByIntervals(intervals):
    result = 0
    for interval in intervals:
        result += interval[1] - interval[0] + 1
    return(result)

def firstHoleInIntervals(intervals):
    result = -1
    position = 0
    for interval in intervals:
        if position < interval[0]:
            ## trou trouvé
            return(position)
        if position <= interval[1]:
            position = interval[1]+1
            continue
    else:
        return(position)



def insertInterval(newInterval, existingInterval):
    ## nouvel interval a inseré avant ou apres
    if (newInterval[1] < existingInterval[0][0]) or (newInterval[0] > existingInterval[-1][1]):
        if newInterval[1] < existingInterval[0][0]:
            #print(f"new Interval {newInterval} inserted at first position")
            existingInterval.insert(0, newInterval)

        if newInterval[0] > existingInterval[-1][1]:
            #print(f"new Interval {newInterval} inserted at last position")
            existingInterval.append(newInterval)
        return(existingInterval)

    ## le nouvel interval couvre tout les existants
    if (newInterval[0] <= existingInterval[0][0]) and (newInterval[1] >= existingInterval[-1][1]):
        #print(f"new Interval {newInterval} overlap the current intervals --> replaced by new interval")
        existingInterval = [newInterval]
        return(existingInterval)

    ## on regarde si on peut l'inserer quelque part entre deux intervalles, ou s'il chevauche des intervals
    returnedIntervals = []
    nbInterval = len(existingInterval)
    for i in range(nbInterval):
        currentInterval = existingInterval[i]
        overlap = doesOverlap(newInterval, currentInterval)
        if not overlap:
            returnedIntervals.append(currentInterval)
            ## Est-ce qu'il peut rentrer entre cet interval et le suivant ? 
            if i < nbInterval - 1:
                nextInterval = existingInterval[i+1]
                if newInterval[0] > currentInterval[1] and newInterval[1] < nextInterval[0]:
                    ## il rentre !
                    #print(f"new Interval {newInterval} entered between interval {i}={currentInterval} and {i+1}={nextInterval}")
                    existingInterval.insert(i+1, newInterval)
                    return(existingInterval)
                ## il ne rentre pas, on regarde le suivant
            continue

        ## il chauvauche cet interval
        ## le nouveau interval à crée a pour borne inferieur le min des deux bornes inferieurs
        tempInterval = [min(newInterval[0], currentInterval[0]),0]

        ## on cherche la fin du chevauchement:
        j = i
        while (j < nbInterval and overlap):
            ## la borne surperieur du nouveau interval est le maximums des deux intervalles qui se chevauchent
            tempInterval[1] = max(newInterval[1], existingInterval[j][1])
            if (j == nbInterval - 1):
                overlap = False
            else:
                overlap = doesOverlap(existingInterval[j+1], newInterval)
            j += 1
        
        ## setting j on the interval which do not overlap
        if j == nbInterval:
            ## il chauvauche tous les intervalles jusqu'au dernier !
            #print(f"new Interval {newInterval} is overlapping all interval from {i}={currentInterval} to the end. Keeping beginning of list and {tempInterval}")
            returnedIntervals = existingInterval[:i]
            returnedIntervals.append(tempInterval)
            return(returnedIntervals)
        else:
            ## j est l'intervalle qu'il ne chauvauche plus
            #print(f"new Interval {newInterval} was overlapping interval from {i}={currentInterval} to {j}={existingInterval[j]}. Replaced by {tempInterval}")
            returnedIntervals.append(tempInterval)
            returnedIntervals.extend(existingInterval[j:])
            return(returnedIntervals)


def stars(sensors, beacons, specialLine, maxZone):
    no_beacon_range = {}
    print(f"Looping on sensor --> size = {len(sensors)}")
    it = 1
    it_max = len(sensors)
    for sensor_coord, distance in sensors.items():
        result = getCoordinateWithinDistance_Range(sensor_coord, distance)
        print(f"  -= Sensor {it}/{it_max} - updating interval of rows impacted by the sensor. number of row --> {len(result)}")
        for row, new_range in result.items():
            if row in no_beacon_range.keys():
                no_beacon_range[row] = insertInterval(new_range, no_beacon_range[row])
            else:
                no_beacon_range[row] = [new_range]
        it+=1

    ### First Star : checking line special : counting disabled position minus beacon on the row
    beacons_on_special_row = [x for x in beacons if x[0] == specialLine]
    star = positionCoveredByIntervals(no_beacon_range[specialLine]) - len(beacons_on_special_row)
    
    end_time = datetime.now()
    print(f"****** First Star = {star} -- Duration = {end_time-start_time}")

    ## Second Star : sarching for beacon : we need to find a hole in the range within the zone
    print(f"Searching for second star : Number of row to seach --> {len(no_beacon_range)}")
    for row in no_beacon_range.keys():
        if 0 <= row <= maxZone: 
            ## on regarde si le beacon peut etre sur cette ligne, on cherche un trou dans le range 0..maxZone
            hole = firstHoleInIntervals(no_beacon_range[row])
            if hole <= maxZone:
                print(f"  -= Hole found on coordinate {(row, hole)}")
                print(f"****** Second Star = {4000000 * hole + row}")                


sensors = {}
beacons = set()
f = open(".\Day15.txt", "r")
for line in f:
    line = line.rstrip()
    match = re.match(regExp, line)
    if match:
        sensor_coordinate = (int(match.group('s_row')), int(match.group('s_col')))
        beacon_coordinante = (int(match.group('b_row')), int(match.group('b_col')))
        beacons.add(beacon_coordinante)
        distance = abs(sensor_coordinate[0] - beacon_coordinante[0]) + abs(sensor_coordinate[1] - beacon_coordinante[1])
        sensors[sensor_coordinate] = distance


stars(sensors, beacons, 2000000, 4000000)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))