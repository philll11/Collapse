from building import *
from collections import OrderedDict

# speed test - use "python optimizer.py" to run
if __name__ == "__main__":
    import timeit
    test_size = 100 # set to 100 to check time for speed race
    t1 = timeit.repeat(stmt="optimizer.max_food(b)", setup="import gc, building, optimizer; b = building.random_building({0}, True); gc.collect()".format(test_size), repeat=3, number=1)
    t2 = timeit.repeat(stmt="optimizer.max_supplies(b)", setup="import gc, building, optimizer; b = building.random_building({0}, False); gc.collect()".format(test_size), repeat=3, number=1)
    # some calculation that takes ~1 sec on my machine
    tref = timeit.repeat(stmt="for i in range(1000000): a=i^2", setup="import gc; gc.collect()", repeat=3, number=19)
    print("max_food(n={0}) = {1} ({3} normalized), max_supplies(n={0}) = {2} ({4} normalized)".format(test_size, min(t1), min(t2), min(t1) / min(tref), min(t2) / min(tref)))

def max_food(building):
    """returns the maximum number of food that can be collected from given building"""
    start = building.size
    length = (building.size * 2) + 1
    matrix = [[building.rooms[y][x].food for x in range(length)] for y in range(length)]
    # matrix = [[0 for x in range(length)] for x in range(length)]

    # Initialize started points for the four quadrants
    # matrix[start - 1][start] = building.rooms[start - 1][start].food
    # matrix[start + 1][start] = building.rooms[start + 1][start].food
    # matrix[start][start - 1] = building.rooms[start][start - 1].food
    # matrix[start][start + 1] = building.rooms[start][start + 1].food

    matrix[start][start] = 0

    # Initialize columns for upper and lower quadrants
    i = start - 1
    while i > 0:
        matrix[i - 1][start] = matrix[i - 1][start] + matrix[i][start]
        i = i - 1
    i = start + 1
    while i < length - 1:
        matrix[i + 1][start] = matrix[i + 1][start] + matrix[i][start]
        i = i + 1

    # Initialize rows for left and right quadrants
    j = start + 1
    while j < length - 1:
        matrix[start][j + 1] = matrix[start][j + 1] + matrix[start][j]
        j = j + 1
    j = start - 1
    while j > 0:
        matrix[start][j - 1] = matrix[start][j - 1] + matrix[start][j]
        j = j - 1


    # Builds upper left matrix
    i = start - 1
    while i >= 0:
        j = start - 1
        while j >= 0:
            matrix[i][j] = max(matrix[i + 1][j], matrix[i][j + 1]) + matrix[i][j]
            j = j - 1
        i = i - 1

    # Builds upper right matrix
    i = start - 1
    while i >= 0:
        j = start + 1
        while j < length:
            matrix[i][j] = max(matrix[i + 1][j], matrix[i][j - 1]) + matrix[i][j]
            j = j + 1
        i = i - 1

    # Builds lower right matrix
    i = start + 1
    while i < length:
        j = start + 1
        while j < length:
            matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1]) + matrix[i][j]
            j = j + 1
        i = i + 1

    # Builds lower left matrix
    i = start + 1
    while i < length:
        j = start - 1
        while j >= 0:
            matrix[i][j] = max(matrix[i - 1][j], matrix[i][j + 1]) + building.rooms[i][j].food
            j = j - 1
        i = i + 1

    # for i in range(0, length):
    #     for j in range(0, length):
    #         print(building.rooms[i][j], end="\t")
    #     print()
    # print("\n\n\n")

    #print(max(matrix[0][0], matrix[0][length - 1], matrix[length - 1][0], matrix[length - 1][length - 1]))

    return max(matrix[0][0], matrix[0][length - 1], matrix[length - 1][0], matrix[length - 1][length - 1])

def addToDict(currentDict, previousDict):
    for key in previousDict:
        if key in currentDict:
            currentDict[key].append(previousDict[key])
        else:
            currentDict[key] = [previousDict[key]]


def max_supplies(building):
    start = building.size
    length = (building.size * 2) + 1
    # Building the matrix
    matrix = [[{} for x in range(length)] for y in range(length)]

    # Player start point
    matrix[start][start] = {0: [0]}

    # Initialize started points for the four quadrants
    matrix[start - 1][start] = {building.rooms[start - 1][start].food: [building.rooms[start - 1][start].water]}
    matrix[start + 1][start] = {building.rooms[start + 1][start].food: [building.rooms[start + 1][start].water]}
    matrix[start][start - 1] = {building.rooms[start][start - 1].food: [building.rooms[start][start - 1].water]}
    matrix[start][start + 1] = {building.rooms[start][start + 1].food: [building.rooms[start][start + 1].water]}

    # Initialize columns for upper and lower quadrants
    i = start - 1
    while i > 0:
        matrix[i - 1][start] = {building.rooms[i - 1][start].food + list(matrix[i][start].keys())[0]:
                                    [building.rooms[i - 1][start].water + list(matrix[i][start].values())[0][0]]}
        i = i - 1
    i = start + 1
    while i < length - 1:
        matrix[i + 1][start] = {building.rooms[i + 1][start].food + list(matrix[i][start].keys())[0]:
                                    [building.rooms[i + 1][start].water + list(matrix[i][start].values())[0][0]]}
        i = i + 1

    # Initialize rows for left and right quadrants
    j = start - 1
    while j > 0:
        matrix[start][j - 1] = {building.rooms[start][j - 1].food + list(matrix[start][j].keys())[0]:
                                    [building.rooms[start][j - 1].water + list(matrix[start][j].values())[0][0]]}
        j = j - 1
    j = start + 1
    while j < length - 1:
        matrix[start][j + 1] = {building.rooms[start][j + 1].food + list(matrix[start][j].keys())[0]:
                                    [building.rooms[start][j + 1].water + list(matrix[start][j].values())[0][0]]}
        j = j + 1

    # Builds upper left matrix
    i = start - 1
    while i >= 0:
        j = start - 1
        while j >= 0:

            # Adding water from cell below
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i + 1][j]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i + 1][j][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            # Adding food from neighbouring cell
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i][j + 1]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i][j + 1][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            j = j - 1
        i = i - 1


    # Builds upper right matrix
    i = start - 1
    while i >= 0:
        j = start + 1
        while j < length:

            # Adding water from cell below
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i + 1][j]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i + 1][j][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            # Adding food from neighbouring cell
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i][j - 1]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i][j - 1][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            j = j + 1
        i = i - 1

    # Builds lower right matrix
    i = start + 1
    while i < length:
        j = start + 1
        while j < length:

            # Adding water from cell below
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i - 1][j]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i - 1][j][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            # Adding food from neighbouring cell
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i][j - 1]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i][j - 1][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            j = j + 1
        i = i + 1

    # Builds lower right matrix
    i = start + 1
    while i < length:
        j = start - 1
        while j >= 0:

            # Adding water from cell below
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i - 1][j]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i - 1][j][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            # Adding food from neighbouring cell
            roomKey = building.rooms[i][j].food
            roomValue = building.rooms[i][j].water
            for matrixKey in matrix[i][j + 1]:
                keySum = roomKey + matrixKey
                listOfValues = matrix[i][j + 1][matrixKey]
                if len(listOfValues) > 1:
                    listOfValues.sort()
                valueSum = roomValue + listOfValues[0]

                if keySum in matrix[i][j]:
                    matrix[i][j][keySum].append(valueSum)
                else:
                    matrix[i][j][keySum] = [valueSum]

            j = j - 1
        i = i + 1

    # for i in range(0, length-1):
    #     for j in range(0, length-1):
    #         print(matrix[i][j], end="\t")
    #     print()
    # print("\n\n")

    list1 = [matrix[0][0], matrix[0][length - 1], matrix[length - 1][0], matrix[length - 1][length - 1]]
    return list1
