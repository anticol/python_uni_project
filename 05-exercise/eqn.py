import numpy
import re
import sys

def main(input_filename):
    
    number_of_line = 0
    coeff = dict()
    vars = []

    for line_number, line in enumerate(open(input_filename, 'r')):
        coeff[line_number] = dict()
        number_of_line = line_number + 1

        no_spaces = line.replace(' ', '')
        for index, part in enumerate(re.findall(r'([=\-+]?[a-z0-9]+)', no_spaces)):
            match = re.match(r'^([=\-+])?(\d*)(\w*)$', part)

            sign = match.group(1)
            if not sign:
                sign = '+'
            cft = match.group(2)
            if cft:
                cft = cft
            else:
                cft = '1'
            letter = match.group(3)
            if sign == '=':
                vars.append(int(cft))
            else:
                coeff[line_number][letter] = int('%s%s' % (sign, cft))

    variables = set()
    for row_index, coefficients in coeff.items():
        for letter, cft in coefficients.items():
            if letter not in variables:
                variables.add(letter)

    mtx = []
    for i in range(number_of_line):
        out = []
        for variable in sorted(list(variables)):
            if i in coeff and variable in coeff[i]:
                out.append(coeff[i][variable])
            else:
                out.append(0)

        mtx.append(out)

    augmented_matrix = [row.copy() for row in mtx]
    for index, number in enumerate(vars):
        augmented_matrix[index].append(number)

    cm_rank = numpy.linalg.matrix_rank(numpy.array(mtx))
    am_rank = numpy.linalg.matrix_rank(numpy.array(augmented_matrix))

    if am_rank != cm_rank:
        print('no solution')
    else:
        try:
            solutions_strings = []
            solts = numpy.linalg.solve(numpy.array(mtx), numpy.array(vars))
            for variable, solution in zip(sorted(list(variables)), solts):
                solutions_strings.append('%s = %s' % (variable, solution))
            print('solution: %s' % ", ".join(solutions_strings))
        except:
            solution_space = len(variables) - cm_rank
            print('solution space dimension: %s' % solution_space)


if len(sys.argv) >= 2:
    input_filename = sys.argv[1]
    main(input_filename)

