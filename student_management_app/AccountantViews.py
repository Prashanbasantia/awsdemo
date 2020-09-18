import json
import datetime
from datetime import date
from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_management_app.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, \
    LeaveReportStaff, Staffs, FeedBackStaffs, CustomUser, Courses,Accountants ,Transaction, Notice
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# subject = 'Subject'
# html_message = render_to_string('accountant_template/mail_receipt.html', {'context': 'values'})
# plain_message = strip_tags(html_message)
# from_email = 'From <from@example.com>'
# to = 'to@example.com'

# mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def accountant_home(request): 
    #for today total paymets
    today=date.today()
    money = Transaction.objects.all().filter(created_at__date=today)
    today_payments= 0
    for m in money:
        today_payments =int(m.ammount)+today_payments
    current_month = datetime.datetime.now().month
    #for monthly total paymets
    month_money = Transaction.objects.all().filter(created_at__month=current_month)
    monthly_payments= 0
    for mm in month_money:
        monthly_payments =int(mm.ammount)+monthly_payments
    
    
    # #For Fetch All Student Under Staff
    # subjects=Subjects.objects.filter(staff_id=request.user.id)
    # course_id_list=[]
    # for subject in subjects:
    #     course=Courses.objects.get(id=subject.course_id.id)
    #     course_id_list.append(course.id)

    # final_course=[]
    # #removing Duplicate Course ID
    # for course_id in course_id_list:
    #     if course_id not in final_course:
    #         final_course.append(course_id)

    # students_count=Students.objects.filter(course_id__in=final_course).count()

    # #Fetch All Attendance Count
    # attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    # #Fetch All Approve Leave
    # accountant=Accountants.objects.get(admin=request.user.id)
    # leave_count=LeaveReportStaff.objects.filter(accountant_id=accountant.id,leave_status=1).count()
    # subject_count=subjects.count()

    # #Fetch Attendance Data by Subject
    # subject_list=[]
    # attendance_list=[]
    # for subject in subjects:
    #     attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
    #     subject_list.append(subject.subject_name)
    #     attendance_list.append(attendance_count1)

    # students_attendance=Students.objects.filter(course_id__in=final_course)
    # student_list=[]
    # student_list_attendance_present=[]
    # student_list_attendance_absent=[]
    # for student in students_attendance:
    #     attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
    #     attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
    #     student_list.append(student.admin.username)
    #     student_list_attendance_present.append(attendance_present_count)
    #     student_list_attendance_absent.append(attendance_absent_count)
    context={
        'today_payments':today_payments,
        'monthly_payments':monthly_payments
    }
    return render(request,"accountant_template/accountant_home_template.html",context)

def make_new_payment(request):
    return render(request,"accountant_template/make_new_payment.html")

def make_new_payment_save(request):
    if request.method !='POST':
        return HttpResponseRedirect(reverse('accountant_home'))
    else:
        roll_number=request.POST.get('roll_number')
        transaction_type=request.POST.get('fee_type')
        ammount=request.POST.get('ammount')
        student_id=request.POST.get('student_id')
        student_name=request.POST.get('student_name')
        x = datetime.datetime.now()
        s =x.strftime("%S")
        mn =x.strftime("%M")
        h = x.strftime("%H")
        d = x.strftime("%d")
        m = x.strftime("%m")
        y = x.strftime("%y")
        receipt_id = m+d+y+mn+h+s
        student_obj=CustomUser.objects.get(id=student_id)
        sp = Students.objects.get(admin_id= student_obj)
        balance = sp.payments
        s_id = sp.id
        
        try:
            receipt=Transaction(student_id=student_obj,roll_number = roll_number,name = student_name,transaction_type=transaction_type,ammount=ammount,receipt_id=receipt_id)
            receipt.save()
            balance = float(balance) + float(ammount)
            pay=Students.objects.get(id=s_id)
            pay.payments=balance
            pay.save()
            messages.success(request, "Money Added Successfully")
            return HttpResponseRedirect(reverse("make_new_payment"))
        except Exception as e:
            messages.error(request, "Failed to make Payment {}".format(e))
            return HttpResponseRedirect(reverse("make_new_payment"))

def payments_history(request):
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    if request.method =='POST':
        transac = Transaction.objects.filter(created_at__gte=from_date,created_at__lte=to_date).order_by('-id')
        if transac.count() == 0:
            transac = Transaction.objects.all().order_by('-id')
            messages.error(request, "No Transaction Found ! This Is your Default All Transaction")
        messages.success(request, "Transaction From Date: {}  To Date: {}".format(from_date,to_date))   
    else:
        transac = Transaction.objects.all().order_by('-id')
    return render(request,"accountant_template/payments_history.html",{'transac':transac})


def check_students_payments(request):
    bran_ug = request.POST.get("ug_branch")
    sy_ug = request.POST.get("ug_sess_year")
    bran_pg = request.POST.get("pg_branch")
    sy_pg = request.POST.get("pg_sess_year")
    butt_on = "False"
    butt_on2 = "False"
    branch_ug = Courses.objects.filter(course_for="ug")
    session_year_ug = SessionYearModel.object.filter(session_for = "ug")

    branch_pg = Courses.objects.filter(course_for="pg")
    session_year_pg = SessionYearModel.object.filter(session_for = "pg")
    
    
    if request.method == "POST":
        if bran_pg == None and sy_pg == None:
            students=Students.objects.filter(course_id_id=bran_ug,session_year_id_id = sy_ug,course_id__course_for ="ug")
            if students.count() == 0 :
                students_pg=Students.objects.filter(course_id__course_for ="pg").order_by("-id")
                butt_on = "True"
                butt_on2 = "False"
                messages.error(request, "No Students Found ! Invalid Inputs")
            else:
                students_pg=Students.objects.filter(course_id__course_for ="pg").order_by("-id")
                messages.success(request, "Succefully Students fetch According to Your request")
        else:
            students_pg=Students.objects.filter(course_id_id=bran_pg,session_year_id_id = sy_pg,course_id__course_for ="pg")
            if students_pg.count()==0:
                students=Students.objects.filter(course_id__course_for ="ug").order_by("-id")
                butt_on = "False"
                butt_on2 = "True"
                messages.error(request, "No Students Found ! Invalid Inputs")
            else:
                students=Students.objects.filter(course_id__course_for ="ug").order_by("-id")
                messages.success(request, "Succefully Students fetch According to Your request")


    else:
        students=Students.objects.filter(course_id__course_for ="ug").order_by("-id")
        students_pg=Students.objects.filter(course_id__course_for ="pg").order_by("-id")
    context = {
        "branch_pg":branch_pg,"session_year_pg":session_year_pg, 
        "branch_ug":branch_ug,"session_year_ug":session_year_ug,
        "students":students,"students_pg":students_pg,
        "butt_on":butt_on,"butt_on2":butt_on2
        }
    return render(request,"accountant_template/check_students_payments.html",context)



def student_payment_details(request,student_id):
    student=CustomUser.objects.get(id=student_id)
    # # student_id = user.id 
    # student = Students.objects.get(admin = student_id)
    tot = 0
    if request.GET.get('filter'):
        query = request.GET.get('filter')
        if query == "All":
            transac = Transaction.objects.filter(student_id=student_id).order_by('-id')
            for i in transac:
                tot = tot+int(i.ammount)
            print(tot)
        else:
            transac = Transaction.objects.filter(student_id=student_id ,transaction_type = query).order_by('-id')
            for i in transac:
                tot = tot+int(i.ammount)
            print(tot)
    else:
        transac = Transaction.objects.filter(student_id=student_id).order_by('-id')
        for i in transac:
            tot = tot+int(i.ammount)
        print(tot)
    context={
        "transac":transac,
        "tot":tot,
        "student_id":student_id,
        "student":student
    }
    return render(request,"accountant_template/view_payments_details.html",context)
def payment_reminder_mail(request,student_id):
    student=CustomUser.objects.get(id=student_id)
    context={
        "student":student
    }
    return render(request,"accountant_template/payment_reminder_mail_modal.html",context)
def pay_remind_mailsend(request):
    if request.method !="POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id = request.POST.get("student_id")
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")

        try:

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                )
            messages.success(request,"Mail send Successfuly")
            return HttpResponseRedirect(reverse("student_payment_details",kwargs={"student_id":student_id}))
        except:
            messages.error(request,"Failed to send Mail")
            return HttpResponseRedirect(reverse("student_payment_details",kwargs={"student_id":student_id}))

def notices(request):
    notice = Notice.objects.all().order_by('-id')
    return render(request,"accountant_template/notices.html",{'notice':notice})

def add_notice(request):
    return render(request,"accountant_template/add_notice.html")
def add_notice_save(request):
    if request.method !='POST':
        return HttpResponseRedirect(reverse('add_notice'))
    else:
        subject=request.POST.get('subject')
        content=request.POST.get('content')
        try:
            notice=Notice(subject=subject,content = content)
            notice.save()
            messages.success(request, "Notice Added Successfully")
            return HttpResponseRedirect(reverse("add_notice"))
        except Exception as e:
            messages.error(request, "Failed to Add Notice {}".format(e))
            return HttpResponseRedirect(reverse("add_notice"))
def edit_notice(request,notice_id):
    notice=Notice.objects.get(id=notice_id)
    return render(request,"accountant_template/edit_notice.html",{'notice':notice})

def edit_notice_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        notice_id=request.POST.get("notice_id")
        subject=request.POST.get("subject")
        content=request.POST.get("content")
        try:
            notice=Notice.objects.get(id=notice_id)
            notice.subject=subject
            notice.content=content
            notice.save()
            messages.success(request,"Successfully Edited Notice")
            return HttpResponseRedirect(reverse("edit_notice",kwargs={"notice_id":notice_id}))
        except:
            messages.error(request,"Failed to Edit Notice")
            return HttpResponseRedirect(reverse("edit_notice",kwargs={"notice_id":notice_id}))
def delete_notice(request,notice_id):
    notice=Notice.objects.get(id=notice_id).delete()
    return HttpResponseRedirect(reverse("notices"))
    
@csrf_exempt
def check_rollno_exist(request):
    roll_no=request.POST.get("roll_number")
    user_obj=CustomUser.objects.filter(username=roll_no).exists()

    if user_obj:
     
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def fetch_rollno(request):
    roll_number=request.POST.get("roll_number")
    fetch_data = CustomUser.objects.get(username__exact=roll_number)
    list_data={"name":fetch_data.first_name+" "+fetch_data.last_name,"email":fetch_data.email,"id":fetch_data.id}
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)
