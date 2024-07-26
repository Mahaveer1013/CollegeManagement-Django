from .models import AdminAccessLog
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?
        if user.is_authenticated:
            if user.user_type == '1':  # Is it the HOD/Admin
                if modulename == 'main_app.student_views':
                    return redirect(reverse('admin_home'))
            elif user.user_type == '2':  # Staff :-/ ?
                if modulename == 'main_app.student_views' or modulename == 'main_app.hod_views':
                    return redirect(reverse('staff_home'))
            elif user.user_type == '3':  # ... or Student ?
                if modulename == 'main_app.hod_views' or modulename == 'main_app.staff_views':
                    return redirect(reverse('student_home'))
            else:  # None of the aforementioned ? Please take the user to login page
                return redirect(reverse('login_page'))
        else:
            # If the path is login or has anything to do with authentication, pass
            if request.path == reverse('login_page') or modulename == 'django.contrib.auth.views' or request.path == reverse('user_login'):
                pass
            else:
                return redirect(reverse('login_page'))



class AdminAccessLogMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print(request.META)
        if request.path == reverse('user_login') and request.user.is_authenticated:
            user = request.user
            ip_address = request.META.get('REMOTE_ADDR')

            # Log the access
            AdminAccessLog.objects.create(
                user=user,
                ip_address=ip_address,
                accessed_at=timezone.now()
            )
        return response
