from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.db.models import Q
import csv
from .models import Application
from courses.models import Course

def is_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def admin_dashboard(request):
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    course_filter = request.GET.get('course', '')
    
    applications = Application.objects.all().order_by('-created_at')
    courses = Course.objects.all()
    
    if search_query:
        applications = applications.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
        
    if status_filter:
        applications = applications.filter(status=status_filter)
        
    if course_filter:
        applications = applications.filter(course_id=course_filter)
        
    total_apps = Application.objects.count()
    new_apps = Application.objects.filter(status='new').count()
    approved_apps = Application.objects.filter(status='approved').count()
    rejected_apps = Application.objects.filter(status='rejected').count()
    
    context = {
        'applications': applications,
        'courses': courses,
        'search_query': search_query,
        'status_filter': status_filter,
        'course_filter': course_filter,
        'total_apps': total_apps,
        'new_apps': new_apps,
        'approved_apps': approved_apps,
        'rejected_apps': rejected_apps,
    }
    return render(request, 'applications/admin_dashboard.html', context)

@user_passes_test(is_staff)
def update_application_status(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    new_status = request.GET.get('status')
    if new_status in ['new', 'approved', 'rejected']:
        app.status = new_status
        app.save()
    return redirect('admin_dashboard')

@user_passes_test(is_staff)
def delete_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    app.delete()
    return redirect('admin_dashboard')

@user_passes_test(is_staff)
def export_applications_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="arizalar.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Ism', 'Familiya', 'Telefon', 'Kurs', 'Sinf', 'Izoh', 'Holati', 'Sana'])
    
    applications = Application.objects.all().values_list(
        'id', 'first_name', 'last_name', 'phone_number', 'course__title', 'school_grade', 'comment', 'status', 'created_at'
    )
    for app in applications:
        writer.writerow(app)
        
    return response
