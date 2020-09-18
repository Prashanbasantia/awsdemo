from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)        
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "student_management_app.HodViews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "student_management_app.StaffViews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                if modulename == "student_management_app.StudentViews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static" or  modulename == "alluser_app.AlluserViews":
                    pass
                else:
                    return HttpResponseRedirect(reverse("home"))
            elif user.user_type == "4":
                if modulename == "student_management_app.AccountantViews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("accountant_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login") or modulename == "alluser_app.AlluserViews" or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("home"))