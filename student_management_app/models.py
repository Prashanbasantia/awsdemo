from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.
class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.IntegerField()
    session_end_year=models.IntegerField()
    session_for = models.CharField(max_length=125 )
    object=models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"),(4,"Accountant"))
    profile_photo = models.FileField()
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
class Accountants(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
class Transaction(models.Model):
    id=models.AutoField(primary_key=True)
    transaction_type=models.CharField(max_length=255)
    ammount = models.FloatField()
    student_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=125)
    name = models.CharField(max_length=125)
    receipt_id = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    course_for = models.CharField(max_length=125 )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE)
    course_name=models.CharField(max_length=255)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    dob=models.DateField(null=True)
    address=models.TextField()
    mobile=models.CharField(max_length=225 ,unique=True)
    aaddhar=models.CharField(max_length= 225, unique=True)
    payments = models.FloatField(default=0)
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()




class StudentResult(models.Model):
    id=models.AutoField(primary_key=True)
    total_mark=models.FloatField(default=0)
    secured_mark=models.FloatField(default=0)
    prac_total_mark=models.CharField(max_length=225,blank=True,null=True)
    prac_secured_mark=models.CharField(max_length= 225,blank=True,null=True)
    roll_number = models.CharField(max_length=250)
    semester = models.CharField(max_length=150)
    subject_name=models.CharField(max_length=150)
    session_year=models.CharField(max_length=150)
    branch = models.CharField(max_length=150)
    is_pass = models.CharField(max_length=150)
    dob=models.CharField(max_length=150)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    objects=models.Manager()
class NeetApply(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    cast_category = models.CharField(max_length=255)
    aaddhar_number = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    at_per = models.CharField(max_length=255)
    po_per = models.CharField(max_length=255)
    gp_per = models.CharField(max_length=255)
    ps_per = models.CharField(max_length=255)
    dist_per = models.CharField(max_length=255)
    state_per = models.CharField(max_length=255)
    pin_per = models.CharField(max_length=255)

    at_pre = models.CharField(max_length=255)
    po_pre = models.CharField(max_length=255)
    gp_pre = models.CharField(max_length=255)
    ps_pre = models.CharField(max_length=255)
    dist_pre = models.CharField(max_length=255)
    state_pre = models.CharField(max_length=255)
    pin_pre = models.CharField(max_length=255)

    tenth_passed = models.CharField(max_length=255)
    tenth_year = models.CharField(max_length=255)
    tenth_school = models.CharField(max_length=255)
    tenth_board = models.CharField(max_length=255)
    tenth_fullmark=models.CharField(max_length=255)
    tenth_securedmark = models.CharField(max_length=255)
    tenth_percent = models.CharField(max_length=255)

    twelth_passed = models.CharField(max_length=255)
    twelth_year = models.CharField(max_length=255)
    twelth_school = models.CharField(max_length=255)
    twelth_board = models.CharField(max_length=255)
    twelth_fullmark=models.CharField(max_length=255)
    twelth_securedmark = models.CharField(max_length=255)
    twelth_percent = models.CharField(max_length=255)

    grad_passed = models.CharField(max_length=255, blank=True,null = True,default="None")
    grad_year = models.CharField(max_length=255, blank=True,null = True,default="None")
    grad_school = models.CharField(max_length=255, blank=True,null = True,default="None")
    grad_board = models.CharField(max_length=255, blank=True,null = True,default="None")
    grad_fullmark=models.CharField(max_length=255, blank=True,null = True,default="None")
    grad_securedmark = models.CharField(max_length=255, blank=True,null = True,default="None")
    grad_percent = models.CharField(max_length=255, blank=True,null = True,default="None")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Notice(models.Model):
    id=models.AutoField(primary_key=True)
    subject=models.CharField(max_length=255)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    objects=models.Manager()
class Otp(models.Model):
    id=models.AutoField(primary_key=True)
    otp_code = models.IntegerField()
    student_id=models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_expier = models.BooleanField(default=False)
    objects=models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")
        if instance.user_type==3:
            Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),session_year_id=SessionYearModel.object.get(id=1),address="",gender="")
        if instance.user_type==4:
            Accountants.objects.create(admin=instance,address="")
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()
    if instance.user_type==4:
        instance.accountants.save()
