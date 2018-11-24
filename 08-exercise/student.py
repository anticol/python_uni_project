import math
import csv
import json
import sys
import datetime
import numpy as np

deadline_points = {}
student_points = {}


def get_mean(p):
    return np.mean(np.array(p))


def get_median(p):
    return np.median(np.array(p))


def get_passed(p):
    passed = 0
    for i in p:
        if i > 0:
            passed += 1
    return passed


def get_regression_slope(dates, points):
    start_date = datetime.datetime.strptime("2018-09-17", '%Y-%m-%d').date().toordinal()
    parsed_dates = sorted(
        [[datetime.datetime.strptime(x.strip(), '%Y-%m-%d').date().toordinal() - start_date] for x in dates])
    dates = np.array(parsed_dates)
    reg = np.linalg.lstsq(dates, points, rcond=-1)[0][0]
    return reg


def get_date(goal, regression_slope):
    if regression_slope == 0:
        return math.inf

    beginning = datetime.datetime.strptime("2018-09-17", '%Y-%m-%d').date().toordinal()
    return datetime.date.fromordinal(int((float(goal) / regression_slope) + beginning)).strftime("%Y-%m-%d")


def cummulate_points(points):
    cummulative_points = []
    idx = 0
    for i in points:
        if idx == 0:
            cummulative_points.append(i)
        else:
            cummulative_points.append(cummulative_points[idx - 1] + i)
        idx += 1
    return cummulative_points


def print_student_results(arr, dates, student_points_by_date):
    student = {}
    student['mean'] = get_mean(arr)
    student['median'] = get_median(arr)
    student['total'] = sum(arr)
    student['passed'] = get_passed(arr)
    student['regression slope'] = get_regression_slope(dates, cummulate_points(student_points_by_date))
    student['date 16'] = get_date(16, student['regression slope'])
    student['date 20'] = get_date(20, student['regression slope'])

    print(json.dumps(student, indent=2, ensure_ascii=False))


def main():
    student_id = sys.argv[2]

    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)

        deadlines = reader.fieldnames[1:]
        dates_list = []
        exercises_list = []
        student_points_by_exercises = {}

        for i in deadlines:
            if i[:-3] not in dates_list:
                dates_list.append(i[:-3])
            if i[-2:] not in exercises_list:
                exercises_list.append(i[-2:])
                student_points_by_exercises.update({i[-2:]: 0})

        for e in deadlines:
            deadline_points.update({e: []})

        for row in reader:
            row_arr = []
            for val in row.values():
                row_arr.append(val)
            student = {row_arr[0]: [float(x.strip()) for x in row_arr[1:]]}
            student_points.update(student)

        student_arrays = (np.array(list(student_points.values())))
        avg_student = np.mean(student_arrays, axis=0)
        student_points.update({'average': list(avg_student)})

    student_points_by_deadline = {}
    idx = 0
    for deadline in deadlines:
        points = student_points[student_id][idx]
        student_points_by_deadline.update({deadline: points})
        student_points_by_exercises.update({deadline[-2:]: (student_points_by_exercises[deadline[-2:]] + points)})
        #if student_points_by_exercises[deadline[-2:]] < points:
        #    student_points_by_exercises.update({deadline[-2:]: points})
        idx += 1
    student_points_by_date = []
    for date in dates_list:
        max = 0
        for deadline in student_points_by_deadline:
            if date in deadline:
                max += student_points_by_deadline[deadline]
        student_points_by_date.append(max)

    print_student_results(list(student_points_by_exercises.values()), dates_list, student_points_by_date)

main()
