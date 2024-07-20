# from django.contrib import admin
# from .models import *
# # from .admin_forms import *
# from .forms import *

# class CustomUserAdmin(admin.ModelAdmin):
#     form = CustomUserForm

# class StudentAdmin(admin.ModelAdmin):
#     form = StudentForm

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "admin":
#             kwargs["queryset"] = CustomUser.objects.filter(
#                 is_staff=False,
#                 is_superuser=False
#             ).exclude(
#                 id__in=Student.objects.values_list('admin_id', flat=True)
#             ).exclude(
#                 id__in=Admin.objects.values_list('admin_id', flat=True)
#             )
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

# class HODAdmin(admin.ModelAdmin):
#     form = AdminForm

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "admin":
#             kwargs["queryset"] = CustomUser.objects.filter(
#                 is_staff=False,
#                 is_superuser=False
#             ).exclude(
#                 id__in=Student.objects.values_list('admin_id', flat=True)
#             ).exclude(
#                 id__in=Admin.objects.values_list('admin_id', flat=True)
#             )
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

# class StaffAdmin(admin.ModelAdmin):
    # form = StaffForm

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "admin":
    #         kwargs["queryset"] = CustomUser.objects.filter(
    #             is_staff=False,
    #             is_superuser=False
    #         ).exclude(
    #             id__in=Student.objects.values_list('admin_id', flat=True)
    #         ).exclude(
    #             id__in=Staff.objects.values_list('admin_id', flat=True)
    #         )
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)