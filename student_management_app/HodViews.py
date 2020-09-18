import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from student_management_app.forms import AddStudentForm, EditStudentForm
from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students,SessionYearModel,FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport,Accountants,NeetApply,StudentResult
import datetime
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

class neet_student_pdf(View):
    def get(self, request,neet_id, *args, **kwargs):
        template = get_template('hod_template/neet_student_pdf.html')
        neet_student=NeetApply.objects.get(id=neet_id)
        context = {
           'neet_student':neet_student
        }
        html = template.render(context)
        pdf = render_to_pdf('hod_template/neet_student_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "NEET_student_Apply%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()
    

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.filter(course_id=1)
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        ses = SessionYearModel.object.get(id=subject.session_year_id.id)
        student_count=Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name + '(' + str(ses.session_start_year) + '-'+ str(ses.session_end_year) + ')')
        student_count_list_in_subject.append(student_count)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)
    context = {"student_count":student_count1,
    "staff_count":staff_count,"subject_count":subject_count,
    "course_count":course_count,"course_name_list":course_name_list,
    "subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,
    "student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,
    "attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,
    "student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,
    "attendance_absent_list_student":attendance_absent_list_student}

    return render(request,"hod_template/home_content.html" ,context)
    

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_accountant(request):
    return render(request,"hod_template/add_accountant_template.html")

def add_accountant_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=4)
            user.accountants.address=address
            user.save()
            messages.success(request,"Successfully Added Accountnt")
            return HttpResponseRedirect(reverse("add_accountant"))
        except Exception as e:
            messages.error(request,"Failed to Add Accountant  {}".format(e))
            return HttpResponseRedirect(reverse("add_accountant"))


def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_for=request.POST.get("course_for")
        course=request.POST.get("course")
        try:
            course_model=Courses(course_for=course_for,course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added  '{}' Course . ".format(course))
            return HttpResponseRedirect(reverse("add_course"))
        except Exception as e:
            messages.error(request,"Failed To Add Course {}".format(e))
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]
            dob=form.cleaned_data["dob"]
            mobile=form.cleaned_data["mobile"]
            aaddhar=form.cleaned_data["aaddhar"]

            
            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                session_year=SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id=session_year
                user.students.gender=sex
                user.students.mobile=mobile
                user.students.dob=dob
                user.students.aaddhar=aaddhar
                user.save()
                send_mail(
                        'Registration ',
                        "this is your oassword :"+password ,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                        ) 
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except Exception as e:
                messages.error(request,"Failed to Add Student {}".format(e))
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses=Courses.objects.all()
    session_year = SessionYearModel.object.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses,"session_year":session_year})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        session_year_id = request.POST.get("session_year")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)
        c_n = Courses.objects.filter(id =course_id)
        cor=[]
        for c in c_n:
            cor.append(c.course_name)
        course_name =cor[0]
         
        try:
            
            subject=Subjects(subject_name=subject_name,course_name=course_name,course_id=course, session_year_id_id = session_year_id, staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject {}" )
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
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
    return render(request,"hod_template/manage_student_template.html",context)
    


def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]
            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                student.mobile=mobile
                student.dob=dob
                student.aaddhar=aaddhar
                session_year = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender=sex
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    session_year = SessionYearModel.object.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id,"session_year":session_year})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))


def manage_session(request):
    sess_ug= SessionYearModel.object.filter(session_for = "ug")
    sess_pg= SessionYearModel.object.filter(session_for = "pg")
    return render(request,"hod_template/manage_session_template.html" , {"sess_ug":sess_ug,"sess_pg":sess_pg})

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_year_for=request.POST.get("session_year_for")
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_for = session_year_for,session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except Exception as e:
            messages.error(request, "Failed to Add Sessions")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_mobile_exist(request):
    mobile=request.POST.get("mobile")
    user_obj=Students.objects.filter(mobile=mobile).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_aaddhar_exist(request):
    aaddhar=request.POST.get("aaddhar")
    user_obj=Students.objects.filter(aaddhar=aaddhar).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":feedbacks})

def student_feedback_message(request):
    feedbacks=FeedBackStudent.objects.all()
    return render(request,"hod_template/student_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    subjects=Subjects.objects.all()
    session_year_id=SessionYearModel.object.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method !="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def add_students_result(request):
    session_year = SessionYearModel.object.all().order_by('-id')
    subject = Subjects.objects.all().order_by('-id')
    branch = Courses.objects.all().order_by('-id')
    context={
        'session_year':session_year,
        'subject':subject,
        'branch':branch
    }
    return render(request,"hod_template/add_students_result.html",context)

def save_students_result(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("add_students_result"))
    else:
        roll_number=request.POST.get("roll_number")
        student_obj = CustomUser.objects.get(username=roll_number)
        student_id = student_obj.id
        
        student = Students.objects.get(admin_id=student_id)
        session_year=student.session_year_id_id
        branch=student.course_id_id
        dob = student.dob
        semester=request.POST.get("semester")
        subject_name=request.POST.get("subject_name")
        total_mark=request.POST.get("total_mark")
        secured_mark=request.POST.get("secured_mark")
        prac_total_mark=request.POST.get("prac_total_mark")
        prac_secured_mark=request.POST.get("prac_secured_mark")
        is_pass=request.POST.get("is_pass")
        print(student_id,session_year,branch)
        # try:
        student_result = StudentResult(roll_number = roll_number,session_year = session_year,branch = branch,semester=semester,subject_name =subject_name,total_mark=total_mark,secured_mark=secured_mark,prac_total_mark=prac_total_mark,prac_secured_mark=prac_secured_mark,is_pass = is_pass,dob = dob)
        student_result.save()
        messages.success(request, " Result Added Successfully")
        return HttpResponseRedirect(reverse("add_students_result"))
        # except Exception as e:
    messages.error(request, "Failed to Add Result {}")
    return HttpResponseRedirect(reverse("add_students_result"))

@csrf_exempt
def check_rollNumber_exist(request):
    roll_no=request.POST.get("roll_number")
    user_obj=CustomUser.objects.filter(username=roll_no).exists()

    if user_obj:
     
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def fetch_rollNumber(request):
    roll_number=request.POST.get("roll_number")
    fetch_data = CustomUser.objects.get(username__exact=roll_number)
    list_data={"name":fetch_data.first_name+" "+fetch_data.last_name,"id":fetch_data.id}
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def view_neet_students(request):
    neet_students = NeetApply.objects.all().order_by('-id')
    return render(request,"hod_template/view_neet_students.html",{"neet_students":neet_students})
def delete_neet_student(request,neet_id):
    neet=NeetApply.objects.get(id=neet_id).delete()
    return HttpResponseRedirect(reverse("view_neet_students"))