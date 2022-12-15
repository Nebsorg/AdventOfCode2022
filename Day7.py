import copy
from datetime import datetime
from collections import defaultdict
from collections import deque

#### Main
print("2022 --- Day 7: No Space Left On Device ---")
start_time = datetime.now()

def firstStar(foldersSize):
    star = 0
    for folder, size in foldersSize.items():
        if size < 100000:
            star += size

    print(f"  ** First Star : {star}")

def secondStar(foldersSize):
    unusedSpace = 70000000 - foldersSize['/']
    neededSpace = 30000000 - unusedSpace

    candidates = [x for x in foldersSize.values() if x >= neededSpace]
    star = min(candidates)

    print(f"  ** Second Star : {star}")

foldersSize = defaultdict(lambda:0)
currentFolder = deque(['/'])
currentFolderKey = '/'

f = open(".\Day7.txt", "r")
for line in f:
    line = line.rstrip()
    if line[0] == '$':
        if line[2:4] == 'cd':
            dest_folder = line[5:]
            if dest_folder == '/':
                ## back to root :
                currentFolder = deque(['/'])
                currentFolderKey = '/'
            elif dest_folder == '..':
                currentFolder.pop()
                currentFolderKey = '/'+''.join([x+'/' for x in list(currentFolder)[1:]])
            else:
                currentFolder.append(dest_folder)
                currentFolderKey += dest_folder+'/'
            print(f" # commande : change folder to {dest_folder} - new folder = {currentFolderKey}")
    else:
        answers = line.split(' ')
        if answers[0] != 'dir':
            size = int(answers[0])
            print(f" result command FILE : = {answers[1]} - size={size}")
            ## adding file size to all folders (current and above)
            deep = 0
            localKey = '/'
            for folder in currentFolder:
                if deep > 0:
                    localKey += folder + '/'
                foldersSize[localKey] += size
                print(f"    Updating folder {localKey} size : new size = {foldersSize[localKey]}")
                deep += 1

firstStar(foldersSize)
secondStar(foldersSize)


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))