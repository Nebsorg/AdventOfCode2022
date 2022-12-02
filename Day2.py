print("2022 --- Day 2 !")
column1 = ['A', 'B', 'C']
column2 = ['X', 'Y', 'Z']
winList = {1:2, 2:3, 3:1}
looseList = {1:3, 2:1, 3:2}

def scoreFirstStar(round):
    #draw
    if round[0] == round[1]:
        return(3+round[1])

    #win
    if round[1] == winList[round[0]]:
        return(6+round[1])

    #Loose
    return(round[1])

def scoreSecondStar(round):
    match round[1]:
        case 'X':
            ## Lose
            return(looseList[round[0]])
        case 'Y':
            ## Draw
            return(3 + round[0])
        case _:
            ## win
            return(6+winList[round[0]])


def firstStar(listOfRound):
    totalScore = 0
    for round in listOfRound:
        currentScore = scoreFirstStar(round)
        totalScore += currentScore

    print(f"  ** First Star : {totalScore}")

def secondStar(listOfRound):
    totalScore = 0
    for round in listOfRound:
        currentScore = scoreSecondStar(round)
        totalScore += currentScore

    print(f"  ** Second Star : {totalScore}")

f = open(".\Day2.txt", "r")
listOfRound1 = []
listOfRound2 = []
for line in f:
    line = line.strip()
    round = line.split(' ')
    listOfRound1.append([column1.index(round[0])+1, column2.index(round[1])+1])
    listOfRound2.append([column1.index(round[0])+1, round[1]])

firstStar(listOfRound1)
secondStar(listOfRound2)

