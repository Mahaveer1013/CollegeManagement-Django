from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.core.exceptions import ValidationError
from django.forms import ModelForm

User = get_user_model()

# class StudentAdminForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['admin'].queryset = User.objects.filter(
#             is_staff=False,
#             is_superuser=False
#         ).exclude(
#             id__in=Staff.objects.values_list('admin_id', flat=True)
#         ).exclude(
#             id__in=Student.objects.values_list('admin_id', flat=True)
#         )


# class StaffAdminForm(forms.ModelForm):
#     class Meta:
#         model = Staff
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['admin'].queryset = User.objects.filter(
#             is_staff=False,
#             is_superuser=False
#         ).exclude(
#             id__in=Student.objects.values_list('admin_id', flat=True)
#         ).exclude(
#             id__in=Staff.objects.values_list('admin_id', flat=True)
#         )


#         class FormSettings(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(FormSettings, self).__init__(*args, **kwargs)
#         for field in self.visible_fields():
#             field.field.widget.attrs['class'] = 'form-control'


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender', 'password', 'profile_pic', 'address']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in self.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self):
        form_email = self.cleaned_data['email'].lower()
        if self.instance.pk is None:
            if CustomUser.objects.filter(email=form_email).exists():
                raise ValidationError("The given email is already registered")
        else:
            db_email = self.Meta.model.objects.get(id=self.instance.pk).admin.email.lower()
            if db_email != form_email:
                if CustomUser.objects.filter(email=form_email).exists():
                    raise ValidationError("The given email is already registered")
        return form_email


class StudentForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + ['department', 'register_number', 'roll_number']


class AdminForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields

class StaffForm(CustomUserForm):
    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + ['department']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']