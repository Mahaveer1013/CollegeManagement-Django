from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _


def create_default_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(email="admin@gmail.com").exists():
        User.objects.create_superuser(email="admin@gmail.com", password="1013")
        print("Default superuser created with email: admin@gmail.com and password: 1013")


post_migrate.connect(create_default_superuser)


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = (("1", "HOD"), ("2", "Staff"), ("3", "Student"))
    GENDER = [("M", "Male"), ("F", "Female")]
    username = None  # Removed username, using email instead
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField()
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class AcademicYear(models.Model):
    academic_year_start = models.IntegerField()
    academic_year_end = models.IntegerField()

    def clean(self):
        super().clean()

        # Ensure both years are four digits
        if not (1000 <= self.academic_year_start <= 9999):
            raise ValidationError(
                _('Academic year start must be a four-digit number.'))
        if not (1000 <= self.academic_year_end <= 9999):
            raise ValidationError(
                _('Academic year end must be a four-digit number.'))

        # Ensure the academic year end is after the start
        if self.academic_year_end <= self.academic_year_start:
            raise ValidationError(
                _('Academic year end must be after the start year.'))

        # Ensure the academic year end is exactly one year after the start
        if self.academic_year_end != self.academic_year_start + 4:
            raise ValidationError(
                _('Academic year end must be exactly four years after the start year.'))

    def __str__(self):
        return f"{self.academic_year_start}-{self.academic_year_end}"


class Department(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    SEM_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', '6th'),
        ('7', '7th'),
        ('8', '8th'),
    )

    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    semester = models.CharField(max_length=1, choices=SEM_CHOICES)
    section = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.department} - {self.get_semester_display()} sem - {self.section} Section"


class Subject(models.Model):
    name = models.CharField(max_length=120)
    # department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default='fb ')
    subject_code = models.CharField(max_length=10, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(
        ClassList, on_delete=models.SET_NULL, null=True)
    register_number = models.CharField(max_length=100, unique=True)
    roll_number = models.CharField(max_length=100, unique=True)
    dob = models.DateField(null=True, default=None)
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"


class Staff(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # faculty_id = models.CharField(max_length=100, unique=True)
    resume = models.FileField(upload_to='staff/resume',null=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"


class Period(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(
        ClassList, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.class_name} - {self.subject}"


class TimeTable(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    class_name = models.ForeignKey(
        ClassList, on_delete=models.SET_NULL, null=True)
    monday_1 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_1')
    monday_2 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_2')
    monday_3 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_3')
    monday_4 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_4')
    monday_5 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_5')
    monday_6 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_6')
    monday_7 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_7')
    monday_8 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='monday_8')
    tuesday_1 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_1')
    tuesday_2 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_2')
    tuesday_3 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_3')
    tuesday_4 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_4')
    tuesday_5 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_5')
    tuesday_6 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_6')
    tuesday_7 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_7')
    tuesday_8 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='tuesday_8')
    wednesday_1 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_1')
    wednesday_2 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_2')
    wednesday_3 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_3')
    wednesday_4 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_4')
    wednesday_5 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_5')
    wednesday_6 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_6')
    wednesday_7 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_7')
    wednesday_8 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='wednesday_8')
    thursday_1 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_1')
    thursday_2 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_2')
    thursday_3 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_3')
    thursday_4 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_4')
    thursday_5 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_5')
    thursday_6 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_6')
    thursday_7 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_7')
    thursday_8 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='thursday_8')
    friday_1 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_1')
    friday_2 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_2')
    friday_3 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_3')
    friday_4 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_4')
    friday_5 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_5')
    friday_6 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_6')
    friday_7 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_7')
    friday_8 = models.ForeignKey(
        Period, on_delete=models.CASCADE, related_name='friday_8')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.class_name} Timetable"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Define fields to update in the staff model
        period_fields = [
            ('monday_1', 'monday_1'),
            ('monday_2', 'monday_2'),
            ('monday_3', 'monday_3'),
            ('monday_4', 'monday_4'),
            ('monday_5', 'monday_5'),
            ('monday_6', 'monday_6'),
            ('monday_7', 'monday_7'),
            ('monday_8', 'monday_8'),
            ('tuesday_1', 'tuesday_1'),
            ('tuesday_2', 'tuesday_2'),
            ('tuesday_3', 'tuesday_3'),
            ('tuesday_4', 'tuesday_4'),
            ('tuesday_5', 'tuesday_5'),
            ('tuesday_6', 'tuesday_6'),
            ('tuesday_7', 'tuesday_7'),
            ('tuesday_8', 'tuesday_8'),
            ('wednesday_1', 'wednesday_1'),
            ('wednesday_2', 'wednesday_2'),
            ('wednesday_3', 'wednesday_3'),
            ('wednesday_4', 'wednesday_4'),
            ('wednesday_5', 'wednesday_5'),
            ('wednesday_6', 'wednesday_6'),
            ('wednesday_7', 'wednesday_7'),
            ('wednesday_8', 'wednesday_8'),
            ('thursday_1', 'thursday_1'),
            ('thursday_2', 'thursday_2'),
            ('thursday_3', 'thursday_3'),
            ('thursday_4', 'thursday_4'),
            ('thursday_5', 'thursday_5'),
            ('thursday_6', 'thursday_6'),
            ('thursday_7', 'thursday_7'),
            ('thursday_8', 'thursday_8'),
            ('friday_1', 'friday_1'),
            ('friday_2', 'friday_2'),
            ('friday_3', 'friday_3'),
            ('friday_4', 'friday_4'),
            ('friday_5', 'friday_5'),
            ('friday_6', 'friday_6'),
            ('friday_7', 'friday_7'),
            ('friday_8', 'friday_8'),
        ]

        # Iterate over each field and update the corresponding Staff instance
        for timetable_field, period_field in period_fields:
            period = getattr(self, timetable_field)
            if period:
                staff = period.staff
                if staff:
                    setattr(staff, period_field, period.class_name)
                    staff.save()


class Attendance(models.Model):

    STATUS_CHOICES = [
        (0, 'Absent'),
        (1, 'Present'),
        (2, 'On Duty Internal'),
        (3, 'On Duty External'),
        (4, 'Pending')
    ]

    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, related_name='attendances')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    period = models.PositiveIntegerField()  # Ensure this is a positive integer
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=4)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure unique records
        unique_together = ('student', 'date', 'period')
        indexes = [
            # Indexes for faster querying
            models.Index(fields=['student', 'date']),
        ]

    def clean(self):
        super().clean()
        if not (1 <= self.period <= 8):
            raise ValidationError('Period must be between 1 and 8.')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date} - Period {self.period} - {self.get_status_display()}"


class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BloomKeyword(models.Model):
    BLOOM_CHOICES = (
        ('1', 'Creating'),
        ('2', 'Evaluate'),
        ('3', 'Analyzing'),
        ('4', 'Applying'),
        ('5', 'Understanding'),
        ('6', 'Remember'),
    )
    word = models.CharField(max_length=120)
    bloom_level = models.CharField(max_length=1, choices=BLOOM_CHOICES)

    def __str__(self):
        return self.get_bloom_choices_display()


class ExamDetail(models.Model):
    SEM_CHOICES = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
        ('6th', '6th'),
        ('7th', '7th'),
        ('8th', '8th'),
    )

    EXAM_TYPE = (
        ('1', 'Internal Assesment 1'),
        ('2', 'Internal Assesment 2'),
        ('3', 'Semester Examination')
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=False)
    semester = models.CharField(max_length=3, choices=SEM_CHOICES)
    exam_date = models.DateField()
    exam_type = models.CharField(max_length=1, choices=EXAM_TYPE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=False)
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.SET_NULL, null=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.semester} sem - {self.get_exam_type_display()} - {self.subject} - ({self.academic_year})"


class Question(models.Model):
    QUESTION_MARK = (
        ('1', '2 Mark'),
        ('2', '13 Mark'),
    )
    UNIT_CHOICES = (
        ('1', '1st Unit'),
        ('2', '2nd Unit'),
        ('3', '3rd Unit'),
        ('4', '4th Unit'),
        ('5', '5th Unit'),
    )
    CO_LEVEL_CHOICES = (
        ('1', 'CO1'),
        ('2', 'CO2'),
        ('3', 'CO3'),
        ('4', 'CO4'),
        ('5', 'CO5'),
    )
    exam_detail = models.ForeignKey(ExamDetail, on_delete=models.CASCADE)
    question_text1 = models.TextField(default=None, null=True)
    unit_no1 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome1 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level1 = models.CharField(max_length=50, default=None, null=True)
    question_text2 = models.TextField(default=None, null=True)
    unit_no2 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome2 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level2 = models.CharField(max_length=50, default=None, null=True)
    question_text3 = models.TextField(default=None, null=True)
    unit_no3 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome3 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level3 = models.CharField(max_length=50, default=None, null=True)
    question_text4 = models.TextField(default=None, null=True)
    unit_no4 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome4 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level4 = models.CharField(max_length=50, default=None, null=True)
    question_text5 = models.TextField(default=None, null=True)
    unit_no5 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome5 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level5 = models.CharField(max_length=50, default=None, null=True)
    question_text6 = models.TextField(default=None, null=True)
    unit_no6 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome6 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level6 = models.CharField(max_length=50, default=None, null=True)
    question_text7 = models.TextField(default=None, null=True)
    unit_no7 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome7 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level7 = models.CharField(max_length=50, default=None, null=True)
    question_text8 = models.TextField(default=None, null=True)
    unit_no8 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome8 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level8 = models.CharField(max_length=50, default=None, null=True)
    question_text9 = models.TextField(default=None, null=True)
    unit_no9 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome9 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level9 = models.CharField(max_length=50, default=None, null=True)
    question_text10 = models.TextField(default=None, null=True)
    unit_no10 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome10 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level10 = models.CharField(max_length=50, default=None, null=True)
    question_text11 = models.TextField(default=None, null=True)
    unit_no11 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome11 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level11 = models.CharField(max_length=50, default=None, null=True)
    question_text12 = models.TextField(default=None, null=True)
    unit_no12 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome12 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level12 = models.CharField(max_length=50, default=None, null=True)
    question_text13 = models.TextField(default=None, null=True)
    unit_no13 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome13 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level13 = models.CharField(max_length=50, default=None, null=True)
    question_text14 = models.TextField(default=None, null=True)
    unit_no14 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome14 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level14 = models.CharField(max_length=50, default=None, null=True)
    question_text15 = models.TextField(default=None, null=True)
    unit_no15 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome15 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level15 = models.CharField(max_length=50, default=None, null=True)
    question_text16 = models.TextField(default=None, null=True)
    unit_no16 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome16 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level16 = models.CharField(max_length=50, default=None, null=True)
    question_text17 = models.TextField(default=None, null=True)
    unit_no17 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome17 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level17 = models.CharField(max_length=50, default=None, null=True)
    question_text18 = models.TextField(default=None, null=True)
    unit_no18 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome18 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level18 = models.CharField(max_length=50, default=None, null=True)
    question_text19 = models.TextField(default=None, null=True)
    unit_no19 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome19 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level19 = models.CharField(max_length=50, default=None, null=True)
    question_text20 = models.TextField(default=None, null=True)
    unit_no20 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome20 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level20 = models.CharField(max_length=50, default=None, null=True)
    question_text21 = models.TextField(default=None, null=True)
    unit_no21 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome21 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level21 = models.CharField(max_length=50, default=None, null=True)
    question_text22 = models.TextField(default=None, null=True)
    unit_no22 = models.CharField(
        max_length=1, choices=UNIT_CHOICES, default=None, null=True)
    course_outcome22 = models.CharField(
        max_length=10, choices=CO_LEVEL_CHOICES, default=1)
    bloom_level22 = models.CharField(max_length=50, default=None, null=True)

    def __str__(self):
        return f"{self.exam_detail} - Questions"


class AssignmentQuestion(models.Model):
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    class_name = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    name=models.CharField(max_length=40,default='Unit 1 Assignment')
    pdf = models.FileField(upload_to='assignments/questions')
    deadline_date = models.DateTimeField()
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} - {self.uploaded_by}"


class AssignmentAnswers(models.Model):
    assignment_question = models.ForeignKey(
        AssignmentQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pdf = models.FileField(
        upload_to='assignments/answers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Note(models.Model):
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    pdf = models.FileField(upload_to='notes')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    deadline_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.department} - {self.subject} - {self.name}"


class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    related_documentz = models.FileField(upload_to='leave/student', default=None, null=True)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()

    related_documents = models.FileField(upload_to='leave/staff', default=None, null=True)
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test = models.FloatField(default=0)
    exam = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AdminAccessLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField()
    accessed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.ip_address} - {self.accessed_at}"
    

class Notice(models.Model):
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, default=None)
    pdf = models.FileField(upload_to='notice')
    name = models.CharField(max_length=40)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def _str_(self):
        return f"{self.department} - {self.subject} - {self.name}"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
