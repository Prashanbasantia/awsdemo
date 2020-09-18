import datetime
import os
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from student_management_app.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, \
    LeaveReportStudent, FeedBackStudent, Transaction,SessionYearModel,Otp
from django.views.generic import View

#generate pdf
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class GenerateTransactionPDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('accountant_template/invoice.html')
        student=request.user.username
        transaction_select = request.GET.get('transaction_select')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        if transaction_select == 'all':
            transac = Transaction.objects.all().filter(roll_number=student).order_by('-id')
            pay_tran="All Payments Transaction"
        elif transaction_select == 'custome':
            transac = Transaction.objects.all().filter(roll_number=student,created_at__gte=from_date,created_at__lte=to_date).order_by('-id')
            pay_tran="Transaction From: {} To: {}".format(from_date,to_date)
        else:
            messages.error(request, "Please Select any Option")
            return HttpResponseRedirect(reverse("student_payment_history"))

        context = {
           "transac":transac,
           'pay_tran':pay_tran 
        }
        html = template.render(context)
        pdf = render_to_pdf('accountant_template/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "NAME_Payments_invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=student_obj.course_id.id)
    subjects=Subjects.objects.filter(course_id=course).count()

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance=Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"student_template/student_home_template.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent})

def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_apply_leave(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request,"alluser_template/student_apply_leave.html",{"leave_data":leave_data})

def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
def edit_student_photo(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"alluser_template/change_profile_modal.html",{"user":user,"student":student})

def student_photo_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        if request.FILES.get('profile_photo'):
            profile_photo=request.FILES['profile_photo']
            fs=FileSystemStorage()
            filename=fs.save(profile_photo.name,profile_photo)
            profile_pic_url=fs.url(filename)
        else:
            profile_pic_url=None
        try:
            old_pic = customuser.profile_photo
            if old_pic != profile_pic_url and profile_pic_url !=None:
                old_pic = str(old_pic)[7:]
                os.remove(os.path.join(settings.MEDIA_ROOT,old_pic))
            if profile_pic_url == None:
                customuser.profile_photo = old_pic
                customuser.save()
            else:
                customuser.profile_photo = profile_pic_url
                customuser.save()

            
        
            messages.success(request,"Successfully Profile Picture Changed ")
            return HttpResponseRedirect(reverse("student_profile"))
        except Exception as e:
            print('photo eror',e)
            messages.error(request,"Failed to Change Profile Picture")
            return HttpResponseRedirect(reverse("student_profile"))
        else:
            # cu=CustomUser.objects.get(id=request.user.id)
            # old_pic = cu.profile_photo
            # print(settings.BASE_DIR + old_pic)
            # print("after remove",old_pic)
            print("hiiiiiiiiiiiiiiiiiii")

           
def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    course = Courses.objects.get(id=student.course_id_id).course_name
    session_year = SessionYearModel.object.get(id =student.session_year_id_id)
    context = {
        "user":user,
        "student":student,
        "course":course,
        "session_year":session_year
        }
    return render(request,"alluser_template/setting.html",context)

def student_profile_change(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password=request.POST.get("password")
        address=request.POST.get("address")
        ot_msg=random.randint(000000,999999)
        old_time =timezone.now() + timedelta(minutes=3)
        Otp.objects.filter(updated_at__lte=old_time).delete()
        send_mail(
                'Nabapravat! Confirmation OTP for Chnage Password or Other Details',
                "this is your OTP :"+str(ot_msg) ,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
                ) 

        otp = Otp(otp_code = ot_msg,student_id=request.user.id)
        otp.save()
        context={
           'email':email,
           'phone':phone,
           'password':password,
           'address':address
        }
        return render(request,"alluser_template/student_otp.html",context)
def student_profile_save_change(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        email=request.POST.get("otp_email")
        phone=request.POST.get("otp_phone")
        password=request.POST.get("otp_password")
        address=request.POST.get("otp_address")
        re_otp = request.POST.get("re_otp")
        
        try:
            tp = Otp.objects.get(student_id=request.user.id).otp_code
            if re_otp == str(tp):
                customuser=CustomUser.objects.get(id=request.user.id)
                customuser.email=email
                student=Students.objects.get(admin=customuser)
                student.mobile=phone
                student.address=address
                student.save()
                if password!=None and password!="" :
                    customuser.set_password(password)
                customuser.save()
                otp = Otp.objects.get(student_id=request.user.id).delete()
                messages.success(request, "Successfully Saved ")
                print('valid otp')
                return HttpResponseRedirect(reverse("student_profile"))
            else:
                messages.error(request, "invalid to OTP")
                print('invalid otp')
                return HttpResponseRedirect(reverse("student_profile")) 

                
        except:
            messages.error(request, "Failed to Save")
            return HttpResponseRedirect(reverse("student_profile"))    
                
            

            
def student_payment_history(request):
    user=CustomUser.objects.get(id=request.user.id)
    st_id =user.id 
    tot = 0
    if request.GET.get('filter'):
        query = request.GET.get('filter')
        if query == "All":
            transac = Transaction.objects.filter(student_id=st_id).order_by('-id')
            for i in transac:
                tot = tot+int(i.ammount)
            print(tot)
        else:
            transac = Transaction.objects.filter(student_id=st_id ,transaction_type = query).order_by('-id')
            for i in transac:
                tot = tot+int(i.ammount)
            print(tot)
    else:
        transac = Transaction.objects.filter(student_id=st_id).order_by('-id')
        for i in transac:
            tot = tot+int(i.ammount)
        print(tot)

    return render(request,"alluser_template/payment_history.html",{'transac':transac,'tot':tot})
