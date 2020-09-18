"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from alluser_app import AlluserViews
from student_management_app import views, HodViews, StaffViews, StudentViews, AccountantViews
from student_management_system import settings


urlpatterns = [
    ### ALL user view  ################
    path("", AlluserViews.index, name="home"),
    path("courses", AlluserViews.courses, name="courses"),
    path("notice", AlluserViews.notice, name="notice"),
    path("contact", AlluserViews.contact, name="contactus"),
    path("view_result", AlluserViews.view_result, name="view_result"),
    path("match_result_data", AlluserViews.match_result_data, name="match_result_data"),
    path('neet_apply',AlluserViews.neet_apply,name="neet_apply"),
    path('neet_apply_save',AlluserViews.neet_apply_save,name="neet_apply_save"),
    

    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('login',views.ShowLoginPage,name="show_login"),
    

    path('get_students', StaffViews.get_students, name="get_students"),
    path('logout_user', views.logout_user,name="logout"),

    path('doLogin',views.doLogin,name="do_login"),
    #    $$$$$$$$$$$$$$$$$$ Admin URLS $$$$$$$$$$$
    path('admin_home',HodViews.admin_home,name="admin_home"),
    path('add_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('add_accountant',HodViews.add_accountant,name="add_accountant"),
    path('add_accountant_save',HodViews.add_accountant_save,name="add_accountant_save"),
    path('add_course', HodViews.add_course,name="add_course"),
    path('add_course_save', HodViews.add_course_save,name="add_course_save"),
    path('add_student', HodViews.add_student,name="add_student"),
    path('add_student_save', HodViews.add_student_save,name="add_student_save"),
    path('add_subject', HodViews.add_subject,name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save,name="add_subject_save"),
    path('manage_staff', HodViews.manage_staff,name="manage_staff"),
    path('manage_student', HodViews.manage_student,name="manage_student"),
    path('manage_course', HodViews.manage_course,name="manage_course"),
    path('manage_subject', HodViews.manage_subject,name="manage_subject"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff,name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<str:student_id>', HodViews.edit_student,name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save,name="edit_student_save"),
    path('edit_subject/<str:subject_id>', HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<str:course_id>', HodViews.edit_course,name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save,name="edit_course_save"),
    path('manage_session', HodViews.manage_session,name="manage_session"),
    path('add_session_save', HodViews.add_session_save,name="add_session_save"),
    path('check_email_exist', HodViews.check_email_exist,name="check_email_exist"),
    path('check_aaddhar_exist', HodViews.check_aaddhar_exist,name="check_aaddhar_exist"),
    path('check_username_exist', HodViews.check_username_exist,name="check_username_exist"),
    path('check_mobile_exist', HodViews.check_mobile_exist,name="check_mobile_exist"),
    path('student_feedback_message', HodViews.student_feedback_message,name="student_feedback_message"),
    path('student_feedback_message_replied', HodViews.student_feedback_message_replied,name="student_feedback_message_replied"),
    path('staff_feedback_message', HodViews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('student_leave_view', HodViews.student_leave_view,name="student_leave_view"),
    path('staff_leave_view', HodViews.staff_leave_view,name="staff_leave_view"),
    path('student_approve_leave/<str:leave_id>', HodViews.student_approve_leave,name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', HodViews.student_disapprove_leave,name="student_disapprove_leave"),
    path('staff_disapprove_leave/<str:leave_id>', HodViews.staff_disapprove_leave,name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', HodViews.staff_approve_leave,name="staff_approve_leave"),
    path('admin_view_attendance', HodViews.admin_view_attendance,name="admin_view_attendance"),
    path('admin_get_attendance_dates', HodViews.admin_get_attendance_dates,name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', HodViews.admin_get_attendance_student,name="admin_get_attendance_student"),
    path('admin_profile', HodViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', HodViews.admin_profile_save,name="admin_profile_save"),
    path('check_rollNumber_exist', HodViews.check_rollNumber_exist, name="check_rollNumber_exist"),
    path('fetch_rollNumber', HodViews.fetch_rollNumber, name="fetch_rollNumber"),
    path('add_students_result', HodViews.add_students_result,name="add_students_result"),
    path('save_students_result', HodViews.save_students_result,name="save_students_result"),
    path('view_neet_students', HodViews.view_neet_students,name="view_neet_students"),
    path('neet_student_pdf/<str:neet_id>', HodViews.neet_student_pdf.as_view(),name="neet_student_pdf"),
    path('delete_neet_student/<str:neet_id>', HodViews.delete_neet_student,name="delete_neet_student"),

                  #     Staff URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students', StaffViews.get_students, name="get_students"),
    path('get_attendance_dates', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data', StaffViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),
    # path('staff_add_result', StaffViews.staff_add_result, name="staff_add_result"),
    # path('save_student_result', StaffViews.save_student_result, name="save_student_result"),

        ################## Accountant Urls ################
    path('accountant_home', AccountantViews.accountant_home, name="accountant_home"),
    path('make_new_payment', AccountantViews.make_new_payment, name="make_new_payment"),
    path('make_new_payment_save', AccountantViews.make_new_payment_save, name="make_new_payment_save"),
    path('check_rollno_exist', AccountantViews.check_rollno_exist, name="check_rollno_exist"),
    path('fetch_rollno', AccountantViews.fetch_rollno, name="fetch_rollno"),
    path('payments_history', AccountantViews.payments_history, name="payments_history"),
    path('check_students_payments', AccountantViews.check_students_payments, name="check_students_payments"),
    path('student_payment_details/<str:student_id>', AccountantViews.student_payment_details, name="student_payment_details"),
    path('payment_reminder_mail/<str:student_id>', AccountantViews.payment_reminder_mail, name="payment_reminder_mail"),
    path('pay_remind_mailsend', AccountantViews.pay_remind_mailsend, name="pay_remind_mailsend"),
    path('notices', AccountantViews.notices, name="notices"),
    path('add_notice', AccountantViews.add_notice, name="add_notice"),
    path('add_notice_save', AccountantViews.add_notice_save, name="add_notice_save"),
    path('edit_notice/<str:notice_id>', AccountantViews.edit_notice,name="edit_notice"),
    path('edit_notice_save', AccountantViews.edit_notice_save,name="edit_notice_save"),
    path('delete_notice/<str:notice_id>', AccountantViews.delete_notice,name="delete_notice"),
    
    


    ################# Student URLS #################

    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('edit_student_photo', StudentViews.edit_student_photo, name="edit_student_photo"),
    path('student_photo_save', StudentViews.student_photo_save, name="student_photo_save"),
    path('student_profile_change', StudentViews.student_profile_change, name="student_profile_change"),
    path('student_profile_save_change', StudentViews.student_profile_save_change, name="student_profile_save_change"),
    path('student_payment_history', StudentViews.student_payment_history, name="student_payment_history"),
    path('download_transaction', StudentViews.GenerateTransactionPDF.as_view(),name="download_transaction"),
    
    
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
