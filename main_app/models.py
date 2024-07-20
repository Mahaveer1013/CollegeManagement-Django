from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_migrate


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
    USER_TYPE = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    GENDER = [("M", "Male"), ("F", "Female")]
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
        return self.first_name + self.last_name


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Department(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Class(models.Model):
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
        Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    semester = models.CharField(max_length=1, choices=SEM_CHOICES)
    section = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.department} - {self.get_sem_display()} sem - Section {self.section}"


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    Class = models.ForeignKey(Class, on_delete=models.DO_NOTHING, null=True)
    register_number = models.CharField(max_length=100, unique=True)
    roll_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.admin.first_name + self.admin.last_name


class Staff(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, null=True, blank=False)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.first_name + self.admin.last_name


class Subject(models.Model):
    name = models.CharField(max_length=120)
    subject_code = models.CharField(max_length=10, unique=True, default=None)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    monday_1 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_1')
    monday_2 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_2')
    monday_3 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_3')
    monday_4 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_4')
    monday_5 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_5')
    monday_6 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_6')
    monday_7 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_7')
    monday_8 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='monday_8')
    tuesday_1 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_1')
    tuesday_2 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_2')
    tuesday_3 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_3')
    tuesday_4 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_4')
    tuesday_5 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_5')
    tuesday_6 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_6')
    tuesday_7 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_7')
    tuesday_8 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='tuesday_8')
    wednesday_1 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_1')
    wednesday_2 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_2')
    wednesday_3 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_3')
    wednesday_4 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_4')
    wednesday_5 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_5')
    wednesday_6 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_6')
    wednesday_7 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_7')
    wednesday_8 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='wednesday_8')
    thursday_1 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_1')
    thursday_2 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_2')
    thursday_3 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_3')
    thursday_4 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_4')
    thursday_5 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_5')
    thursday_6 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_6')
    thursday_7 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_7')
    thursday_8 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='thursday_8')
    friday_1 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_1')
    friday_2 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_2')
    friday_3 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_3')
    friday_4 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_4')
    friday_5 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_5')
    friday_6 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_6')
    friday_7 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_7')
    friday_8 = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name='friday_8')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department} - {self.Class} - {self.day} - {self.get_period_display()}"


class Attendance(models.Model):
    # session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    date = models.DateField()
    period = models.IntegerField(default=None)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssignmentQuestions(models.Model):
    uploaded_by = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    pdf = models.FileField(
        upload_to='assignments/answers/', null=True, blank=True)
    deadline_data = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssignmentAnswers(models.Model):
    assignment_question = models.ForeignKey(
        AssignmentQuestions, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    pdf = models.FileField(upload_to='assignments/', null=True, blank=True)
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

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "1":
            Admin.objects.create(admin=instance)
        elif instance.user_type == "2":
            if Student.objects.filter(admin=instance).exists():
                raise ValidationError("This user is already a student.")
            Staff.objects.create(admin=instance)
        elif instance.user_type == "3":
            if Staff.objects.filter(admin=instance).exists():
                raise ValidationError("This user is already a staff member.")
            Student.objects.create(admin=instance)
