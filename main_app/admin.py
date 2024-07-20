from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .admin_models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(ClassList)
admin.site.register(TimeTable)
admin.site.register(QpKeyword)
admin.site.register(QuestionPaper)
admin.site.register(AssignmentQuestions)
admin.site.register(AssignmentAnswers)
admin.site.register(CustomUser)
