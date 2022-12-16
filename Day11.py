from datetime import datetime
import math
import copy

#### Main
print("2022 --- Day 11: Monkey in the Middle ---")
start_time = datetime.now()

def calculateWorriedValue(worried, operation):
    if operation[1] == "old":
        value = worried
    else:
        value = int(operation[1])

    if operation[0] == "+":
        return(worried + value)
    else: 
        return(worried * value)


def firstStar(monkeys):
    for i in range(1,21):
        #print(f"Round {i} : ---- Beginning ----")
        for monkeyId in monkeys.keys(): 
            items = monkeys[monkeyId][0]
            #print(f"    ** Monkey {monkeyId} is playing. List of Items : {items}")
            itemId = 1
            while len(items)>0:
                item = items.pop()
                #print(f"       - Examinating item {itemId} : Worried Value : {item}")
                item = calculateWorriedValue(item, monkeys[monkeyId][1])
                #print(f"       - Examinating item {itemId} : new Worried : {item}")
                item = math.floor(item/3)
                #print(f"       - Examinating item {itemId} : Monkey is worried with the item, divided by 3 --> new Worried : {item} -- Examinate condition : Divided by {monkeys[monkeyId][2]}")
                if item % monkeys[monkeyId][2] == 0:
                    targetMonkey = monkeys[monkeyId][3]
                    #print(f"       - Examinating item {itemId} : TRUE condition apply -> sending item to monkey {targetMonkey}")

                else:
                    targetMonkey = monkeys[monkeyId][4]
                    #print(f"       - Examinating item {itemId} : FALSE condition apply -> sending item to monkey {targetMonkey}")
                monkeys[targetMonkey][0].append(item)
                itemId += 1
                ## increasing the number of time this monkey inspected an item: 
                monkeys[monkeyId][5] += 1
        #print(f"Round {i} : ---- END of Round ---- Monkeys = {monkeys}")

    inspected = []
    for monkeyId, value in monkeys.items():
        print(f"Monkey {monkeyId} inspected items {value[5]} times.")
        inspected.append(value[5])
    inspected.sort()
    star = inspected[-1] * inspected[-2]

    print(f"  ** First Star : {star}")

def secondStar(monkeys, globalModulo):
    checkRound = [1,20]
    for i in range (1,11): 
        checkRound.append(i*1000)

    for i in range(1,10001):
        #print(f"Round {i} : ---- Beginning ----")
        for monkeyId in monkeys.keys(): 
            items = monkeys[monkeyId][0]
            #print(f"    ** Monkey {monkeyId} is playing. List of Items : {items}")
            itemId = 1
            while len(items)>0:
                item = items.pop()
                #print(f"       - Examinating item {itemId} : Worried Value : {item}")
                item = calculateWorriedValue(item, monkeys[monkeyId][1])
                #print(f"       - Examinating item {itemId} : new Worried : {item} -- Examinate condition : Divided by {monkeys[monkeyId][2]}")
                modulo = item % monkeys[monkeyId][2]
                if modulo == 0:
                    targetMonkey = monkeys[monkeyId][3]
                    #print(f"       - Examinating item {itemId} : TRUE condition apply -> sending item to monkey {targetMonkey}")

                else:
                    targetMonkey = monkeys[monkeyId][4]
                    #print(f"       - Examinating item {itemId} : FALSE condition apply -> sending item to monkey {targetMonkey}")
                monkeys[targetMonkey][0].append(item%globalModulo)
                itemId += 1
                ## increasing the number of time this monkey inspected an item: 
                monkeys[monkeyId][5] += 1
        #print(f"Round {i} : ---- END of Round ---- Monkeys = {monkeys}")
        if i in checkRound: 
            print(f"===== After {i} rounds ==========")
            inspected = []
            for monkeyId, value in monkeys.items():
                print(f"Monkey {monkeyId} inspected items {value[5]} times.")
                inspected.append(value[5])
            inspected.sort()
            star = inspected[-1] * inspected[-2]

            if i == 10000:
                print(f"  ** Second Star : {star}")



f = open(".\Day11.txt", "r")
monkeys = {}
currentline = 1
globalModulo = 1
for line in f:
    line = line.rstrip()
    match currentline%7:
        case 1:
            monkey_id = int(line[7])
            print(f"monkey = {monkey_id}")
        case 2:
            starting_items = [int(x) for x in line[17:].split(',')]
            print(f"starting_items = {starting_items}")
        case 3:
            ## operation
            operation = line[23:].split(' ')
            print(f"operation = {line} --> {operation}")
        case 4:
            ## test
            test = int(line[21:])
            globalModulo *= test
            print(f"test  = {line} --> test={test} -- Global Modulo = {globalModulo}")
        case 5:
            ## true
            ifTrue = int(line[29:])
            print(f"true  = {line} --> ifTrue={ifTrue}")
        case 6:
            ## FALSE
            ifFalse = int(line[30:])
            print(f"false  = {line} -- ifFalse = {ifFalse}")
        case _:
            ## new linte
            monkeys[monkey_id] = [starting_items, operation, test, ifTrue, ifFalse, 0]
            print(f"EOL  = {line}")
    currentline += 1

monkeySecondStar = copy.deepcopy(monkeys)

firstStar(monkeys)
secondStar(monkeySecondStar, globalModulo)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))