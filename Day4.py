from datetime import datetime

#### Main
print("2022 --- Day 4: Camp Cleanup ---")
start_time = datetime.now()

def isIncluded(r1, r2):
    if (r1[0]<=r2[0] and r1[1] >= r2[1]):
        return(True)
    else:
        return(False)

def isOverlap(r1, r2):
    if (r1[1] >= r2[0] and r1[0] <= r2[1]):
        return (True)
    else:
        return (False)

f = open(".\Day4.txt", "r")

firstStar = 0
secondStar = 0
for line in f:
    line = line.rstrip()
    elfs = line.split(',')
    r1 = [int(x) for x in elfs[0].split('-')]
    r2 = [int(x) for x in elfs[1].split('-')]
    print(f"line={line} - elfs={elfs} - r1={r1} - r2={r2}")
    if isIncluded(r1,r2) or isIncluded(r2,r1):
        firstStar += 1
    if isOverlap(r1,r2) or isOverlap(r2,r1):
        secondStar += 1
        print(f"Overlap")

print(f"firstStar = {firstStar}")
print(f"secondStar = {secondStar}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))