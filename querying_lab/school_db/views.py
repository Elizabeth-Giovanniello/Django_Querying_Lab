from django.shortcuts import render
from .models import Student, Instructor, Course, StudentCourse


def index(request):
    students = Student.objects.all()

    # The following line creates a list that allows you to examine the data 
    # from a Queryset in an easier to visualize way
    # It is not required for functionality!
    # Place a breakpoint on line 14, then compare 'students' and 'data_visualization'
    data_visualization = [item for item in students]

    context = {
        'students': students
    }
    return render(request, 'school/index.html', context)

def problem_one(request):
    # Find all students who have a GPA greater than 3.0. 
    # Order the data by highest GPAs first.
    high_gpa_students = Student.objects.filter(gpa__gte=3)
    context = {
        'students': high_gpa_students
    }
    return render(request, 'school/one.html', context)

def problem_two(request):
    # Find all instructors hired prior to 2010
    # Order by hire date
    instructors_hired_before_2010 = Instructor.objects.filter(hire_date__year__lt=2010)

    data_visualization = [item for item in instructors_hired_before_2010]

    context = {
        'instructors': instructors_hired_before_2010
    }
    return render(request, 'school/two.html', context)

def problem_three(request):
    #TODO Find all students who have a A+ in any class and are NOT getting a C+ in any class. 
    # Order the data by student's first name alphabetically.
    students_with_a_plus = StudentCourse.objects.exclude(grade='C+').filter(grade='A+').order_by('student__first_name')

    context = {
        'student_courses': students_with_a_plus
    }
    return render(request, 'school/three.html', context)

def problem_four(request):
    # Find all students who are taking the Programming class. 
    # Order by their grade. 
    programming_students = StudentCourse.objects.filter(course__name="Programming").order_by('grade')

    context = {
        'student_courses': programming_students
    }
    return render(request, 'school/four.html', context)

def problem_five(request):
    # Find all students getting an A in the Programming class. 
    # Order by last name.
    programming_students_with_As = StudentCourse.objects.filter(course__name="Programming", grade__icontains='A').order_by('student__last_name')

    context = {
        'student_courses': programming_students_with_As
    }
    return render(request, 'school/five.html', context)

def problem_six(request):
    # Find all students with a GPA less than 3.0 who are getting an A in Programming class.
    # Order by GPA.
    bad_students_good_coders = StudentCourse.objects.filter(course__name="Programming", grade="A", student__gpa__lt=3.0).order_by('student__gpa')

    context = {
        'student_courses': bad_students_good_coders
    }
    return render(request, 'school/six.html', context)

################## BONUS #################
# These problems will require using Aggregate functions along with annotate()
# https://docs.djangoproject.com/en/4.0/topics/db/aggregation/
# https://docs.djangoproject.com/en/4.0/ref/models/querysets/#annotate

# Create a view function and template for each bonus problem you complete

# BONUS ONE
# Write a query to find any instructors who are only teaching one single course. Display the instructor and the course

from django.db.models import Count, Q, Avg, Max, Min, FloatField, Sum
def bonus_one(request):
    classes_taught = Instructor.objects.annotate(num_courses=Count('course')).filter(num_courses=1)
    context= { 'courses': classes_taught }
    return render(request, 'school/bonus_one.html', context)


# BONUS TWO
# Display all students along with the number of credits they are taking
def bonus_two(request):
    total_credits = Student.objects.annotate(num_credits = Sum('studentcourse__course__credits'))
    data_visualization = [item for item in total_credits]
    context= { 'students': total_credits }
    return render(request, 'school/bonus_two.html', context)

# BONUS THREE
# Find all students who are getting an A in any course and average their GPAs. 
# Display the number of students and their Average GPA
def bonus_three(request): 
    students_with_As = Student.objects.filter(studentcourse__grade__icontains="a").distinct()
    A_student_stats = students_with_As.aggregate(Count('id'), Avg('gpa'))

    data_visualization = [item for item in A_student_stats]
    context = {'students': A_student_stats}
    return render(request, 'school/bonus_three.html', context)

# BONUS FOUR
def bonus_four(request): 

# Write a function that will replace student GPAs in the database with an accurate score based only on their current grades
# This may require multiple queries
# See https://www.indeed.com/career-advice/career-development/gpa-scale for a chart of what point value each grade is worth
    all_students = Student.objects.all()
    all_student_courses = StudentCourse.objects.all()
    student_grade_points = {}

    for entry in all_student_courses:
        if not entry.student.id in student_grade_points.keys():
            student_grade_points[entry.student.id] = []
        student_grade_points[entry.student.id].append(convert_grade(entry.grade))

    for student in all_students:
        student.gpa = average_list(student_grade_points[student.id])
        student.save(update_fields=['gpa'])

    context = {'students': all_students}

    return render(request, 'school/bonus_four.html', context)


def average_list(list):
    total = 0
    for item in list:
        total += item
    return total / len(list)

def convert_grade(grade) -> float:
        match grade:
            case 'A+': return 4
            case 'A': return 4
            case 'A-': return 3.7
            case 'B+': return 3.3
            case 'B': return 3
            case 'B-': return 2.7
            case 'C+': return 2.3
            case 'C': return 2
            case 'C-': return 1.7
            case 'D+': return 1.3
            case 'D': return 1
            case 'F': return 0
            
    



    