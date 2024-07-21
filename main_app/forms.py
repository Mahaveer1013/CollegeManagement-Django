from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import ModelChoiceField
from dal import autocomplete

from .models import *

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = '__all__'
        widgets = {
            'class_name': autocomplete.ModelSelect2(url='dep-to-class-autocomplete', forward=['department']),
            'monday_1': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'monday_2': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'monday_3': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'monday_4': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'monday_5': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'monday_6': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'monday_7': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'monday_8': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_1': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_2': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_3': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_4': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_5': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_6': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_7': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'tuesday_8': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_1': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_2': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_3': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_4': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_5': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_6': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_7': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'wednesday_8': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_1': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_2': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_3': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_4': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_5': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_6': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_7': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'thursday_8': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_1': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_2': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_3': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_4': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_5': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_6': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_7': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
            'friday_8': autocomplete.ModelSelect2(url='class-to-sub-autocomplete', forward=['class_name']),
        }


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
            instance = kwargs.get('instance').admin.__dict__
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
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'gender',  'password', 'profile_pic', 'address']


# class StudentForm(CustomUserForm):
#     def __init__(self, *args, **kwargs):
#         super(StudentForm, self).__init__(*args, **kwargs)

#     class Meta(CustomUserForm.Meta):
#         model = Student
#         fields = CustomUserForm.Meta.fields + \
#             ['department','register_number', 'roll_number']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': False})
        self.fields['password'].initial = ''  # Ensure no initial value

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


# class TimeTableForm(forms.ModelForm):
#     class Meta:
#         model = TimeTable
#         fields = [
#             'department', 'class_name',
#             'monday_1', 'monday_2', 'monday_3', 'monday_4', 'monday_5', 'monday_6', 'monday_7', 'monday_8',
#             'tuesday_1', 'tuesday_2', 'tuesday_3', 'tuesday_4', 'tuesday_5', 'tuesday_6', 'tuesday_7', 'tuesday_8',
#             'wednesday_1', 'wednesday_2', 'wednesday_3', 'wednesday_4', 'wednesday_5', 'wednesday_6', 'wednesday_7', 'wednesday_8',
#             'thursday_1', 'thursday_2', 'thursday_3', 'thursday_4', 'thursday_5', 'thursday_6', 'thursday_7', 'thursday_8',
#             'friday_1', 'friday_2', 'friday_3', 'friday_4', 'friday_5', 'friday_6', 'friday_7', 'friday_8',
#         ]

#     def __init__(self, *args, **kwargs):
#         super(TimeTableForm, self).__init__(*args, **kwargs)
#         self.fields['department'].widget.attrs.update({'class': 'form-control'})
#         self.fields['class_name'].widget.attrs.update({'class': 'form-control'})

#         days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
#         periods = range(1, 9)

#         for day in days:
#             for period in periods:
#                 field_name = f'{day}_{period}'
#                 self.fields[field_name].widget.attrs.update({'class': 'form-control'})


# class TimeTableForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(TimeTableForm, self).__init__(*args, **kwargs)
#     class Meta:
#         model = TimeTable
#         fields = ['department', 'Class', 'day', 'period', 'staff']
#         widgets = {
#             'department': forms.Select(attrs={'class': 'form-control'}),
#             'Class': forms.Select(attrs={'class': 'form-control'}),
#             'day': forms.Select(attrs={'class': 'form-control'}),
#             'period': forms.Select(attrs={'class': 'form-control'}),
#             'staff': forms.Select(attrs={'class': 'form-control'}),
#         }

# class TimeTableForm(FormSettings):
#     monday_1 = forms.ChoiceField(required=False)
#     monday_2 = forms.ChoiceField(required=False)
#     monday_3 = forms.ChoiceField(required=False)
#     monday_4 = forms.ChoiceField(required=False)
#     monday_5 = forms.ChoiceField(required=False)
#     monday_6 = forms.ChoiceField(required=False)
#     monday_7 = forms.ChoiceField(required=False)
#     monday_8 = forms.ChoiceField(required=False)

#     tuesday_1 = forms.ChoiceField(required=False)
#     tuesday_2 = forms.ChoiceField(required=False)
#     tuesday_3 = forms.ChoiceField(required=False)
#     tuesday_4 = forms.ChoiceField(required=False)
#     tuesday_5 = forms.ChoiceField(required=False)
#     tuesday_6 = forms.ChoiceField(required=False)
#     tuesday_7 = forms.ChoiceField(required=False)
#     tuesday_8 = forms.ChoiceField(required=False)

#     wednesday_1 = forms.ChoiceField(required=False)
#     wednesday_2 = forms.ChoiceField(required=False)
#     wednesday_3 = forms.ChoiceField(required=False)
#     wednesday_4 = forms.ChoiceField(required=False)
#     wednesday_5 = forms.ChoiceField(required=False)
#     wednesday_6 = forms.ChoiceField(required=False)
#     wednesday_7 = forms.ChoiceField(required=False)
#     wednesday_8 = forms.ChoiceField(required=False)

#     thursday_1 = forms.ChoiceField(required=False)
#     thursday_2 = forms.ChoiceField(required=False)
#     thursday_3 = forms.ChoiceField(required=False)
#     thursday_4 = forms.ChoiceField(required=False)
#     thursday_5 = forms.ChoiceField(required=False)
#     thursday_6 = forms.ChoiceField(required=False)
#     thursday_7 = forms.ChoiceField(required=False)
#     thursday_8 = forms.ChoiceField(required=False)

#     friday_1 = forms.ChoiceField(required=False)
#     friday_2 = forms.ChoiceField(required=False)
#     friday_3 = forms.ChoiceField(required=False)
#     friday_4 = forms.ChoiceField(required=False)
#     friday_5 = forms.ChoiceField(required=False)
#     friday_6 = forms.ChoiceField(required=False)
#     friday_7 = forms.ChoiceField(required=False)
#     friday_8 = forms.ChoiceField(required=False)

#     class Meta:
#         model = TimeTable
#         fields = ['department', 'Class']

#     def __init__(self, *args, **kwargs):
#         super(TimeTableForm, self).__init__(*args, **kwargs)
#         subjects = Subject.objects.all()
#         subject_choices = [(subject.id, subject.name) for subject in subjects]
#         subject_choices.insert(0, ('', 'Select Subject'))  # Add an empty option for default

#         # Setting choices for each period of each day
#         for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
#             for period in range(1, 9):
#                 self.fields[f'{day}_{period}'].choices = subject_choices

#     def clean(self):
#         cleaned_data = super().clean()
#         days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
#         timetable = {}

#         for day in days:
#             timetable[day] = []
#             for period in range(1, 9):
#                 period_data = cleaned_data.get(f'{day}_{period}')
#                 if period_data:
#                     timetable[day].append(int(period_data))
#                 else:
#                     timetable[day].append(None)
#         cleaned_data['timetable'] = timetable
#         return cleaned_data

#     def save(self, commit=True):
#         instance = super(TimeTableForm, self).save(commit=False)
#         instance.monday = self.cleaned_data['timetable']['monday']
#         instance.tuesday = self.cleaned_data['timetable']['tuesday']
#         instance.wednesday = self.cleaned_data['timetable']['wednesday']
#         instance.thursday = self.cleaned_data['timetable']['thursday']
#         instance.friday = self.cleaned_data['timetable']['friday']

#         if commit:
#             instance.save()
#         return instance

# class StaffForm(CustomUserForm):
#     def __init__(self, *args, **kwargs):
#         super(StaffForm, self).__init__(*args, **kwargs)

#     class Meta(CustomUserForm.Meta):
#         model = Staff
#         fields = CustomUserForm.Meta.fields + \
#             ['department']

# class DepartmentForm(FormSettings):
#     def __init__(self, *args, **kwargs):
#         super(DepartmentForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = Department
#         fields = ['name']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#         }

# class ClassListForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ClassListForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = ClassList
#         fields = ['department', 'semester', 'section']
#         widgets = {
#             'department': forms.Select(attrs={'class': 'form-control'}),
#             'semester': forms.Select(attrs={'class': 'form-control'}),
#             'section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Section'}),
#         }

# class SubjectForm(FormSettings):

#     def __init__(self, *args, **kwargs):
#         super(SubjectForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = Subject
#         fields = ['subject_code','name', 'staff', 'department']


# class SessionForm(FormSettings):
#     def __init__(self, *args, **kwargs):
#         super(SessionForm, self).__init__(*args, **kwargs)

#     class Meta:
#         model = Session
#         fields = '__all__'
#         widgets = {
#             'start_semester': DateInput(attrs={'type': 'date'}),
#             'end_semester': DateInput(attrs={'type': 'date'}),
#         }


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


class AssignmentQuestionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentQuestionsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AssignmentQuestions
        fields = ['class_name','deadline_date', 'pdf']
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'deadline_date': forms.DateInput(attrs={'class': 'form-control'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control'})
        }


class AssignmentAnswersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignmentAnswersForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AssignmentAnswers
        fields = ['pdf']
        widgets = {
            'pdf': forms.FileInput(attrs={'class': 'form-control'})
        }


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
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
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
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


