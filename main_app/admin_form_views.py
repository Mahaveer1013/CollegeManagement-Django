from dal import autocomplete
from .models import *

class DepToClass(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ClassList.objects.none()

        class_list = ClassList.objects.all()

        department_id = self.forwarded.get('department', None)

        if department_id:
            class_list = class_list.filter(department_id=department_id)

        return class_list 
    
class ClassToSub(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Period.objects.none()

        class_list = Period.objects.all()

        class_name_id = self.forwarded.get('class_name', None)

        if class_name_id:
            class_list = class_list.filter(class_name_id=class_name_id)

        return class_list 
