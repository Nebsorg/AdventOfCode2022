import copy
from datetime import datetime

#### Main
print("2022 --- Day 8: Treetop Tree House ---")
start_time = datetime.now()


def computeScenicValue(tree, forest):
    nbOfRow = len(forest)
    nbOfColumn = len(forest[0])
    row = tree[0]
    col = tree[1]
    treeHigh = forest[row][col][0]
    vectors = [(-1,0), (1,0), (0,-1), (0,1)]

    if row == 0 or col == 0 or row == nbOfRow-1 or col == nbOfColumn-1:
        #print(f"  - Tree {tree} - {forest[row][col][0]} --> Scenic Value = 0 (on Edge)")
        return(0)

    scenicScore = 1
    for vector in vectors:
        nbOfTreeVisible = 0
        currentRow = row + vector[0]
        currentCol = col + vector[1]
        while currentRow >= 0 and currentRow < nbOfRow and currentCol >= 0 and currentCol < nbOfColumn:
            ## we can see this tree, as we are still within boudaries
            nbOfTreeVisible += 1

            ## does it block the sight
            testedTreeHigh = forest[currentRow][currentCol][0]
            if testedTreeHigh >= treeHigh:
                ## yes --> we stop for this direction
                break

            ## no --> checking next tree
            currentRow += vector[0]
            currentCol += vector[1]

        #print(f"  - Tree {tree} - {forest[row][col][0]} --> #tree visible on side {vector} : {nbOfTreeVisible}")
        scenicScore *= nbOfTreeVisible

    #print(f"  - Tree {tree} - {forest[row][col][0]} --> Scenic score = {scenicScore}")
    return (scenicScore)

def isVisible(tree, forest):
    nbOfRow = len(forest)
    nbOfColumn = len(forest[0])
    row = tree[0]
    col = tree[1]
    treeHigh = forest[row][col][0]
    vectors = [(-1,0), (1,0), (0,-1), (0,1)]

    if row == 0 or col == 0 or row == nbOfRow-1 or col == nbOfColumn-1:
        #print(f"  - Tree {tree} - {forest[row][col]} --> VISIBLE (on Edge)")
        return(True)

    for vector in vectors:
        currentRow = row + vector[0]
        currentCol = col + vector[1]
        while currentRow >= 0 and currentRow < nbOfRow and currentCol >= 0 and currentCol < nbOfColumn:
            testedTreeHigh = forest[currentRow][currentCol][0]
            if testedTreeHigh >= treeHigh:
                #print(f"  - Tree {tree} - {forest[row][col]} --> INVISIBLE on side {vector}")
                ## invisible on this side
                break
            currentRow += vector[0]
            currentCol += vector[1]
        else:
            ## reach the edges without founded a tree equal or higher --> visible
            #print(f"  - Tree {tree} - {forest[row][col]} --> VISIBLE on side {vector}")
            return(True)

    ## invisible on each size
    #print(f"  - Tree {tree} - {forest[row][col]} --> INVISIBLE on 4 side")
    return(False)


def firstStar(forest):
    star = 0
    visibleTree = 0
    nbOfRow = len(forest)
    nbOfColumn = len(forest[0])

    for rowNb in range(nbOfRow):
        for colNb in range(nbOfColumn):
            if isVisible((rowNb, colNb), forest):
                visibleTree += 1

    star = visibleTree
    print(f"  ** First Star : {star}")

def secondStar(forest):

    nbOfRow = len(forest)
    nbOfColumn = len(forest[0])
    maxScenic = 0
    ## compute all scenic values :
    for rowNb in range(nbOfRow):
        for colNb in range(nbOfColumn):
            forest[rowNb][colNb][1] = computeScenicValue((rowNb, colNb), forest)
            if maxScenic < forest[rowNb][colNb][1]:
                maxScenic = forest[rowNb][colNb][1]
                #print(f"Tree {forest[rowNb][colNb]} with an high of {forest[rowNb][colNb][0]} has a bigger scenic value than max {maxScenic}")
    star = maxScenic
    print(f"  ** Second Star : {star}")


forest = []
currentRow = 0
f = open(".\Day8.txt", "r")
for line in f:
    line = line.rstrip()
    forest.append([[int(x),0] for x in line])

firstStar(forest)
secondStar(forest)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))