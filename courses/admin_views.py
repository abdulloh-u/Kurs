from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Course
from django.utils.text import slugify

def is_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def admin_course_list(request):
    courses = Course.objects.all().order_by('-id')
    return render(request, 'courses/admin_course_list.html', {'courses': courses})

@user_passes_test(is_staff)
def admin_course_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        
        slug = slugify(title)
        counter = 1
        original_slug = slug
        while Course.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
            
        Course.objects.create(
            title=title,
            slug=slug,
            description=description,
            price=price,
            duration=duration
        )
        return redirect('admin_course_list')
    return render(request, 'courses/admin_course_form.html', {'action': 'Qo\'shish'})

@user_passes_test(is_staff)
def admin_course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.price = request.POST.get('price')
        course.duration = request.POST.get('duration')
        course.save()
        return redirect('admin_course_list')
    return render(request, 'courses/admin_course_form.html', {'course': course, 'action': 'Tahrirlash'})

@user_passes_test(is_staff)
def admin_course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('admin_course_list')
