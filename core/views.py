from django.shortcuts import render
from courses.models import Course
from applications.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

def home_view(request):
    courses = Course.objects.all()[:6]
    total_students = User.objects.count()
    total_courses = Course.objects.count()
    total_applications = Application.objects.count()
    
    context = {
        'courses': courses,
        'total_students': total_students,
        'total_courses': total_courses,
        'total_applications': total_applications,
    }
    return render(request, 'home.html', context)
