from __future__ import print_function
import numpy as np
import re,os

FILENAME = 'equations.txt'
letters = []

def parseLeft(toParse):
    items = []
    splitedItems = toParse.split(' ')

    if '-' not in splitedItems[0]:
        items.append('+' + splitedItems[0])
    else:
        items.append(splitedItems[0])
    iterator = 1

    while iterator + 1 < len(splitedItems):
        items.append(splitedItems[iterator] + splitedItems[iterator +1])
        iterator = iterator + 2

    equation = {}
    for i in items:
        if i[:-1] == '-':
            number = int('-1')
        #elif i[0] == '-':
        #    number = int((i[:-1])[1:])
        else:
            number = 1 if len(i[:-1]) < 2 else int(i[:-1])
        letter = i[-1:]
        if letter not in letters:
            letters.append(letter)
        equation.update({letter: number})

    return equation


def createArrays(parsedEquations):
    variablesCount = len(parsedEquations[0])
    variables = list(parsedEquations[0].keys())
    arrays = []
    iterator1 = 0
    iterator2 = 0

    while iterator1 < len(parsedEquations):
        newArray = []
        while iterator2 < variablesCount:
            variable = variables[iterator2]
            newArray.append(parsedEquations[iterator1][variable])
            iterator2 = iterator2 +1
        arrays.append(newArray)
        iterator1 = iterator1 +1
        iterator2 = 0

    return arrays

def checkRanks(a,b):
    rank_A = np.linalg.matrix_rank(a)
    rank_B = np.linalg.matrix_rank(b)
    if rank_B < len(letters):
        print('solution space dimension:', len(letters) -rank_B)
        return False

def checkZeroDeterminant(a):
    det = int(np.linalg.det(a))
    return det == 0

def countResult(a,b,variables,EQUATIONS):
    result = np.linalg.solve(a, b)
    iterator = 0
    #for i in EQUATIONS:
        #print(i)
    results_dict = {}

    it = 0
    while it < len(variables):
        results_dict.update({variables[it]: str(round(result[it],5))})
        it = it + 1

    print('solution: ', end='')
    delimiter = ''
    for key in sorted(results_dict):
        print(delimiter + key + ' = ' + results_dict[key] , end= '')
        delimiter = ', '

def compute(input):

    EQUATIONS = input

    results_array = []
    parsedEquations = []
    for i in EQUATIONS:
        parsedEquations.append(parseLeft(i.split('=')[0]))
        results_array.append(int(i.split('=')[1].strip()))

    for i in parsedEquations:
        for l in letters:
            if l not in i:
                i[l] = 0
    equations_arrays = createArrays(parsedEquations)
    matrix_b_arrays = []

    it = 0
    while it < len(results_array):
        matrix_b_arrays.append(equations_arrays[it] + [results_array[it]])
        it = it + 1

    matrix_a = np.matrix(equations_arrays)
    matrix_b = np.matrix(matrix_b_arrays)
    if(checkRanks(matrix_a,matrix_b) == False):
        return
    if checkZeroDeterminant(matrix_a) is True:
        print('no solution\n')
        return

    a = np.array(createArrays(parsedEquations))
    b = np.array(results_array)
    countResult(a,b,letters,EQUATIONS)
    return


def main():
    f = open(FILENAME, 'r', encoding='utf-8-sig')
    input = f.read().split('\n')
    equations = []

    for equation in input:
        equations.append(equation.strip())

    #(equations)
    compute(equations)

main()
