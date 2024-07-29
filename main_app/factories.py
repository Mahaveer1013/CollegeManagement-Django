import main_app.factories as factories
from django.utils import timezone
from django.contrib.auth import get_user_model
from main_app.models import *
import factory
from factory.django import DjangoModelFactory

User = get_user_model()

class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.CustomUser'

    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    gender = factory.Faker('random_element', elements=[choice[0] for choice in User.GENDER])
    user_type = factory.Faker('random_element', elements=[choice[0] for choice in User.USER_TYPE])
    address = factory.Faker('address')

class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.Department'

    name = factory.Faker('word')

class AcademicYearFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.AcademicYear'

    academic_year_start = factory.Faker('year')
    academic_year_end = factory.LazyAttribute(lambda obj: int(obj.academic_year_start) + 4)

class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.Subject'

    name = factory.Faker('word')
    subject_code = factory.Faker('bothify', text='??###')

class StaffFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.Staff'

    department = factory.SubFactory(DepartmentFactory)
    user = factory.SubFactory(CustomUserFactory, user_type='2')
    faculty_id = factory.Faker('bothify', text='FAC###')
    phone_number = factory.Faker('phone_number')
    resume = factory.django.FileField(filename='resume.pdf')
    qualification = factory.Faker('word')
    experience = factory.Faker('paragraph')

class ClassListFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.ClassList'

    department = factory.SubFactory(DepartmentFactory)
    semester = factory.Faker('random_element', elements=['1', '2', '3', '4', '5', '6', '7', '8'])
    section = factory.Faker('random_letter')
    incharge = factory.SubFactory(StaffFactory)

class StudentFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.Student'

    user = factory.SubFactory(CustomUserFactory, user_type='3')
    roll_number = factory.Faker('bothify', text='ROLL###')
    register_number = factory.Faker('bothify', text='REG###')
    department = factory.SubFactory(DepartmentFactory)
    phone_number = factory.Faker('phone_number')
    parent_phone_number = factory.Faker('phone_number')
    class_name = factory.SubFactory(ClassListFactory)
    dob = factory.Faker('date_of_birth')
    mentor = factory.SubFactory(StaffFactory)
    academic_year = factory.SubFactory(AcademicYearFactory)

class PeriodFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.Period'

    department = factory.SubFactory(DepartmentFactory)
    class_name = factory.SubFactory(ClassListFactory)
    subject = factory.SubFactory(SubjectFactory)
    staff = factory.SubFactory(StaffFactory)

class AttendanceFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.Attendance'

    subject = factory.SubFactory(SubjectFactory)
    student = factory.SubFactory(StudentFactory)
    date = factory.Faker('date')
    period = factory.Faker('random_int', min=1, max=8)
    status = factory.Faker('random_element', elements=[choice[0] for choice in Attendance.STATUS_CHOICES])

class ExamDetailFactory(DjangoModelFactory):
    class Meta:
        model = 'main_app.ExamDetail'

    maximum_mark = 100
    added_by = factory.SubFactory(CustomUserFactory)
    semester = factory.Faker('random_element', elements=[choice[0] for choice in ExamDetail.SEM_CHOICES])
    exam_date = factory.Faker('date')
    exam_type = factory.Faker('random_element', elements=[choice[0] for choice in ExamDetail.EXAM_TYPE])
    department = factory.SubFactory(DepartmentFactory)
    academic_year = factory.SubFactory(AcademicYearFactory)

# Add more factories for other models similarly...

# Usage example:
if __name__ == "__main__":
    # Create a department
    department = DepartmentFactory.create()

    # Create an academic year
    academic_year = AcademicYearFactory.create()

    # Create a subject
    subject = SubjectFactory.create(department=department)

    # Create a staff member
    staff = StaffFactory.create(department=department)

    # Create a class list
    class_list = ClassListFactory.create(department=department, incharge=staff)

    # Create a student
    student = StudentFactory.create(department=department, class_name=class_list, mentor=staff, academic_year=academic_year)

    # Create an attendance record
    attendance = AttendanceFactory.create(subject=subject, student=student)

    # Create an exam detail
    exam_detail = ExamDetailFactory.create(department=department, academic_year=academic_year)
