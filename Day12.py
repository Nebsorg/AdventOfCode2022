from datetime import datetime
from collections import deque
import math
import copy

#### Main
print("2022 --- Day 12: Hill Climbing Algorithm ---")
start_time = datetime.now()


def dijkstraFast(maze, start_node):

    node_bag = deque([start_node])
    costMap = {start_node: 0}
    size_row = len(maze)
    size_col = len(maze[0])

    while node_bag:
        ## taking a node
        current_node = node_bag.popleft()

        ## checking Neighbours
        for shift in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_node = (current_node[0] + shift[0], current_node[1] + shift[1])
            if new_node[0] >= size_row or new_node[0] < 0 or new_node[1] >= size_col or new_node[1] < 0:
                ## new node outside of boudaries
                continue

            new_node_value = maze[new_node[0]][new_node[1]]
            current_node_value = maze[current_node[0]][current_node[1]]

            if (new_node_value > current_node_value + 1):
                ## new node to high to being reached (but lower node can be reached)
                continue

            ## updating neighbour cost : each node cost 1 more to reach
            risk = costMap[current_node] + 1
            if new_node not in costMap or risk < costMap[new_node]:
                costMap[new_node] = risk
                node_bag.append(new_node)
    return costMap


f = open(".\Day12.txt", "r")
maze = []
startingPosition = {}
currentRow = 0
for line in f:
    line = line.rstrip()
    #print(line)
    ## searching for Start & Target
    index = line.find('S')
    if index != -1:
        startPos = (currentRow, index)
        line = line.replace('S','a')

    index = line.find('E')
    if index != -1:
        targetPos = (currentRow, index)
        line = line.replace('E','z')
    
    ## storing all starting position possible: 
    indexes = [x for x, v in enumerate(line) if v == 'a']
    for column in indexes:
        startingPosition[(currentRow, column)] = 0

    ## replacing letter by numbers
    l = [int(ord(v)-96) for v in line]
    maze.append(l)
    currentRow += 1

print(f"StartPosition = {startPos} - Target = {targetPos}")
cost_map = dijkstraFast(maze, startPos)
print(f"** First Star = {cost_map[(targetPos[0], targetPos[1])]}")

#print(f"All Start Position = {startingPosition} - Target = {targetPos}")
## for each starting position, determine the better start point: 
allCosts = []
for start in startingPosition.keys():
    cost_map = dijkstraFast(maze, start)
    if (targetPos[0], targetPos[1]) in cost_map.keys():
        cost = cost_map[(targetPos[0], targetPos[1])]
        startingPosition[start] = cost
        allCosts.append(cost)
        #print(f" ** Starting position : {start} - Shortest Path Cost = {cost}")
    #else: 
        #print(f" ** Starting position : {start} - No Path found to the target")

print(f"** Second Star = {min(allCosts)}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))