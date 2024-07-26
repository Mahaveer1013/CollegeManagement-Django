from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *
from .admin_forms import *


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    form = TimeTableForm


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    form = PeriodForm


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffForm
    list_display = ['admin','department','resume']
    search_fields = ()
    ordering = ()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ['admin','department', 'class_name', 'academic_year']
    search_fields = ('register_number','roll_number')
    ordering = ('register_number',)

@admin.register(AssignmentQuestion)
class AssignmentQuestionsAdmin(admin.ModelAdmin):
    # Hide the 'uploaded_by' field in the admin form
    exclude = ('uploaded_by',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        staff_member = Staff.objects.filter(admin=request.user).first()
        if staff_member:
            # Filter class_name to show only the classes where the staff is a subject teacher
            periods = Period.objects.filter(staff=staff_member).values_list(
                'class_name', flat=True).distinct()
            form.base_fields['class_name'].queryset = ClassList.objects.filter(
                id__in=periods)
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(uploaded_by=request.user)


@admin.register(Notice)
class NoticesAdmin(admin.ModelAdmin):
    exclude = ('uploaded_by',)
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    add_form = CustomUserForm
    model = CustomUser

    list_display = ['email', 'first_name', 'last_name', 'user_type', 'gender']
    list_filter = ['user_type', 'gender']
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name',
         'user_type', 'gender', 'profile_pic', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'gender', 'profile_pic', 'address')}
         ),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm

    exclude = [
        'bloom_level1', 'bloom_level2', 'bloom_level3', 'bloom_level4',
        'bloom_level5', 'bloom_level6', 'bloom_level7', 'bloom_level8',
        'bloom_level9', 'bloom_level10', 'bloom_level11', 'bloom_level12',
        'bloom_level13', 'bloom_level14', 'bloom_level15', 'bloom_level16',
        'bloom_level17', 'bloom_level18', 'bloom_level19', 'bloom_level20',
        'bloom_level21', 'bloom_level22'
    ]

    def save_model(self, request, obj, form, change):
        # Update Bloom levels based on question text
        if not change:  # If creating a new Question
            for i in range(1, 23):
                question_text = getattr(obj, f'question_text{i}')
                if question_text:
                    words = question_text.split()
                    bloom_level = None

                    for word in words:
                        word = word.strip()
                        if word:
                            bloom_keyword = BloomKeyword.objects.filter(
                                word__iexact=word).first()
                            print(bloom_keyword)
                            if bloom_keyword.bloom_level==1:
                                bloom_level = 'Creating'
                                break
                            if bloom_keyword.bloom_level==2:
                                bloom_level = 'Evaluate'
                                break
                            if bloom_keyword.bloom_level==3:
                                bloom_level = 'Analyzing'
                                break
                            if bloom_keyword.bloom_level==4:
                                bloom_level = 'Applying'
                                break
                            if bloom_keyword.bloom_level==5:
                                bloom_level = 'Understanding'
                                break
                            if bloom_keyword.bloom_level==6:
                                bloom_level = 'Remember'
                                break

                    setattr(obj, f'bloom_level{i}', bloom_level)

        super().save_model(request, obj, form, change)


@admin.register(Note)
class NotesAdmin(admin.ModelAdmin):
    # Hide the 'uploaded_by' field in the admin form
    exclude = ('uploaded_by',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created (and not updated)
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


from django.contrib import admin
from .models import AdminAccessLog

@admin.register(AdminAccessLog)
class AdminAccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'accessed_at')
    list_filter = ('accessed_at',)
    search_fields = ('user__username', 'ip_address')

admin.site.register(ExamDetail)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(AcademicYear)
admin.site.register(ClassList)
