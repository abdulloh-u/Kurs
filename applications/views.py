from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.conf import settings
import csv
import requests
from courses.models import Course
from .models import Application
from .utils import send_telegram_notification

def send_user_status_notification(application, status):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    if not token or not application.note:
        return
    
    try:
        # CHAT_ID formatini tekshirib olish
        if 'CHAT_ID:' in application.note:
            chat_id = application.note.split('CHAT_ID:')[1].split()[0].strip()
        else:
            return

        course_name = application.course.title if application.course else "Tanlangan kurs"
        
        if status == 'approved':
            message = (
                f"🎉 <b>Tabriklaymiz, {application.first_name}!</b>\n\n"
                f"Sizning <b>«{course_name}»</b> kursi bo'yicha yuborgan arizangiz <b>TASDIQLANDI!</b> ✅\n\n"
                f"Tez orada Qabul bo'limimiz siz bilan bog'lanadi."
            )
        elif status == 'rejected':
            message = (
                f"❌ <b>Xabarnoma</b>\n\n"
                f"Hurmatli {application.first_name}, afsuski sizning <b>«{course_name}»</b> kursi bo'yicha yuborgan arizangiz <b>BEKOR QILINDI</b>."
            )
        else:
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Xabar yuborishda xatolik: {e}")

def apply_course(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone_number')
        age_str = request.POST.get('age')
        course_id = request.POST.get('course')
        note = request.POST.get('comment')
        
        if not first_name or not last_name or not phone or not age_str or not course_id:
            return render(request, 'apply.html', {'courses': courses, 'error': "Barcha majburiy maydonlarni to'ldiring!"})
        
        # Yoshni tekshirish (10 dan 36 gacha)
        try:
            age = int(age_str)
            if not (10 <= age <= 36):
                return render(request, 'apply.html', {'courses': courses, 'error': "Yosh 10 yoshdan 36 yoshgacha bo'lishi kerak!"})
        except ValueError:
            return render(request, 'apply.html', {'courses': courses, 'error': "Iltimos, to'g'ri yosh kiriting!"})
        
        course = get_object_or_404(Course, id=course_id)
        
        application = Application.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            age=age,
            course=course,
            note=note or "",
            status='new'
        )
        
        send_telegram_notification(application)
        
        # Arizangiz muvaffaqiyatli qabul qilindi degan xabar bilan sahifani qaytarish
        return render(request, 'apply.html', {
            'courses': courses, 
            'success': True, 
            'message': "Arizangiz qabul qilindi! Tez orada siz bilan bog'lanamiz."
        })
        
    return render(request, 'apply.html', {'courses': courses})

def is_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def admin_dashboard(request):
    search_query = request.GET.get('q', '')
    course_filter = request.GET.get('course', '')
    status_filter = request.GET.get('status', '')

    applications = Application.objects.all().order_by('-created_at')

    if search_query:
        applications = applications.filter(first_name__icontains=search_query) | applications.filter(last_name__icontains=search_query) | applications.filter(phone__icontains=search_query)
    
    if course_filter:
        applications = applications.filter(course_id=course_filter)
        
    if status_filter:
        applications = applications.filter(status=status_filter)

    total_apps = Application.objects.count()
    new_apps = Application.objects.filter(status='new').count() or Application.objects.filter(status__isnull=True).count()
    approved_apps = Application.objects.filter(status='approved').count()
    rejected_apps = Application.objects.filter(status='rejected').count()

    courses = Course.objects.all()

    context = {
        'applications': applications,
        'total_apps': total_apps,
        'new_apps': new_apps,
        'approved_apps': approved_apps,
        'rejected_apps': rejected_apps,
        'courses': courses,
        'search_query': search_query,
        'course_filter': course_filter,
        'status_filter': status_filter,
    }
    return render(request, 'applications/admin_dashboard.html', context)

@user_passes_test(is_staff)
def update_application_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    new_status = request.GET.get('status')
    if new_status in ['new', 'approved', 'rejected']:
        application.status = new_status
        application.save()
        send_user_status_notification(application, new_status)
    return redirect('admin_dashboard')

@user_passes_test(is_staff)
def delete_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    application.delete()
    return redirect('admin_dashboard')

@user_passes_test(is_staff)
def export_applications_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="arizalar.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Ism', 'Familiya', 'Telefon', 'Kurs', 'Yosh', 'Izoh', 'Holat', 'Sana'])
    
    applications = Application.objects.all().values_list('id', 'first_name', 'last_name', 'phone', 'course__title', 'age', 'note', 'status', 'created_at')
    for app in applications:
        writer.writerow(app)
        
    return response