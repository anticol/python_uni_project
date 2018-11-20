import csv
import json
import sys
import numpy as np

deadline_points = {}
student_points = {}

def get_mean(p):
    points = np.array(p)
    mean = np.mean(points)
    return mean

def get_median(p):
    points = np.array(p)
    median = np.median(points)
    return median


def get_first_quartile(p):
    points = np.array(p)
    first_quartile = np.percentile(points, 25)
    return first_quartile


def get_last_quartile(p):
    points = np.array(p)
    last_quartile = np.percentile(points, 75)
    return last_quartile


def get_passed(p):
    passed = 0
    for i in p:
        if i > 0:
            passed += 1
    return passed


def print_results(data):
    result = {}
    for i in data:
        deadline = {}
        deadline['mean'] = get_mean(data[i])
        deadline['median'] = get_median(data[i])
        deadline['first'] = get_first_quartile(data[i])
        deadline['last'] = get_last_quartile(data[i])
        deadline['passed'] = get_passed(data[i])
        result.update({i.strip(): deadline})

    print(json.dumps(result, indent=2, ensure_ascii=False))


def parseDates(data):
    exercises = {}
    for i in data:
        if i not in exercises.keys():
            new_results = []
            for arr in data[i]:
                new_results.extend(list(arr.values()))
            results = np.sum(new_results, axis=0)
            exercises.update({i: results})

    return exercises


def parseDeadlines(data):
    result = {}
    for d in data:
        if d[:-3] not in result.keys():
            current = {d[:-3]: [{d[-2:]: deadline_points[d]}]}
            result.update(current)
        else:
            result[d[:-3]].append({d[-2:]: deadline_points[d]})

    return result


def main():
    # dates, deadlines, exercises
    mode = sys.argv[2]

    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        deadlines = reader.fieldnames[1:]
        dates = list(set([x[:-3] for x in reader.fieldnames[1:]]))
        exercises = list(set([x[-2:] for x in reader.fieldnames[1:]]))

        for e in deadlines:
            deadline_points.update({e: []})

        for row in reader:
            row_arr = []
            for val in row.values():
                row_arr.append(val)
            for e in deadlines:
                deadline_points[e].append(float(row[e]))

        parsedCSV = parseDeadlines(deadline_points)

        exercises_points = {}
        for x in exercises:
            exercises_points.update({x: []})

        for date in parsedCSV:
            for exs in parsedCSV[date]:
                for e in exs:
                    exercises_points[e].extend([exs[e]])

        for x in exercises_points:
            exercises_points[x] = np.amax(exercises_points[x], axis=0)

        if (mode == 'deadlines'):
            print_results(deadline_points)
            return
        if (mode == 'exercises'):
            print_results(exercises_points)
            return
        if (mode == 'dates'):
            print_results(parseDates(parsedCSV))
            return

main()
