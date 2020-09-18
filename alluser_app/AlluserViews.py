from django.shortcuts import render ,redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from student_management_app.models import Notice,Courses,NeetApply,SessionYearModel,StudentResult,Courses,CustomUser,Students
# Create your views here.

def index(request):
    notices = Notice.objects.all().order_by('-id')[:5]
    return render(request ,'alluser_template/index.html',{'notices':notices})


def contact(request):
    return render(request ,'alluser_template/contactus.html')


def courses(request):
    return render(request ,'alluser_template/courses.html')

def view_result(request):
    session_year = SessionYearModel.object.all()
    return render(request ,'alluser_template/view_result.html',{'session_year':session_year})

def match_result_data(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        roll_number=request.POST.get("roll_number")
        student_obj = CustomUser.objects.get(username=roll_number)
        student_id = student_obj.id
        student = Students.objects.get(admin_id=student_id)
        branch=student.course_id_id
        course = Courses.objects.get(id= branch)
        stream = course.course_name

        dob=request.POST.get("dob")
        semester=request.POST.get("semester")
        session_year=request.POST.get("session_year")
        try:
            result = StudentResult.objects.filter(roll_number=roll_number,dob = dob,session_year =session_year,semester = semester)
            if result:
                context = {
                'result':result,
                'semester':semester,
                'stream':stream}
                return render(request ,'alluser_template/result.html',context)
            else:
                messages.error(request,"Invalid Inputs")
                return HttpResponseRedirect(reverse("view_result"))
            
        except Exception as e:
            print(e)
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("view_result")) 
            print("somthing went wrong")
def notice(request):
    notices = Notice.objects.all().order_by('-id')
    return render(request ,'alluser_template/notice.html',{'notices':notices})


def notice_full(request , subject):
    # notices = Notices.objects.all().filter(subject = subject).first()
    
    return render(request ,'alluser_template/notice.html')
def neet_apply(request):
    course = Courses.objects.all()
    return  render(request,"alluser_template/neet.html",{'course':course})
def neet_apply_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("neet_apply"))
    else:
        course=request.POST.get("department")
        full_name=request.POST.get("full_name")
        father_name=request.POST.get("father_name")
        mother_name=request.POST.get("mother_name")
        dob=request.POST.get("dob")
        gender=request.POST.get("gender")
        cast_category=request.POST.get("cast_category")
        aaddhar_number=request.POST.get("aaddharno")
        phone_number=request.POST.get("mobile")
        email=request.POST.get("email")

        at_pre=request.POST.get("at_pre")
        po_pre=request.POST.get("po_pre")
        gp_pre=request.POST.get("gp_pre")
        ps_pre=request.POST.get("ps_pre")
        dist_pre=request.POST.get("dist_pre")
        state_pre=request.POST.get("state_pre")
        pin_pre=request.POST.get("pin_pre")

        at_per=request.POST.get("at_per")
        po_per=request.POST.get("po_per")
        gp_per=request.POST.get("gp_per")
        ps_per=request.POST.get("ps_per")
        dist_per=request.POST.get("dist_per")
        state_per=request.POST.get("state_per")
        pin_per=request.POST.get("pin_per")

        tenth_passed=request.POST.get("tenth_passed")
        tenth_year=request.POST.get("tenth_year")
        tenth_school=request.POST.get("tenth_school")
        tenth_board=request.POST.get("tenth_board")
        tenth_fullmark=request.POST.get("tenth_fullmark")
        tenth_securedmark=request.POST.get("tenth_securedmark")
        tenth_percent=request.POST.get("tenth_percent")

        twelth_passed=request.POST.get("twelth_passed")
        twelth_year=request.POST.get("twelth_year")
        twelth_school=request.POST.get("twelth_school")
        twelth_board=request.POST.get("twelth_board")
        twelth_fullmark=request.POST.get("twelth_fullmark")
        twelth_securedmark=request.POST.get("twelth_securedmark")
        twelth_percent=request.POST.get("twelth_percent")

        grad_passed=request.POST.get("grad_passed")
        grad_year=request.POST.get("grad_year")
        grad_school=request.POST.get("grad_school")
        grad_board=request.POST.get("grad_board")
        grad_fullmark=request.POST.get("grad_fullmark")
        grad_securedmark=request.POST.get("grad_securedmark")
        grad_percent=request.POST.get("grad_percent")
        try:
            neet=NeetApply(course = course,full_name=full_name,father_name=father_name,mother_name = mother_name,
            dob = dob ,gender = gender, cast_category = cast_category,aaddhar_number = aaddhar_number,phone_number = phone_number,email=email,
            at_pre=at_pre,po_pre = po_pre,gp_pre=gp_pre,ps_pre=ps_pre,dist_pre =dist_pre,state_pre = state_pre,pin_pre = pin_pre,
            at_per=at_per,po_per = po_per,gp_per=gp_per,ps_per=ps_per,dist_per =dist_per,state_per = state_per,pin_per = pin_per,
            tenth_passed = tenth_passed,tenth_year = tenth_year,tenth_school = tenth_school,tenth_board=tenth_board,
            tenth_fullmark= twelth_fullmark,tenth_securedmark = tenth_securedmark,tenth_percent = tenth_percent,
            twelth_passed = twelth_passed,twelth_year = twelth_year,twelth_school = twelth_school,twelth_board=twelth_board,
            twelth_fullmark= twelth_fullmark,twelth_securedmark = twelth_securedmark,twelth_percent = twelth_percent,
            grad_passed = grad_passed,grad_year = grad_year,grad_school = grad_school,grad_board=grad_board,
            grad_fullmark= grad_fullmark,grad_securedmark = grad_securedmark,grad_percent = grad_percent)
            neet.save()
            messages.success(request,"Successfully Aplied")
            return HttpResponseRedirect(reverse('neet_apply'))
        except Exception as e:
            messages.error(request,"Error in Applying ")
            return HttpResponseRedirect(reverse('neet_apply'))


