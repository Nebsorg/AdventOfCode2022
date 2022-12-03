from datetime import datetime

#### Main
print("2022 --- Day 3 !")
start_time = datetime.now()

def firstStar(backpacks):
    miscategorizedItem = []
    for items in backpacks:
        mid = int((len(items) / 2))
        intersection = {x for x in items[:mid] if x in items[mid:]}
        miscategorizedItem.append(intersection.pop())
    valueIntersection = [ord(value) - 38 if ord(value) < 91 else ord(value) - 96 for value in miscategorizedItem]
    print(f"  ** First Star : {sum(valueIntersection)}")

def secondStar(listOfRound):
    groupItems = []
    currentGroupId = 1
    currentGroupBackPack = []
    for items in backpacks:
        currentGroupBackPack.append(set(items))
        if currentGroupId%3 == 0:
            intersection = currentGroupBackPack[0].intersection(currentGroupBackPack[1], currentGroupBackPack[2])
            groupItems.append(intersection.pop())
            currentGroupBackPack = []
        currentGroupId+=1

    valueIntersection = [ord(value) - 38 if ord(value) < 91 else ord(value) - 96 for value in groupItems]
    print(f"  ** Second Star : {sum(valueIntersection)}")


f = open(".\Day3.txt", "r")

backpacks = []
for line in f:
    backpacks.append(list(line.strip()))

firstStar(backpacks)
secondStar(backpacks)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))