print("2022 --- Day 1 !")

def firstStar(listOfCalories):
    print(f"  ** First Star : {listOfCalories[0]}")

def secondStar(listOfCalories):
    print(f"  ** Second Star : {sum(listOfCalories[0:3])}")

f = open(".\Day1.txt", "r")
listOfCalories = []
currentElfCalories = 0
for line in f:
    line = line.strip()
    if line == "":
        listOfCalories.append(currentElfCalories)
        currentElfCalories = 0
    else:
        currentElfCalories += int(line)
## don't forget final line
listOfCalories.append(currentElfCalories)
listOfCalories.sort(reverse=True)

firstStar(listOfCalories)
secondStar(listOfCalories)

