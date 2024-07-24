from django import forms
from django.contrib.auth import get_user_model
from .models import *
from dal import autocomplete

User = get_user_model()


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name',
                  'user_type', 'gender', 'profile_pic', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.pk:  # If the user is being created (not updated)
            # Set the email as the password
            user.password = make_password(user.email)
        if commit:
            user.save()
        return user


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = '__all__'
        widgets = {
            'class_name': autocomplete.ModelSelect2(url='dep-to-class-autocomplete', forward=['department'])
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        linked_student_users = Student.objects.values_list(
            'admin_id', flat=True)
        linked_staff_users = Staff.objects.values_list('admin_id', flat=True)
        # Combine both sets of linked users
        linked_users = set(linked_student_users).union(set(linked_staff_users))
        # Exclude those users from the options in the admin field
        self.fields['admin'].queryset = CustomUser.objects.exclude(
            id__in=linked_users
        ).exclude(user_type='3').exclude(user_type='1')
        if self.instance.pk:
            self.fields['admin'].disabled = True


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'class_name': autocomplete.ModelSelect2(url='dep-to-class-autocomplete', forward=['department']),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        linked_student_users = Student.objects.values_list(
            'admin_id', flat=True)
        linked_staff_users = Staff.objects.values_list('admin_id', flat=True)
        # Combine both sets of linked users
        linked_users = set(linked_student_users).union(set(linked_staff_users))
        # Exclude those users from the options in the admin field
        self.fields['admin'].queryset = CustomUser.objects.exclude(
            id__in=linked_users).exclude(user_type='2').exclude(user_type='1')
        if self.instance.pk:  # Check if this is an editing operation
            if 'admin' in self.fields:
                del self.fields['admin']


class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = '__all__'
        widgets = {
            'class_name': autocomplete.ModelSelect2(url='timetable-dep-to-class-autocomplete', forward=['department']),
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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     assigned_class = TimeTable.objects.values_list('class_name', flat=True)
    #     self.fields['class_name'].queryset = TimeTable.objects.exclude(
    #         class_name__in=assigned_class)

    #     # Check if an instance is being updated
    #     if self.instance.pk:
    #         timetable = TimeTable.objects.get(pk=self.instance.pk)
    #         assigned_staff = {
    #             period.staff for period in [
    #                 timetable.monday_1, timetable.monday_2, timetable.monday_3, timetable.monday_4,
    #                 timetable.monday_5, timetable.monday_6, timetable.monday_7, timetable.monday_8,
    #                 timetable.tuesday_1, timetable.tuesday_2, timetable.tuesday_3, timetable.tuesday_4,
    #                 timetable.tuesday_5, timetable.tuesday_6, timetable.tuesday_7, timetable.tuesday_8,
    #                 timetable.wednesday_1, timetable.wednesday_2, timetable.wednesday_3, timetable.wednesday_4,
    #                 timetable.wednesday_5, timetable.wednesday_6, timetable.wednesday_7, timetable.wednesday_8,
    #                 timetable.thursday_1, timetable.thursday_2, timetable.thursday_3, timetable.thursday_4,
    #                 timetable.thursday_5, timetable.thursday_6, timetable.thursday_7, timetable.thursday_8,
    #                 timetable.friday_1, timetable.friday_2, timetable.friday_3, timetable.friday_4,
    #                 timetable.friday_5, timetable.friday_6, timetable.friday_7, timetable.friday_8
    #             ]
    #             if period.staff
    #         }

    #         # Filter staff options to exclude those already assigned to columns
    #         for field_name in self.fields:
    #             if field_name.endswith('_staff'):
    #                 self.fields[field_name].queryset = Staff.objects.exclude(id__in=assigned_staff)
