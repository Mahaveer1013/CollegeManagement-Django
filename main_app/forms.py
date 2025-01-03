from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import ModelChoiceField
from dal import autocomplete
from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').user.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).user.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'gender',  'password', 'profile_pic', 'address']


class DateSelectionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    period = forms.ChoiceField(
        choices=[(i, f'Period {i}') for i in range(1, 9)], required=False)


class AttendanceSelectionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}))
    class_name = forms.ModelChoiceField(
        queryset=ClassList.objects.all().order_by(
            'department__name', 'semester', 'section'),
        empty_label="Select a class",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ResultViewForm(forms.Form):
    exam_type = forms.ModelChoiceField(
        queryset=ExamDetail.objects.filter(
            examresult__isnull=False).distinct(),
        empty_label="Select an Exam Type",
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'id_exam_type'}),
        required=True
    )
    class_name = forms.ModelChoiceField(
        queryset=ClassList.objects.all().order_by(
            'department__name', 'semester', 'section'),
        empty_label="Select a class",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class OverallAttendanceSelectionForm(forms.Form):
    from_date = forms.DateField(
        label='From :',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    to_date = forms.DateField(
        label='To :',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select a Department",
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'id_department'}),
        required=False
    )
    class_name = forms.ModelChoiceField(
        queryset=ClassList.objects.all().order_by(
            'department__name', 'semester', 'section'),
        empty_label="Select a class",
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'id_class_name'}),
        required=False
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        empty_label="Select Student",
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'id_student'}),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date:
            if from_date > to_date:
                raise ValidationError(
                    'From date must be less than to date and they should not be equal.')

        return cleaned_data

    def get_roll_number(self):
        student = self.cleaned_data.get('student')
        if student:
            return student.roll_number
        return None


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': False})
        self.fields['password'].initial = ''  # Ensure no initial value
        if 'email' in self.fields:
            del self.fields['email']

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = [field for field in CustomUserForm.Meta.fields if field != 'email']


class AttendanceForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'start_semester': DateInput(attrs={'type': 'date'}),
            'end_semester': DateInput(attrs={'type': 'date'}),
        }


# class ExamDetailForm(FormSettings):
class ExamDetailForm(FormSettings):
    semester_choices = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', '6th'),
        ('7', '7th'),
        ('8', '8th'),
    )
    exam_type_choices = (
        ('1', 'Internal Assesment 1'),
        ('2', 'Internal Assesment 2'),
        ('3', 'Semester Examination')
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'onchange': 'updateSubjects()'})
    )

    academic_year = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        empty_label="Select Subject"
    )

    semester = forms.ChoiceField(
        choices=semester_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    exam_type = forms.ChoiceField(
        choices=exam_type_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ExamDetail
        fields = ['department', 'subject', 'semester', 'exam_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year'].choices = [
            (year.id, year)
            for year in AcademicYear.objects.all()
        ]
        self.fields['department'].queryset = Department.objects.all()
        self.fields['subject'].queryset = Subject.objects.all()


class AssignmentAnswersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentAnswersForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AssignmentAnswers
        fields = ['pdf']
        widgets = {
            'pdf': forms.FileInput(attrs={'class': 'form-control'})
        }


class CertificateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CertificateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Certificate
        fields = ['title', 'description', 'certificate']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'certificate': forms.FileInput(attrs={'class': 'form-control'})
        }


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message', 'related_documents']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'related_documents': forms.FileInput(attrs={'class': 'form-control'})
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message', 'related_documents']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'related_documents': forms.FileInput(attrs={'class': 'form-control'})
        }


class FeedbackStudentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']


class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        # Remove the email field from the form
        if 'email' in self.fields:
            del self.fields['email']

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = [field for field in CustomUserForm.Meta.fields if field != 'email']


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)
        # Remove the email field from the form
        if 'email' in self.fields:
            del self.fields['email']

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = [field for field in CustomUserForm.Meta.fields if field != 'email']
