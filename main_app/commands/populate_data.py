import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from ..models import *

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        
        # Create 5 departments
        departments = []
        for i in range(5):
            department = Department.objects.create(name=f"Department {i+1}")
            departments.append(department)
        
        # Create 5 custom users for each type
        users = []
        for i in range(5):
            user = CustomUser.objects.create_user(
                email=f"user{i+1}@example.com",
                password="password",
                user_type=random.choice([1, 2, 3]),
                gender=random.choice(["M", "F"]),
                profile_pic=None,
                address=f"Address {i+1}"
            )
            users.append(user)
        
        # Create 5 Admins, Staffs, Students
        for user in users:
            if user.user_type == 1:
                Admin.objects.create(admin=user)
            elif user.user_type == 2:
                staff = Staff.objects.create(admin=user, department=random.choice(departments))
                staff.save()
            elif user.user_type == 3:
                student_class = Class.objects.create(
                    department=random.choice(departments),
                    year=random.choice(['1', '2', '3', '4']),
                    section=f"Section {i+1}"
                )
                Student.objects.create(
                    admin=user,
                    department=random.choice(departments),
                    Class=student_class,
                    register_number=f"Reg{i+1}",
                    roll_number=f"Roll{i+1}"
                )

        # Create 5 subjects
        for i in range(5):
            Subject.objects.create(
                name=f"Subject {i+1}",
                subject_code=f"SUBJ{i+1}",
                staff=Staff.objects.order_by('?').first(),
                department=random.choice(departments)
            )

        # Create 5 days
        for day_name in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            Day.objects.get_or_create(name=day_name)

        # Create 5 timetables
        for i in range(5):
            TimeTable.objects.create(
                department=random.choice(departments),
                Class=Class.objects.order_by('?').first(),
                day=Day.objects.order_by('?').first(),
                period=random.choice(['1', '2', '3', '4', '5', '6', '7', '8']),
                staff=Staff.objects.order_by('?').first()
            )

        # Create 5 attendances
        for i in range(5):
            Attendance.objects.create(
                session=Session.objects.order_by('?').first(),
                subject=Subject.objects.order_by('?').first(),
                student=Student.objects.order_by('?').first(),
                date=timezone.now().date(),
                period=random.randint(1, 8),
                status=random.choice([True, False])
            )

        # Create 5 attendance reports
        for i in range(5):
            AttendanceReport.objects.create(
                student=Student.objects.order_by('?').first(),
                attendance=Attendance.objects.order_by('?').first(),
                status=random.choice([True, False])
            )

        # Create 5 assignment questions and answers
        for i in range(5):
            question = AssignmentQuestions.objects.create(
                uploaded_by=Staff.objects.order_by('?').first(),
                Class=Class.objects.order_by('?').first(),
                deadline_data=timezone.now(),
            )
            AssignmentAnswers.objects.create(
                assignment_question=question,
                student=Student.objects.order_by('?').first()
            )

        # Create 5 leave reports for students and staff
        for i in range(5):
            LeaveReportStudent.objects.create(
                student=Student.objects.order_by('?').first(),
                date=str(timezone.now().date()),
                message=f"Leave message {i+1}",
                status=random.randint(0, 1)
            )
            LeaveReportStaff.objects.create(
                staff=Staff.objects.order_by('?').first(),
                date=str(timezone.now().date()),
                message=f"Leave message {i+1}",
                status=random.randint(0, 1)
            )

        # Create 5 feedbacks for students and staff
        for i in range(5):
            FeedbackStudent.objects.create(
                student=Student.objects.order_by('?').first(),
                feedback=f"Feedback {i+1}",
                reply=f"Reply {i+1}"
            )
            FeedbackStaff.objects.create(
                staff=Staff.objects.order_by('?').first(),
                feedback=f"Feedback {i+1}",
                reply=f"Reply {i+1}"
            )

        # Create 5 notifications for students and staff
        for i in range(5):
            NotificationStudent.objects.create(
                student=Student.objects.order_by('?').first(),
                message=f"Notification {i+1}"
            )
            NotificationStaff.objects.create(
                staff=Staff.objects.order_by('?').first(),
                message=f"Notification {i+1}"
            )

        # Create 5 student results
        for i in range(5):
            StudentResult.objects.create(
                student=Student.objects.order_by('?').first(),
                subject=Subject.objects.order_by('?').first(),
                test=random.uniform(0, 100),
                exam=random.uniform(0, 100)
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
