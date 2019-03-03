"""
Program to distribute the exercises of activity sheets from Calculus 3
among students.

It is required that the input comes in the following format:

*For the problems, the input file shall be named problems.txt
and must be placed in the same directory as script. The input
format for problems is as follows:

Activity_Number:Quantity_of_Problems
Example:
1:10
2:8
3:5

*For the students that will participate, the input file shall be named
students.txt, and must be placed in the same directory as script. The
input format for students is as follows:

Student_Name
Example:
JohnSmith
Mike
Billy

"""

import random
import os


class Student:
    def __init__(self, name):
        """
        Constructor
        :param name: str - name of student
        """
        self.name = name    # name of student
        self.problems = {}  # set of assigned problems { activity: [p1, p2, p3] }
        self.assigned = 0

    def assign(self, activity, problem):
        """
        Assign a set of problems to a student.
        :param activity: int - Activity sheet
        :param problem: int - Number of problem
        :return: None
        """

        if not self.problems.get(activity):
            p = []
            p.append(problem)
            self.problems.__setitem__(activity, p)
        else:
            p = self.problems.get(activity)
            p.append(problem)
            self.problems.__setitem__(activity, p)
        self.assigned += 1
        return None

    def get_assignment(self):
        """
        Get student's assignment.
        :return: str with assigned problems
        """
        s = self.name+', you have '+str(self.assigned)+' problems assigned:\n'
        for a in self.problems:
            s += 'From activity '+str(a)+' {'
            probs = self.problems.get(a)
            for p in probs:
                s += ' '+str(p)+','
            s += '}\n'
        return s


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

students = []
problems = {}
total_problems = 0

# Reading students.txt
try:
    f = open('students.txt', 'r')
    std = f.readlines()
    f.close()
    for s in std:
        students.append(Student(s.replace('\n', '')))
except FileNotFoundError:
    print('Something went wrong while reading students.txt. '
          '\nPlease make sure the file exists and is located '
          'in the same directory as the script, and that it '
          'follows the format required.\n')

# Reading problems.txt
try:
    f = open('problems.txt', 'r')
    prob = f.readlines()
    f.close()
    for p in prob:
        d = p.replace('\n', '').split(':')
        problems.__setitem__(int(d[0]), int(d[1]))
        total_problems += int(d[1])
except FileNotFoundError:
    print('Something went wrong while reading problems.txt. '
          '\nPlease make sure the file exists and is located '
          'in the same directory as the script, and that it '
          'follows the format required.\n')

if len(students) == 0:
    print('No students are participating')
else:
    excess = total_problems % len(students)           # Residue of problems / students
    num_problems = total_problems-excess            # Number of problems - residue
    prob_per_std = int(num_problems/len(students))  # Problems per student, without residue

    # Saving some stats for results
    x = excess
    probs_x = num_problems

    # Distribution algorithm
    for p in problems:
        i = problems.get(p)
        while i > 0:
            r = random.randint(0, len(students)-1)    # Selecting random student
            std = students[r]
            if std.assigned < prob_per_std:     # Distributing problems evenly
                std.assign(p, i)
                i -= 1
                num_problems -= 1
            elif std.assigned == prob_per_std and num_problems == 0:    # Distributing residue
                std.assign(p, i)
                i -= 1
                excess -= 1

    try:
        f = open('results.txt', 'w')
        f.write('STATS'
                '\nTotal of students: {0}'
                '\nTotal of problems: {1}'
                '\nExcess: {2}'
                '\nTotal - excess: {3}'
                '\nPorblems per student (without residue): {4}'
                '\n---------------------------------------------'
                '\nRESULTS\n\n'
                .format(len(students), total_problems, x, probs_x, prob_per_std))
        for s in students:
            f.write(s.get_assignment()+'\n')
        f.close()
        print('Distribution calculated successfully!'
              '\nResults can be found at:', os.getcwd()+'/results.txt')
    except Exception:
        print('Something went wrong while printing results.')
