from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


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

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"


class Staff(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

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
        return self.word+' - ' + self.bloom_level


class Examdetail(models.Model):
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
    EXAM_TYPE = (
        ('1', 'Internal Assesment 1'),
        ('2', 'Internal Assesment 2'),
        ('3', 'Semester Examination')
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    added_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=False)
    semester = models.CharField(max_length=1, choices=SEM_CHOICES)
    exam_date = models.DateField()
    exam_type = models.CharField(max_length=1, choices=EXAM_TYPE)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=False)
    academic_year = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    QUESTION_MARK = (
        ('1', '2 Mark'),
        ('2', '13 Mark'),
        ('3', '15 mark')
    )
    exam_detail = models.ForeignKey(Examdetail, on_delete=models.CASCADE)
    question_text = models.TextField()
    unit_no = models.IntegerField()
    mark = models.CharField(max_length=1, choices=QUESTION_MARK)
    course_outcome = models.CharField(max_length=10)
    bloom_level = models.CharField(max_length=50)


class AssignmentQuestions(models.Model):
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    class_name = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='assignments/questions')
    deadline_date = models.DateTimeField()
    subject = models.ForeignKey(Period, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} - {self.uploaded_by}"


class AssignmentAnswers(models.Model):
    assignment_question = models.ForeignKey(
        AssignmentQuestions, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pdf = models.FileField(
        upload_to='assignments/answers', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
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
