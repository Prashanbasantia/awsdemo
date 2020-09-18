from django import forms

from student_management_app.models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    mobile=forms.IntegerField(label="Phone",widget=forms.NumberInput(attrs={"class":"form-control","autocomplete":"off"}))
    username=forms.CharField(label="Roll No",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    
    course_list=[]
    try:
        courses=Courses.objects.all()
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]
    #course_list=[]

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year)+"   -  "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list=[]

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    course=forms.ChoiceField(label="Branch",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    dob=forms.DateField(label="Date Of Birth",widget=DateInput(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    aaddhar=forms.IntegerField(label="Aaddhar",widget=forms.NumberInput(attrs={"class":"form-control","autocomplete":"off"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control","autocomplete":"new-password"}))

class EditStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Roll No",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))


    course_list=[]
    try:
        courses = Courses.objects.all()
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year)+"   -  "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        pass
        #session_list = []

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    course=forms.ChoiceField(label="Branch",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))

class StudentPhotoForm(forms.Form):
    profile_photo=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=True)
