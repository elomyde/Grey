import random

def create_map(mapSizeX, mapSizeY):
    #creates a square list of lists size (mapSize+2)^2 filled with ZEROs
    map = []
    for i in range(mapSizeY):
        map.append(0)
        map[i] = []
        for j in range(mapSizeX):
            map[i].append(0)
    return map

def generateBomb(x, y, bombNumber, map):
    coords = []
    randcoords = []
    for i in range (1, y-1) :
        for j in range (1, x-1) :
            coords.append((i, j))
    randcoords = random.sample(coords, bombNumber)
    for items in randcoords :
        map[items[0]][items[1]] = 'bomb'
    return map

def fillNumbers(map1, map2):
    numMap = map1
    bombMap = map2
    #Searches the whole grid for bombs. When one is found increases the value of its vicinity by 1
    for i in range(1, len(bombMap)-1) :
        for j in range(1, len(bombMap[i])-1) :
                if bombMap[i][j] == 'bomb' :
                        for k in range (i-1, i+2) :
                            for l in range (j-1, j+2) :
                                numMap[k][l] += 1
    return numMap

def assembleMap(mapSizeX = 5, mapSizeY = 5, bombNumber = 10):
    numMap = create_map(mapSizeX + 2, mapSizeY +2)
    bombMap = create_map(mapSizeX + 2, mapSizeY +2)
    bombMap = generateBomb(mapSizeX + 2, mapSizeY + 2, bombNumber, bombMap)

    numMap = fillNumbers(numMap, bombMap)
    finalMap = create_map(mapSizeX, mapSizeY)

    for i in range(0, mapSizeY) :
        for j in range(0, mapSizeX) :
            if bombMap[i+1][j+1] == 'bomb' :
                finalMap[i][j] = 'bomb'
            else :
                finalMap[i][j] = numMap[i+1][j+1]
    return finalMap


x = int(input())
y = int(input())
z = int(input())

print(assembleMap(x,y,z))
