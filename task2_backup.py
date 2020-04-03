# !/usr/bin/env python3.7
import random
import logging

class Student:
    def __init__(self,name,surname, attendence = True):
        self.name = name
        self.surname = surname
        self.grades = []
        self.attendence = attendence

    def add_grade(grade):
        self.grades.append(grade)

    def avarage_grade():
        av = sum(self.grades)
        av /= len(self.grades)
        return av
    
    def set_attendence(present = True):
        self.attendence = present

    def __str__(self):
        return "Name: {n}  Surname: {s} Is present: {p}\n".format(n=self.name, s=self.surname, p=self.attendence)


class Class:

    def __init__(self, name, students = []):
        self.name = name
        self.students = students

    def add_student(self, name, surname, attendence = True):
        self.students.append(Student(name,surname, attendence))
    
    def avarage_grade_class():
        grades = [st.avarage_grade() for st in self.students]
        av = sum(grades)
        av /= len(grades)
        return av
    
    def count_attendence():
        count = 0
        for st in self.students:
            if st.attendence:
                count += 1
        return count

    def __sizeof__(self):
        return len(self.students)

    def __str__(self):
        info = "Class {}\n".format(self.name)

        for s in self.students:
            info += str(s)

        return info

if __name__ == "__main__":

    students = [Student('St1', 'LN1', True),Student('St2', 'LN2', False),Student('St3', 'LN3', True)]
    
    class_name = input("Insert class name: ")

    class1 = Class(class_name, students)
    
    try:
        while True:
            task = int(input("""What would you like to do?
            1 - add a student
            2 - see class stats
            3 - see avarage score
            4 - add a grade
            """))
            if task == 1:
                s_name = input("Insert student name: ")
                s_lname = input("Insert student surname: ")
            if task == 2:
                logging.info(str(class1))
                print(str(class1))

    except KeyboardInterrupt:
        print("Class dismissed!")
