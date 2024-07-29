import os
import django
import sys

# Ensure the project directory is in the sys.path
sys.path.append('C:/MyDesktop/Projects/CollegeManagement-Django')

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_management_system.settings')
django.setup()

from faker import Faker
from main_app.factories import *  # Adjust this import to match your actual app and factories module

fake = Faker()

# Create some departments
departments = DepartmentFactory.create_batch(5)

# Create some academic years
academic_years = AcademicYearFactory.create_batch(4)

# Create some subjects
subjects = SubjectFactory.create_batch(10)

# Create some staff members
staff_members = StaffFactory.create_batch(10)

# Create some class lists
class_lists = ClassListFactory.create_batch(5)

# Create some students
students = StudentFactory.create_batch(50)

# Create some periods
periods = PeriodFactory.create_batch(20)

# Create some attendance records
attendances = AttendanceFactory.create_batch(100)

# Create some exam details
exam_details = ExamDetailFactory.create_batch(20)

print("Dummy data generated successfully!")
