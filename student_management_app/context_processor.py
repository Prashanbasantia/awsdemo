from student_management_app.models import Notice
def seen_processor(request):
    seen = Notice.objects.filter(seen=False).count()
    return {'seen':seen}